import os


class Config:
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/images')
    DEBUG = True  # Ativar o modo de depuração


class RedisConfig:
    HOST = 'localhost'
    PORT = 6379
    PASSWORD = 'qwert'  # Substitua pela senha do seu Redis
    DB = 0
