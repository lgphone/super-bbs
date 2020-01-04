from datetime import datetime
from super_bbs.core.dbwrapper import BaseModal, db


class Topics(BaseModal):
    """
    topics 表
    """
    __tablename__ = 'super_bbs_topics'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(64), unique=True, index=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text(16000))
    content_length = db.Column(db.Integer)
    tab_id = db.Column(db.Integer, nullable=False)
    sub_tab_id = db.Column(db.Integer, nullable=False)
    last_reply_user_id = db.Column(db.Integer)
    last_reply_time = db.Column(db.DateTime)
    view_count = db.Column(db.Integer, default=0)
    available = db.Column(db.Boolean, default=1)
    time_create = db.Column(db.DateTime, default=datetime.now)
    time_modify = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class TopicAppends(BaseModal):
    """
    topic 的append表
    """
    __tablename__ = 'super_bbs_topic_appends'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(64), unique=True, index=True)
    topic_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text(16000), nullable=False)
    available = db.Column(db.Boolean, default=1)
    time_create = db.Column(db.DateTime, default=datetime.now)
    time_modify = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class TopicFav(BaseModal):
    """
    topic 收藏表
    """
    __tablename__ = 'super_bbs_topic_fav'

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, default=1)
    time_create = db.Column(db.DateTime, default=datetime.now)
    time_modify = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class TopicThank(BaseModal):
    """
    topic 感谢关联表
    """
    __tablename__ = 'super_bbs_topic_like'

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, default=1)
    time_create = db.Column(db.DateTime, default=datetime.now)
    time_modify = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class TopicUpDown(BaseModal):
    """
    topic 点up和点down统计
    """
    __tablename__ = 'super_bbs_topic_up_down'

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.Boolean, nullable=False)
    available = db.Column(db.Boolean, default=1)
    time_create = db.Column(db.DateTime, default=datetime.now)
    time_modify = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Tags(BaseModal):
    """
    tag 表
    """
    __tablename__ = 'super_bbs_tags'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(256), nullable=False)
    available = db.Column(db.Boolean, default=1)
    time_create = db.Column(db.DateTime, default=datetime.now)
    time_modify = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class TopicToTag(BaseModal):
    """
    topic 关联 tag 表
    """
    __tablename__ = 'super_bbs_topic_to_tag'

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, nullable=False)
    tag_id = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, default=1)
    time_create = db.Column(db.DateTime, default=datetime.now)
    time_modify = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
