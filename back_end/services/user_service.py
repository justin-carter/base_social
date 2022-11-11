import logging
import uuid
from flask import make_response, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from back_end.models.models import User, db

log = logging.getLogger()


def get_profile(user_id):
    user = User.query.filter_by(id=user_id).first()

    return jsonify({'email': user.email})


def create_user(email, password):
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(
            public_id=str(uuid.uuid4()),
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()

        return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)


def authenticate_user(email, password):
    if not email or not password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Login missing!'})

    user = User.query.filter_by(email=email).first()

    if not user:
        log.debug('User not found with email={}'.format(email))
        return make_response('Could not verify', 403, {'WWW-Authenticate': 'Login failed!"'})

    if check_password_hash(user.password, password):
        log.info('User authenticated with email={}'.format(email))
        access_token = create_access_token(identity=user.id)
        response = {"access_token": access_token}
        return response
    else:
        log.debug('Password incorrect for user={}'.format(email))
        return make_response('Could not verify', 403, {'WWW-Authenticate': 'Login failed!"'})
