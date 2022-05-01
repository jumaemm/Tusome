
from flask import Flask
from tusome_pkg.auth import bp as auth_bp
from tusome_pkg.site import bp as site_bp
from tusome_pkg.models import db
from flask_login import LoginManager
from tusome_pkg.config import config



def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.register_blueprint(auth_bp,url_prefix='/auth')
    app.register_blueprint(site_bp)
    app.add_url_rule('/', endpoint='site.home_page')
    from tusome_pkg.models import User, Book, Review, Role
    db.init_app(app)
    with app.app_context():
        db.create_all()
        Role.insert_roles()
    login_manager = LoginManager(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    return app