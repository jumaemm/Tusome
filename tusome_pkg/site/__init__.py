from flask import Blueprint
bp = Blueprint('site',__name__, template_folder='templates')
from tusome_pkg.site import routes