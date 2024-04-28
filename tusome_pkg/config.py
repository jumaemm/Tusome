import os 
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY') 
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    TUSOME_MAIL_SUBJECT_PREFIX = '[Tusome]'
    TUSOME_MAIL_SENDER = 'TUSOME Admin <tusome@example.com>'
    TUSOME_ADMIN = os.environ.get('TUSOME_ADMIN')
    PERMANENT_SESSION_LIFETIME = 3600
    @staticmethod
    def init_app(app):
        pass

#Additional configs for Development environment
class DevelopmentConfig(Config):
    DEBUG=True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, "instance//tusome-dev.sqlite")


#Additionsl configs for testing environment
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, "instance//tusome-test.sqlite")


#Additional configs for Production environment
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, "instance//tusome.sqlite")

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}