from flask import Blueprint,jsonify
database_update = Blueprint(
    'database_update',
    __name__,
    url_prefix="/database_update"
)

@database_update.route('/',methods=('GET', 'POST'))
def func():
    return 0