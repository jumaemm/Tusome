import os
from flask import Flask
from tusome_pkg.auth import bp as auth_bp
from tusome_pkg.site import bp as site_bp

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'tusome.sqlite'),
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
    app.add_url_rule('/', endpoint='home_page')
    #@app.route('/hello')
    #def hello():
    #    return render_template('site/home.html')
    return app