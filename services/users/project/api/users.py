# services/users/project/api/users.py


from flask import Blueprint, jsonify, request, render_template, redirect

from project.api.models import User
from project import db
from sqlalchemy import exc


users_blueprint = Blueprint('users', __name__, template_folder='./templates')


@users_blueprint.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
        })


@users_blueprint.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()
    response_object = {
            'status': 'failed',
            'message': 'carga invalida.'
    }
    if not post_data:
        return jsonify(response_object), 400
    username = post_data.get('username')
    email = post_data.get('email')
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(username=username, email=email))
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'{email} ha sido agregado!'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'lo siento. el email ya existe.'
            return jsonify(response_object), 400
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(response_object), 400


@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    """Obtener detalles de usuario único """
    response_object = {
        'status': 'failed',
        'mensaje': 'El usuario no existe'
    }
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'active': user.active
                }
            }
            return jsonify(response_object), 200
        # return render_template('user.html', user=user)
    except ValueError:
        return jsonify(response_object), 404


@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    """Obteniendo todos los usuarios"""
    response_object = {
        'status': 'success',
        'data': {
            'users': [user.to_json() for user in User.query.all()]
        }
    }
    return jsonify(response_object), 200


@users_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        db.session.add(User(username=username, email=email))
        db.session.commit()
    users = User.query.all()
    return render_template('index.html', users=users)


@users_blueprint.route('/user', methods=['POST'])
def update_user():
    if request.method == 'POST':
        iduser = request.form['iduser']
        user = User.query.get(iduser)
        user.username = request.form['username']
        user.email = request.form['email']
        db.session.commit()
        return redirect('/', code=302)


@users_blueprint.route('/delete', methods=['POST'])
def delete_user():
    if request.method == 'POST':
        iduser = request.form['iduser']
        user = User.query.get(iduser)
        db.session.delete(user)
        db.session.commit()
        return redirect('/', code=302)
