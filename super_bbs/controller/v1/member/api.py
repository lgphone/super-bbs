from collections import defaultdict
from flask import session
from super_bbs.core.viewhandler import ApiViewHandler, LogicError
from super_bbs.model.tabs import Tabs, SubTabs
from super_bbs.model.topics import Topics, TopicUpDown
from super_bbs.model.comments import Comments, CommentThank
from super_bbs.model.users import Users, UserFavUser
from super_bbs.utils import need_params, login_required


class MemberIndexAPI(ApiViewHandler):
    @need_params('username')
    def get(self):
        data = dict()
        user_info = Users.get_by_query(username=self.input.username).to_dict(remove_fields_list=['password'])
        user_info['fav_user_count'] = UserFavUser.filter_by_query(user_id=user_info['id']).count()
        user_info['be_fav_user_count'] = UserFavUser.filter_by_query(fav_user_id=user_info['id']).count()
        data['user'] = user_info
        data['is_open'] = True
        data['is_fav'] = False
        if session.get('is_login'):
            if UserFavUser.filter_by_query(user_id=session['user_info']['id'], fav_user_id=user_info['id']).first():
                data['is_fav'] = True

        comment_list = [
            i.to_dict()
            for i in Comments.filter_by_query(user_id=user_info['id']).order_by(Comments.time_create.desc())[:10]
        ]
        comment_topic_dict = {
            i.id: i.to_dict()
            for i in Topics.query.filter(
                Topics.id.in_(set([i['topic_id'] for i in comment_list])),
                Topics.available == 1
            )
        }
        comment_topic_list = [i for i in comment_topic_dict.values()]
        user_dict = {
            i.id: i.to_dict(remove_fields_list=['password'])
            for i in Users.query.filter(
                Users.id.in_(set(i['user_id'] for i in comment_topic_list)),
                Users.available == 1
            )
        }
        tab_dict = {
            i.id: i.to_dict()
            for i in Tabs.query.filter(
                Tabs.id.in_(set(i['tab_id'] for i in comment_topic_list)),
                Tabs.available == 1
            )
        }
        sub_tab_dict = {
            i.id: i.to_dict()
            for i in SubTabs.query.filter(
                SubTabs.id.in_(set(i['sub_tab_id'] for i in comment_topic_list)),
                SubTabs.available == 1
            )
        }
        for topic in comment_topic_list:
            comment_topic_dict[topic['id']]['user'] = user_dict[topic['user_id']]
            comment_topic_dict[topic['id']]['tab'] = tab_dict[topic['tab_id']]
            comment_topic_dict[topic['id']]['sub_tab'] = sub_tab_dict[topic['sub_tab_id']]

        for comment in comment_list:
            comment['is_thank'] = False
            comment['topic'] = comment_topic_dict[comment['topic_id']]

        if session.get('user_info'):
            comment_thank_id_list = [i.comment_id for i in
                                     CommentThank.filter_by_query(user_id=session['user_info']['id'])]
            for comment in comment_list:
                if comment['id'] in comment_thank_id_list:
                    comment['is_thank'] = True
        data['comments'] = comment_list

        if user_info['privacy_level'] == 1 and not session.get('is_login'):
            data['is_open'] = False
            data['topics'] = []
            return data

        if user_info['privacy_level'] == 2:
            if not session.get('user_info') or session.get('user_info')['id'] != user_info['id']:
                data['is_open'] = False
                data['topics'] = []
                return data

        topic_list = [
            i.to_dict()
            for i in Topics.filter_by_query(user_id=user_info['id']).order_by(Topics.time_create.desc())[:10]
        ]
        last_reply_user_dict = {
            i.id: i.to_dict(remove_fields_list=['password'])
            for i in Users.query.filter(
                Users.id.in_(set(i['last_reply_user_id'] for i in topic_list)),
                Users.available == 1
            )
        }
        tab_dict = {
            i.id: i.to_dict()
            for i in Tabs.query.filter(Tabs.id.in_(set(i['tab_id'] for i in topic_list)), Tabs.available == 1)
        }
        sub_tab_dict = {
            i.id: i.to_dict()
            for i in SubTabs.query.filter(
                SubTabs.id.in_(set(i['sub_tab_id'] for i in topic_list)),
                SubTabs.available == 1
            )
        }
        comment_count_dict = dict()
        for c in Comments.query.filter(
                Comments.topic_id.in_(set(i['id'] for i in topic_list)),
                Comments.available == 1
        ):
            if comment_count_dict.get(c.topic_id):
                comment_count_dict[c.topic_id] += 1
            else:
                comment_count_dict[c.topic_id] = 1

        up_down_dict_list = defaultdict(list)
        for up_down_obj in TopicUpDown.query.filter(
                TopicUpDown.topic_id.in_(set(i['id'] for i in topic_list)),
                TopicUpDown.available == 1
        ):
            up_down_dict_list[up_down_obj.topic_id].append(up_down_obj.action)

        for _t in topic_list:
            if _t['last_reply_user_id']:
                _t['last_reply_user'] = last_reply_user_dict[_t['last_reply_user_id']]
            _t['tab'] = tab_dict[_t['tab_id']]
            _t['sub_tab'] = sub_tab_dict[_t['sub_tab_id']]
            _t['comment_count'] = comment_count_dict.get(_t['id'], 0)
            # 获取up和down数量
            if up_down_dict_list.get(_t['id']):
                _t['up_count'] = len([i for i in up_down_dict_list[_t['id']] if i is True])
                _t['down_count'] = len([i for i in up_down_dict_list[_t['id']] if i is False])
            else:
                _t['up_count'] = 0
                _t['down_count'] = 0
        data['topics'] = topic_list

        return data


class MemberTopicAPI(ApiViewHandler):
    @need_params('username')
    def get(self):
        data = dict()
        user_info = Users.get_by_query(username=self.input.username).to_dict(remove_fields_list=['password'])
        data['user'] = user_info

        if user_info['privacy_level'] == 1 and not session.get('is_login'):
            raise LogicError('没有权限访问此用户的信息哦')

        if user_info['privacy_level'] == 2:
            if not session.get('user_info') or session.get('user_info')['id'] != user_info['id']:
                raise LogicError('没有权限访问此用户的信息哦')

        topic_objs = Topics.filter_by_query(user_id=user_info['id'])
        topic_count = topic_objs.count()
        data['total'] = topic_count
        if topic_count > 100:
            page = int(self.input.page) if self.input.page else 1
            page_size = 50
            topic_objs = topic_objs.order_by(
                Topics.time_create.desc()
            ).order_by(Topics.id.desc()).offset((page - 1) * page_size).limit(page_size)
        else:
            topic_objs = topic_objs.order_by(Topics.time_modify.desc()).order_by(Topics.id.desc())
        topic_list = [_t.to_dict() for _t in topic_objs]

        last_reply_user_dict = {
            i.id: i.to_dict(remove_fields_list=['password'])
            for i in Users.query.filter(
                Users.id.in_(set(i['last_reply_user_id'] for i in topic_list)),
                Users.available == 1
            )
        }
        tab_dict = {
            i.id: i.to_dict()
            for i in Tabs.query.filter(Tabs.id.in_(set(i['tab_id'] for i in topic_list)), Tabs.available == 1)
        }
        sub_tab_dict = {
            i.id: i.to_dict()
            for i in SubTabs.query.filter(
                SubTabs.id.in_(set(i['sub_tab_id'] for i in topic_list)),
                SubTabs.available == 1
            )
        }
        comment_count_dict = dict()
        for c in Comments.query.filter(
                Comments.topic_id.in_(set(i['id'] for i in topic_list)),
                Comments.available == 1
        ):
            if comment_count_dict.get(c.topic_id):
                comment_count_dict[c.topic_id] += 1
            else:
                comment_count_dict[c.topic_id] = 1

        up_down_dict_list = defaultdict(list)
        for up_down_obj in TopicUpDown.query.filter(
                TopicUpDown.topic_id.in_(set(i['id'] for i in topic_list)),
                TopicUpDown.available == 1
        ):
            up_down_dict_list[up_down_obj.topic_id].append(up_down_obj.action)

        for _t in topic_list:
            if _t['last_reply_user_id']:
                _t['last_reply_user'] = last_reply_user_dict[_t['last_reply_user_id']]
            _t['tab'] = tab_dict[_t['tab_id']]
            _t['sub_tab'] = sub_tab_dict[_t['sub_tab_id']]
            _t['comment_count'] = comment_count_dict.get(_t['id'], 0)
            # 获取up和down数量
            if up_down_dict_list.get(_t['id']):
                _t['up_count'] = len([i for i in up_down_dict_list[_t['id']] if i is True])
                _t['down_count'] = len([i for i in up_down_dict_list[_t['id']] if i is False])
            else:
                _t['up_count'] = 0
                _t['down_count'] = 0
        data['list'] = topic_list

        return data


class MemberCommentAPI(ApiViewHandler):
    @need_params('username')
    def get(self):
        data = dict()
        user_info = Users.get_by_query(username=self.input.username).to_dict(remove_fields_list=['password'])
        data['user'] = user_info
        comment_objs = Comments.filter_by_query(user_id=user_info['id'])
        comment_count = comment_objs.count()
        data['total'] = comment_count

        if comment_count > 100:
            page = int(self.input.page) if self.input.page else 1
            page_size = 50
            topic_objs = comment_objs.order_by(
                Comments.time_create.desc()
            ).order_by(Comments.id.desc()).offset((page - 1) * page_size).limit(page_size)
        else:
            topic_objs = comment_objs.order_by(Comments.time_modify.desc()).order_by(Comments.id.desc())
        comment_list = [_t.to_dict() for _t in topic_objs]

        comment_topic_dict = {
            i.id: i.to_dict()
            for i in Topics.query.filter(
                Topics.id.in_(set([i['topic_id'] for i in comment_list])),
                Topics.available == 1
            )
        }
        comment_topic_list = [i for i in comment_topic_dict.values()]
        user_dict = {
            i.id: i.to_dict(remove_fields_list=['password'])
            for i in Users.query.filter(
                Users.id.in_(set(i['user_id'] for i in comment_topic_list)),
                Users.available == 1
            )
        }
        tab_dict = {
            i.id: i.to_dict()
            for i in Tabs.query.filter(
                Tabs.id.in_(set(i['tab_id'] for i in comment_topic_list)),
                Tabs.available == 1
            )
        }
        sub_tab_dict = {
            i.id: i.to_dict()
            for i in SubTabs.query.filter(
                SubTabs.id.in_(set(i['sub_tab_id'] for i in comment_topic_list)),
                SubTabs.available == 1
            )
        }
        for topic in comment_topic_list:
            comment_topic_dict[topic['id']]['user'] = user_dict[topic['user_id']]
            comment_topic_dict[topic['id']]['tab'] = tab_dict[topic['tab_id']]
            comment_topic_dict[topic['id']]['sub_tab'] = sub_tab_dict[topic['sub_tab_id']]

        for comment in comment_list:
            comment['is_thank'] = False
            comment['topic'] = comment_topic_dict[comment['topic_id']]

        if session.get('user_info'):
            comment_thank_id_list = [i.comment_id for i in
                                     CommentThank.filter_by_query(user_id=session['user_info']['id'])]
            for comment in comment_list:
                if comment['id'] in comment_thank_id_list:
                    comment['is_thank'] = True

        data['list'] = comment_list

        return data
