from flask import Blueprint, make_response, abort
from flask import current_app, g
from .decorators import parse_plist_input_data

omdm_app = Blueprint('omdm_app', __name__)


@omdm_app.route('/', methods=['PUT'])
@parse_plist_input_data
def process():
    print(g.plist_data)