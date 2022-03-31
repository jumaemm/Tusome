import os
from flask import Flask
from tusome_pkg.auth import bp as auth_bp
from tusome_pkg.site import bp as site_bp
from tusome_pkg.models import db

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='8549c630be55c1f8d724e4dc',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(BASE_DIR, "instance//tusome.db") ,
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    app.register_blueprint(auth_bp,url_prefix='/auth')
    app.register_blueprint(site_bp)
    app.add_url_rule('/', endpoint='site.home_page')
    from tusome_pkg.models import User, Book, Review
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app