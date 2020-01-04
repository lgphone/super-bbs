from datetime import datetime
from super_bbs.core.dbwrapper import BaseModal, db


class Tabs(BaseModal):
    """
    tab 表
    """
    __tablename__ = 'super_bbs_tabs'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    zh = db.Column(db.String(128), nullable=False, unique=True)
    sort_num = db.Column(db.Integer, default=100)
    available = db.Column(db.Boolean, default=1)
    time_create = db.Column(db.DateTime, default=datetime.now)
    time_modify = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class SubTabs(BaseModal):
    """
    tab 子表
    """
    __tablename__ = 'super_bbs_sub_tabs'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(64), unique=True, index=True)
    tab_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(128), nullable=False, unique=True)
    zh = db.Column(db.String(128), nullable=False, unique=True)
    desc = db.Column(db.String(256))
    sort_num = db.Column(db.Integer, default=100)
    available = db.Column(db.Boolean, default=1)
    time_create = db.Column(db.DateTime, default=datetime.now)
    time_modify = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class SubTabFav(BaseModal):
    """
    tab user 收藏关联表
    """
    __tablename__ = 'super_bbs_sub_tab_fav'

    id = db.Column(db.Integer, primary_key=True)
    sub_tab_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, default=1)
    time_create = db.Column(db.DateTime, default=datetime.now)
    time_modify = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)