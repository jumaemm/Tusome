import os
from tusome_pkg import create_app
from tusome_pkg.config import Config

from dotenv import load_dotenv

load_dotenv()


app = create_app(os.getenv('FLASK_CONFIG'))
app.permanent_session_lifetime = Config.PERMANENT_SESSION_LIFETIME

if __name__ == '__main__':
    app.run(debug=True)