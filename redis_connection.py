import redis
from config import RedisConfig
from flask import url_for
import os


class RedisConnection:
    def __init__(self):
        self.redis_client = redis.StrictRedis(
            host=RedisConfig.HOST, port=RedisConfig.PORT,
            password=RedisConfig.PASSWORD, db=RedisConfig.DB)

    def get_client(self):
        return self.redis_client

    def add_image_to_gallery(self, image_id):
        self.redis_client.lpush('gallery', image_id)

    def save_image_info(self, image_id, image_data):
        self.redis_client.hmset(image_id, image_data)

    def get_gallery_images_info(self):
        image_ids = self.redis_client.lrange('gallery', 0, -1)
        images_info = []

        for img_id in image_ids:
            image_data = self.redis_client.hgetall(img_id)
            image_info = {
                'image_url': url_for('static', filename='images/' + img_id.decode() + '.jpg'),
                'photo_name': image_data.get(b'photo_name', b'').decode(),
                'photo_date': image_data.get(b'photo_date', b'').decode(),
                'collection_name': image_data.get(b'collection_name', b'').decode()
            }
            images_info.append(image_info)

        return images_info

    def delete_image(self, image_id):
        # Remover o ID da imagem da lista de galeria
        self.redis_client.lrem('gallery', 0, image_id)

        # Excluir o hash associado à imagem
        self.redis_client.delete(image_id)
