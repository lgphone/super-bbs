from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from super_bbs.core.dbwrapper import BaseModal, db
from super_bbs.constants import default_password


class Users(BaseModal):
    """
    用户表
    """
    __tablename__ = 'super_bbs_users'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    sex = db.Column(db.Integer, default=0)
    avatar_url = db.Column(db.String(32))
    role_id = db.Column(db.Integer, default=0)  # role_id 是否是管理员或者其他权限 0是一般用户 1 管理员用户
    site = db.Column(db.String(256))
    location = db.Column(db.String(256))
    company = db.Column(db.String(256))
    github = db.Column(db.String(256))
    twitter = db.Column(db.String(256))
    weibo = db.Column(db.String(256))
    bio = db.Column(db.String(512))
    privacy_level = db.Column(db.Integer, default=0)  # 0 所有人可以查看我的回复 我的主题 1 只有登录的人可以查看 2 只有自己可以查看
    status = db.Column(db.Boolean, default=1)
    available = db.Column(db.Boolean, default=1)
    time_create = db.Column(db.DateTime, default=datetime.now)
    time_modify = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def reset_password(self):
        return self.set_password(default_password)


class Passport(BaseModal):
    """
    用户session id
    """
    __tablename__ = 'super_bbs_passports'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    data = db.Column(db.String(256))
    token = db.Column(db.String(64), nullable=False)
    expire = db.Column(db.DateTime)
    time_create = db.Column(db.DateTime, default=datetime.now)
    time_modify = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class UserFavUser(BaseModal):
    """
    user user 收藏关联表
    """
    __tablename__ = 'super_bbs_user_fav_user'

    id = db.Column(db.Integer, primary_key=True)
    fav_user_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, default=1)
    time_create = db.Column(db.DateTime, default=datetime.now)
    time_modify = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class CeleryTaskLogs(BaseModal):
    """
    Celery 任务记录
    """
    __tablename__ = 'super_bbs_celery_task_logs'

    success_status = 1
    fail_status = 0

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(128))
    task_id = db.Column(db.String(64), index=True, unique=True)
    retval = db.Column(db.Text)
    done = db.Column(db.Boolean)
    task_status = db.Column(db.Boolean)
    exc = db.Column(db.Text)
    einfo = db.Column(db.Text)
    args = db.Column(db.Text)
    kwargs = db.Column(db.Text)
    available = db.Column(db.Boolean, default=1)
    time_done = db.Column(db.DateTime)
    time_create = db.Column(db.DateTime, default=datetime.now)
    time_modify = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
