from flask import Blueprint
bp = Blueprint('auth',__name__)
from tusome_pkg.auth import routes
