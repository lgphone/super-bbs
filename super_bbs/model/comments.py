from datetime import datetime
from super_bbs.core.dbwrapper import BaseModal, db


class Comments(BaseModal):
    """
    comments 表
    """
    __tablename__ = 'super_bbs_comments'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(64), unique=True, index=True)
    topic_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    like_count = db.Column(db.Integer, default=0)
    available = db.Column(db.Boolean, default=1)
    time_create = db.Column(db.DateTime, default=datetime.now)
    time_modify = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class CommentThank(BaseModal):
    """
    comment 感谢关联表
    """
    __tablename__ = 'super_bbs_comment_like'

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, default=1)
    time_create = db.Column(db.DateTime, default=datetime.now)
    time_modify = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

