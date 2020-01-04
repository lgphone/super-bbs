from flask import session, current_app
from super_bbs.core.viewhandler import ApiViewHandler
from super_bbs.model.users import Users, Passport, UserFavUser
from super_bbs.model.topics import TopicFav
from super_bbs.model.tabs import SubTabFav
from super_bbs.utils import need_params, login_required
from .wrapper import check_login


class LoginAPI(ApiViewHandler):
    @need_params(*['username', 'password'])
    def post(self):
        user_obj = check_login(username=self.input.username, password=self.input.password)
        user_dict = user_obj.to_dict(remove_fields_list=['password'])
        session['is_login'] = True
        session['role_id'] = user_dict['role_id']
        session['user_info'] = user_dict
        # add token to passport
        passport = Passport.create_or_update(
            query_dict={'user_id': user_obj.id},
            update_dict={'token': session.sid}
        )
        passport.expire = self.get_datetime_now() + current_app.config['REMEMBER_COOKIE_DURATION']
        passport.save()

        return user_dict


class LoginOutAPI(ApiViewHandler):
    @login_required(admin=True)
    def get(self):
        session.clear()

    def post(self):
        return self.get()


class LoginStatusCheck(ApiViewHandler):
    def get(self):
        user_info = session.get('user_info')
        if user_info:
            user_obj = Users.get_by_id(user_info['id'])
            user_dict = user_obj.to_dict(remove_fields_list=['password'])
            user_dict['fav_sub_tab_count'] = SubTabFav.filter_by_query(user_id=user_dict['id']).count()
            user_dict['fav_topic_count'] = TopicFav.filter_by_query(user_id=user_dict['id']).count()
            user_dict['fav_user_count'] = UserFavUser.filter_by_query(user_id=user_dict['id']).count()
            session['user_info'] = user_dict
            return user_dict


class ProfileAPI(ApiViewHandler):
    @login_required(admin=True)
    def get(self):
        user_obj = Users.get_by_id(session['user_info']['id'])
        user_dict = user_obj.to_dict(remove_fields_list=['password'])
        user_dict['fav_sub_tab_count'] = SubTabFav.filter_by_query(user_id=user_dict['id']).count()
        user_dict['fav_topic_count'] = TopicFav.filter_by_query(user_id=user_dict['id']).count()
        user_dict['fav_user_count'] = UserFavUser.filter_by_query(user_id=user_dict['id']).count()
        session['user_info'] = user_dict
        return user_dict

    @login_required(admin=True)
    def post(self):
        user_info = session.get('user_info')
        user_obj = Users.get_by_uid(user_info['uid'])

        update_dict = dict()

        for k in ['sex', 'avatar_url', 'site', 'location', 'company', 'github', 'twitter', 'weibo', 'bio']:
            if getattr(self.input, k) is not None:
                update_dict[k] = getattr(self.input, k)
        if self.input.sex in [0, 1, 2]:
            update_dict['sex'] = self.input.sex

        if self.input.privacy_level in [0, 1, 2]:
            update_dict['privacy_level'] = self.input.privacy_level

        user_obj.update(**update_dict)
        user_info.update(update_dict)
        session['user_info'] = user_info

        return user_info
