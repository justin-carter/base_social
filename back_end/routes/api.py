from datetime import datetime, timedelta, timezone

from flask import Blueprint
from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, \
    unset_jwt_cookies, jwt_required

from back_end.services.post_service import create_post, post_react, post_report, get_post_comments, post_comment, \
    post_comment_react, report_comment
from back_end.services.user_service import authenticate_user, create_user, get_profile

api_bp = Blueprint('api', __name__)


@api_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    user_id = get_jwt_identity()
    response = get_profile(user_id)
    return response


@api_bp.route('/token', methods=['POST'])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    response = authenticate_user(email, password)
    return response


@api_bp.route('/signup', methods =['POST'])
def signup():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    response = create_user(email, password)
    return response


@api_bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@api_bp.route("/create-post", methods=["POST"])
@jwt_required()
def post_create():
    post_data = request.json.get("post_data", None)
    user_id = get_jwt_identity()
    response = create_post(post_data, user_id)
    return response


@api_bp.route("/post-react", methods=["POST"])
@jwt_required()
def react_post():
    post_id = request.json.get("post_id", None)
    reaction = request.json.get("reaction", None)
    user_id = get_jwt_identity()
    response = post_react(user_id, post_id, reaction)
    return response


@api_bp.route("/post-report", methods=["POST"])
@jwt_required()
def report_post():
    post_id = request.json.get("post_id", None)
    response = post_report(post_id)
    return response


@api_bp.route("/post-comments", methods=["GET"])
@jwt_required()
def post_comments():
    post_id = request.json.get("post_id", None)
    response = get_post_comments(post_id)
    return response


@api_bp.route("/post-comment", methods=["POST"])
@jwt_required()
def comment_post():
    user_id = get_jwt_identity()
    post_id = request.json.get("post_id", None)
    comment = request.json.get("comment", None)
    response = post_comment(user_id, post_id, comment)
    return response


@api_bp.route("/post-comment-react", methods=["POST"])
@jwt_required()
def comment_post_react():
    comment_id = request.json.get("comment_id", None)
    user_id = get_jwt_identity()
    reaction = request.json.get("reaction", None)
    response = post_comment_react(comment_id, user_id, reaction)
    return response


@api_bp.route("/comment-report", methods=["POST"])
@jwt_required()
def comment_report():
    comment_id = request.json.get("comment_id", None)
    response = report_comment(comment_id)
    return response


@api_bp.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response
