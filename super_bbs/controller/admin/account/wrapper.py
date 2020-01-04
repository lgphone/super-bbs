from super_bbs.model.users import Users
from super_bbs.core.basehandler import AuthError


def check_login(username, password):
    user_obj = Users.filter_by_query(username=username).first()
    if not user_obj:
        raise AuthError("用户不存在")
    if not user_obj.check_password(password):
        raise AuthError("密码错误")
    if not user_obj.status:
        raise AuthError("账户已经停用")
    if user_obj.role_id != 1:
        raise AuthError("认证失败,账户不是超管")
    return user_obj
