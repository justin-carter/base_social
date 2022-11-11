import uuid
from flask import make_response, jsonify
from back_end.helpers.constants import Reaction
from back_end.models.models import Post, db, PostComment, User, UserPostReact


def create_post(post_data, user_id):
    post = Post(
        public_id=str(uuid.uuid4()),
        user_id=user_id,
        content=post_data['content'],
        tags=post_data['tags'].replace(' ', '')
    )
    db.session.add(post)
    db.session.commit()

    return make_response('Successfully created post.', 201)


def get_post_buffer(num_posts):
    """
    get a buffer of n posts
    """
    pass


def post_react(user_id, post_id, reaction):
    post = Post.query.filter_by(id=post_id).first()

    if reaction == Reaction.positive:
        post.pos_reaction += 1
        user_react = Reaction.positive
    else:
        post.neg_reaction += 1
        user_react = Reaction.negative

    user_post_react = UserPostReact(
        user_id=user_id,
        post_id=post_id,
        reaction=user_react
    )
    db.session.add(user_post_react)

    db.session.commit()

    return make_response('Successfully reacted to post.', 200)


def post_report(post_id):
    post = Post.query.filter_by(id=post_id).first()

    post.report_count += 1

    db.session.commit()

    return make_response('Successfully reported post.', 200)


def get_post_comments(post_id):
    post_comments = db.session.query(PostComment.id, PostComment.comment, User.id).filter_by(post_id=post_id)\
                                    .join(User, User.id == PostComment.user_id).all()

    comments = []

    for pc in post_comments:
        comments.append({
            'id': pc[0],
            'comment': pc[1],
            'user_id': pc[2]
        })

    return jsonify(comments)


def post_comment(user_id, post_id, comment):
    post_comment = PostComment(
        public_id=str(uuid.uuid4()),
        user_id=user_id,
        post_id=post_id,
        comment=comment
    )
    db.session.add(post_comment)
    db.session.commit()

    return make_response('Successfully added comment to post.', 201)


def post_comment_react(comment_id, user_id, reaction):
    post_comment = PostComment.query.filter_by(id=comment_id).first()

    if reaction == Reaction.positive:
        post_comment.pos_reaction += 1
    else:
        post_comment.neg_reaction += 1

    db.session.commit()

    return make_response('Successfully reacted to comment.', 200)


def report_comment(comment_id):
    post_comment = PostComment.query.filter_by(id=comment_id).first()

    post_comment.report_count += 1

    db.session.commit()

    return make_response('Successfully reported comment.', 200)