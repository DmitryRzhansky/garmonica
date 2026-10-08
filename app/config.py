import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-nova-clinic")
    JSON_AS_ASCII = False
