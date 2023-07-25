class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:12345@postgres:5432/wotp"
    SECRET_KEY = 'secret-key'
    SECURITY_FRESHNESS_GRACE_PERIOD = 3600
    SECURITY_DEFAULT_REMEMBER_ME = True
    SECURITY_REGISTERABLE = True


class DevEnvConfig(Config):
    DEBUG = True
    UPLOAD_FOLDER = 'photos'
    ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']
    SECRET_KEY = 'MYSECRETKEY!'
