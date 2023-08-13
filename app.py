from flask import Flask, jsonify, render_template, request, redirect, url_for
import os
import redis
from uuid import uuid4
from io import BytesIO
from PIL import Image
import cv2
import utilities.preprocess as pp
from config import Config
from redis_connection import RedisConnection

app = Flask(__name__)
app.config.from_object(Config)

# Cria uma instância da classe RedisConnection para gerenciar a conexão do Redis
redis_connection = RedisConnection()

# Obtém o cliente Redis do RedisConnection
redis_client = redis_connection.get_client()


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Página inicial do aplicativo de edição de imagens.

    Esta rota é responsável por lidar com as solicitações para a página inicial do aplicativo.
    Quando uma solicitação POST é recebida, verifica se um arquivo de imagem foi enviado pelo usuário.
    Se um arquivo de imagem for recebido, ele é salvo no sistema de arquivos com um ID único.
    Em seguida, a rota renderiza a página de pré-visualização, exibindo a imagem carregada e
    fornecendo um ID de imagem único para referência.

    Returns:
        render_template: A página HTML renderizada com a imagem carregada (se aplicável) e o ID da imagem.

    Note:
        Certifique-se de que o objeto Flask 'app' esteja configurado corretamente e que as bibliotecas
        necessárias estejam importadas.
        A página renderizada exibirá a imagem carregada e permitirá que o usuário visualize e selecione
        as opções de edição disponíveis.
    """
    if request.method == 'POST':
        image = request.files['image']
        if image:
            image_id = str(uuid4())
            image_path = os.path.join(
                app.config['UPLOAD_FOLDER'], image_id + '.jpg')
            image.save(image_path)

            image_url = url_for(
                'static', filename='images/' + image_id + '.jpg')

            return render_template('preview.html', image_url=image_url, image_id=image_id)
    return render_template('index.html')


@app.route('/save/<image_id>', methods=['POST'])
def save_image(image_id):
    """
    Salva informações da imagem no banco de dados e adiciona à galeria.

    Esta rota trata solicitações POST para salvar informações associadas a uma imagem no banco de dados
    (nesse caso, Redis). As informações incluem a URL da imagem, o nome da foto, a data da foto
    e o nome da coleção. As informações são armazenadas em um hash associado ao ID da imagem.
    Além disso, o ID da imagem é adicionado à lista da galeria no Redis para que a imagem possa ser
    exibida na página de galeria.

    Args:
        image_id (str): O ID único da imagem associada às informações.

    Returns:
        redirect: Redireciona o usuário de volta à página inicial após salvar as informações.

    Note:
        Certifique-se de que o objeto Flask 'app' esteja configurado corretamente e que as bibliotecas
        necessárias estejam importadas.
        As informações da imagem são salvas no banco de dados para que possam ser recuperadas posteriormente
        para exibição na página de galeria.
    """
    image_url = request.form.get('image_url')
    photo_name = request.form.get('photo_name')
    photo_date = request.form.get('photo_date')
    collection_name = request.form.get('collection_name')

    image_data = {
        'image_url': image_url,
        'photo_name': photo_name,
        'photo_date': photo_date,
        'collection_name': collection_name
    }

    redis_client.hmset(image_id, image_data)
    redis_client.lpush('gallery', image_id)

    return redirect(url_for('index'))


@app.route('/gallery')
def gallery():
    """
    Exibe a galeria de imagens armazenadas no banco de dados.

    Esta rota exibe a página da galeria, que contém informações sobre as imagens previamente
    salvas no banco de dados (Redis). As informações exibidas incluem a URL da imagem, o nome da foto,
    a data da foto e o nome da coleção. Essas informações são recuperadas do banco de dados e formatadas
    para exibição na página da galeria.

    Returns:
        render_template: A página HTML renderizada com as informações das imagens na galeria.

    Note:
        Certifique-se de que o objeto Flask 'app' esteja configurado corretamente e que as bibliotecas
        necessárias estejam importadas.
        As informações recuperadas do banco de dados são exibidas na página da galeria para que os usuários
        possam visualizar e navegar pelas imagens previamente salvas.
    """
    image_ids = redis_client.lrange('gallery', 0, -1)
    images_info = []

    for img_id in image_ids:
        image_data = redis_client.hgetall(img_id)
        image_info = {
            'image_url': url_for('static', filename='images/' + img_id.decode() + '.jpg'),
            'photo_name': image_data.get(b'photo_name', b'').decode(),
            'photo_date': image_data.get(b'photo_date', b'').decode(),
            'collection_name': image_data.get(b'collection_name', b'').decode()
        }
        images_info.append(image_info)

    return render_template('gallery.html', images_info=images_info)


@app.route('/delete/<image_id>', methods=['POST'])
def delete_image(image_id):
    """
    Exclui uma imagem da galeria.

    Esta rota trata solicitações POST para excluir uma imagem da galeria. Quando uma solicitação POST
    é recebida, o ID da imagem é utilizado para obter o caminho completo do arquivo de imagem no sistema
    de arquivos. O ID da imagem é então removido da lista da galeria no banco de dados (Redis) e o arquivo
    de imagem é excluído do sistema de arquivos. Após a exclusão, o usuário é redirecionado de volta à página
    da galeria.

    Args:
        image_id (str): O ID único da imagem a ser excluída.

    Returns:
        redirect: Redireciona o usuário de volta à página da galeria após a exclusão.

    Note:
        Certifique-se de que o objeto Flask 'app' esteja configurado corretamente e que as bibliotecas
        necessárias estejam importadas.
        A exclusão da imagem é realizada tanto no banco de dados quanto no sistema de arquivos para garantir
        que a imagem seja removida completamente.
    """
    if request.method == 'POST':
        # Obtém o caminho completo do arquivo de imagem a partir do image_id
        image_path = os.path.join(
            app.config['UPLOAD_FOLDER'], image_id + '.jpg')

        # Remove o image_id da lista no Redis
        redis_client.lrem('gallery', 0, image_id)

        # Remove o arquivo de imagem do sistema de arquivos
        if os.path.exists(image_path):
            os.remove(image_path)

        # Redireciona de volta para a página da galeria
        return redirect(url_for('gallery'))


@app.route('/delete_preview/<image_id>')
def delete_image_preview(image_id):
    """
    Exclui uma imagem da galeria durante a visualização.

    Esta rota permite aos usuários excluir uma imagem da galeria enquanto estão visualizando-a na página
    de visualização individual. Quando acessada, a rota utiliza o ID da imagem para obter o caminho completo
    do arquivo de imagem no sistema de arquivos. O ID da imagem é removido da lista da galeria no banco de dados
    (Redis) e o arquivo de imagem é excluído do sistema de arquivos. Após a exclusão, o usuário é redirecionado
    de volta à página inicial.

    Args:
        image_id (str): O ID único da imagem a ser excluída durante a visualização.

    Returns:
        redirect: Redireciona o usuário de volta à página inicial após a exclusão.

    Note:
        Certifique-se de que o objeto Flask 'app' esteja configurado corretamente e que as bibliotecas
        necessárias estejam importadas.
        A exclusão da imagem é realizada tanto no banco de dados quanto no sistema de arquivos para garantir
        que a imagem seja removida completamente.
    """
    # Obtém o caminho completo do arquivo de imagem a partir do image_id
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_id + '.jpg')

    # Remove o image_id da lista no Redis
    redis_client.lrem('gallery', 0, image_id)

    # Remove o arquivo de imagem do sistema de arquivos
    if os.path.exists(image_path):
        os.remove(image_path)

    # Redireciona de volta para a página inicial
    return redirect(url_for('index'))


@app.route('/edit_image/<image_id>', methods=['GET', 'POST'])
def edit_image(image_id):
    """
    Permite a edição de uma imagem carregada.

    Esta rota permite aos usuários editar uma imagem previamente carregada da galeria. A imagem original é carregada
    usando o ID da imagem fornecido e exibida na página de edição. Os usuários podem selecionar entre várias funções
    de edição de imagem disponíveis para aplicar à imagem carregada. Um dicionário é criado para mapear os nomes das
    funções de edição para seus IDs correspondentes para seleção. O usuário também pode visualizar uma versão em
    miniatura da imagem original enquanto escolhe as edições. Após a seleção das edições, o usuário pode confirmar
    e aplicar as edições à imagem. A imagem editada é então salva e exibida na página de visualização.

    Args:
        image_id (str): O ID único da imagem a ser editada.

    Returns:
        render_template: A página HTML renderizada com a imagem original, opções de edição e a versão em miniatura.

    Note:
        Certifique-se de que o objeto Flask 'app' esteja configurado corretamente e que as bibliotecas necessárias
        estejam importadas.
        O usuário pode escolher entre várias funções de edição disponíveis e aplicar as edições à imagem carregada.
        A imagem editada é salva no sistema de arquivos e o usuário é redirecionado para a página de visualização
        para visualizar a imagem editada.
    """
    # Carregue a imagem original usando o image_id
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_id + '.jpg')
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    # Crie um dicionário para mapear os nomes das funções para seus IDs
    methods_ids = {}
    methods_functions = {}
    for method_name in dir(pp):
        method = getattr(pp, method_name)
        if callable(method):
            method_id = len(methods_ids) + 1
            methods_ids[method_name] = method_id
            methods_functions[method_id] = method_name

    # Recupere a URL da imagem da query string
    image_url = request.args.get('image_url')

    return render_template('edit_image.html', image=image, methods_ids=methods_ids, image_url=image_url, image_id=image_id)


@app.route('/apply_method/<method_name>/<image_id>', methods=['POST'])
def apply_method(method_name, image_id):
    """
    Aplica uma função de pré-processamento à imagem carregada.

    Esta rota permite aos usuários aplicar uma função de pré-processamento específica à imagem carregada.
    A imagem original é carregada usando o ID da imagem fornecido e a função de pré-processamento é determinada
    pelo nome do método passado como argumento. A função de pré-processamento é obtida através de reflexão da
    biblioteca de funções de pré-processamento (utilities.preprocess). A função é então aplicada à imagem e a imagem
    resultante é salva no sistema de arquivos. O caminho da imagem processada é retornado como uma resposta JSON.

    Args:
        method_name (str): O nome do método de pré-processamento a ser aplicado à imagem.
        image_id (str): O ID único da imagem a ser processada.

    Returns:
        jsonify: Um objeto JSON contendo o URL da imagem processada.

    Note:
        Certifique-se de que o objeto Flask 'app' esteja configurado corretamente e que as bibliotecas necessárias
        estejam importadas.
        A função de pré-processamento aplicada à imagem deve estar definida na biblioteca de pré-processamento
        (utilities.preprocess).
        A imagem processada é salva no sistema de arquivos e o URL da imagem processada é retornado como uma resposta JSON.
    """
    # Carregue a imagem original usando o image_id
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_id + '.jpg')
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    # Obtenha o método de pré-processamento pelo nome do método
    method = getattr(pp, method_name)

    # Aplique o método de pré-processamento à imagem
    processed_image = method(image)

    # Salve a imagem processada em algum lugar (por exemplo, Redis ou disco)
    # Atualize o caminho da imagem no banco de dados, se necessário

    # Construa o caminho completo da imagem processada
    processed_image_filename = f"{image_id}_processed.jpg"
    processed_image_path = os.path.join(
        app.config['UPLOAD_FOLDER'], processed_image_filename)

    # Salve a imagem processada no caminho especificado
    cv2.imwrite(processed_image_path, processed_image)

    # Retorne o caminho da imagem processada como resposta
    processed_image_url = url_for(
        'static', filename='images/' + processed_image_filename)
    return jsonify({"processed_image_url": processed_image_url})


@app.route('/update/<image_id>', methods=['POST'])
def update_image(image_id):
    """
    Atualiza uma imagem existente na galeria.

    Esta rota permite atualizar uma imagem existente na galeria. Primeiro, verifica se a imagem com o image_id fornecido
    está na galeria. Se estiver, o arquivo da imagem existente é removido do sistema de arquivos. Em seguida, a nova
    imagem enviada pelo usuário é processada e salva no sistema de arquivos. O ID único da nova imagem é gerado e
    atualizado no Redis para refletir a substituição da imagem. A resposta é uma redireção para a página da galeria,
    após a atualização ser concluída.

    Args:
        image_id (str): O ID único da imagem a ser atualizada.

    Returns:
        redirect: Redireciona para a página da galeria após a atualização ser concluída.

        jsonify: Retorna um erro JSON com status 404 se a imagem não for encontrada na galeria.

    Note:
        Certifique-se de que o objeto Flask 'app' esteja configurado corretamente e que as bibliotecas necessárias
        estejam importadas.
        A nova imagem é processada e salva no sistema de arquivos com um novo ID único gerado.
        O Redis é atualizado para refletir a substituição da imagem na galeria.
    """
    if request.method == 'POST':
        # Verifica se a imagem com o image_id existe na galeria
        if redis_client.lindex('gallery', 0) == image_id.encode('utf-8'):
            # Obtém o caminho completo do arquivo de imagem existente
            existing_image_path = os.path.join(
                app.config['UPLOAD_FOLDER'], image_id + '.jpg')

            # Remove o arquivo de imagem existente do sistema de arquivos
            if os.path.exists(existing_image_path):
                os.remove(existing_image_path)

            # Processa a nova imagem enviada pelo usuário
            new_image = request.files['new_image']
            new_image_id = str(uuid4())
            new_image_path = os.path.join(
                app.config['UPLOAD_FOLDER'], new_image_id + '.jpg')
            new_image.save(new_image_path)

            # Atualiza o Redis para refletir a substituição da imagem
            redis_client.lrem('gallery', 0, image_id)
            redis_client.lpush('gallery', new_image_id)

            return redirect(url_for('gallery'))
        else:
            return jsonify({"error": "Image not found in the gallery"}), 404
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    # Verifica se a chave 'gallery' existe no Redis, cria se não existir
    if not redis_client.exists('gallery'):
        # Pode ser qualquer valor, não será usado
        redis_client.lpush('gallery', 'initial_value')

    app.run(debug=True)
