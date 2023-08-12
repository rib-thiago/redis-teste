from flask import Flask, jsonify, render_template, request, redirect, url_for
import os
import redis
from uuid import uuid4
from io import BytesIO
from PIL import Image
import cv2
import utilities.preprocess as pp

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static/images')


# Conexão com o banco de dados Redis
# Configuração da conexão ao Redis
redis_host = 'localhost'
redis_port = 6379
redis_password = 'qwert'  # Substitua pela senha do seu Redis
redis_db = 0


# Conexão com o banco de dados Redis
redis_client = redis.StrictRedis(
    host=redis_host, port=redis_port, password=redis_password, db=redis_db)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image = request.files['image']
        if image:
            image_id = str(uuid4())
            image_path = os.path.join(
                app.config['UPLOAD_FOLDER'], image_id + '.jpg')
            image.save(image_path)

            # Cria a URL da imagem para passar ao template
            image_url = url_for(
                'static', filename='images/' + image_id + '.jpg')

            # Renderiza a imagem para o usuário
            return render_template('preview.html', image_url=image_url, image_id=image_id)
    return render_template('index.html')


@app.route('/save/<image_id>', methods=['POST'])
def save_image(image_id):
    image_url = request.form.get('image_url')
    photo_name = request.form.get('photo_name')
    photo_date = request.form.get('photo_date')
    collection_name = request.form.get('collection_name')

    # Crie um hash com as informações da imagem
    image_data = {
        'image_url': image_url,
        'photo_name': photo_name,
        'photo_date': photo_date,
        'collection_name': collection_name
    }

    # Armazene o hash da imagem no Redis
    redis_client.hmset(image_id, image_data)

    # Adicione o image_id à lista da galeria no Redis
    redis_client.lpush('gallery', image_id)

    return redirect(url_for('index'))


@app.route('/gallery')
def gallery():
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
