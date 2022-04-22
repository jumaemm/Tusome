import os
from tusome_pkg import create_app
from tusome_pkg import config

from dotenv import load_dotenv

load_dotenv()


app = create_app(os.getenv('FLASK_CONFIG'))


if __name__ == '__main__':
    app.run(debug=True)