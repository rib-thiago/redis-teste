from flask import Flask, render_template, request, redirect, url_for
import os
import redis
from uuid import uuid4
from io import BytesIO
from PIL import Image

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
    redis_client.lpush('gallery', image_id)
    return redirect(url_for('index'))


@app.route('/gallery')
def gallery():
    image_ids = redis_client.lrange('gallery', 0, -1)
    image_urls = [url_for('static', filename='images/' +
                          img_id.decode() + '.jpg') for img_id in image_ids]
    return render_template('gallery.html', image_urls=image_urls)


@app.route('/delete/<image_id>')
def delete_image(image_id):
    # Obtém o caminho completo do arquivo de imagem a partir do image_id
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_id + '.jpg')

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


if __name__ == '__main__':
    # Verifica se a chave 'gallery' existe no Redis, cria se não existir
    if not redis_client.exists('gallery'):
        # Pode ser qualquer valor, não será usado
        redis_client.lpush('gallery', 'initial_value')

    app.run(debug=True)
