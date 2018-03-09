from flask import Blueprint,jsonify
wind_data = Blueprint(
    'wind_data',
    __name__,
    url_prefix="/wind_data"
)

@wind_data.route('/',methods=('GET', 'POST'))
def func():
    return 1