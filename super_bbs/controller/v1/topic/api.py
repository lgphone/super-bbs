from collections import defaultdict
from flask import session
from super_bbs.core.viewhandler import ApiViewHandler, LogicError
from super_bbs.model.topics import Topics, TopicAppends, TopicFav, TopicUpDown, TopicThank
from super_bbs.model.users import Users, UserFavUser
from super_bbs.model.tabs import Tabs, SubTabs
from super_bbs.model.comments import Comments, CommentThank
from super_bbs.utils import need_params, login_required


class TopicAPI(ApiViewHandler):
    @need_params('uid')
    def get(self):
        data = Topics.get_by_uid(self.input.uid).to_dict()
        data['user'] = Users.get_by_id(data['user_id']).to_dict()
        if data['last_reply_user_id']:
            data['last_reply_user'] = Users.get_by_id(data['last_reply_user_id']).to_dict()
        data['tab'] = Tabs.get_by_id(data['tab_id']).to_dict()
        data['sub_tab'] = SubTabs.get_by_id(data['sub_tab_id']).to_dict()
        data['appends'] = [i.to_dict() for i in TopicAppends.filter_by_query(topic_id=data['id'])]

        comment_objs = Comments.filter_by_query(topic_id=data['id'])
        data['comment_count'] = comment_objs.count()
        if data['comment_count'] < 100:
            comment_list = [i.to_dict() for i in comment_objs]
            for index, comment in enumerate(comment_list):
                comment['index'] = index + 1
        else:
            page_size = 50
            page = int(self.input.page) if self.input.page else 1
            comment_objs = comment_objs.offset((page - 1) * page_size).limit(page_size)
            comment_list = [i.to_dict() for i in comment_objs]
            for index, comment in enumerate(comment_list):
                comment['index'] = (page - 1) * page_size + index + 1

        comment_user_dict = {
            i.id: i.to_dict(remove_fields_list=['password'])
            for i in Users.query.filter(
                Users.id.in_(set(i['user_id'] for i in comment_list)),
                Users.available == 1
            )
        }
        for comment in comment_list:
            comment['user'] = comment_user_dict[comment['user_id']]
            comment['is_thank'] = False
        data['up_count'] = TopicUpDown.filter_by_query(topic_id=data['id'], action=True).count()
        data['down_count'] = TopicUpDown.filter_by_query(topic_id=data['id'], action=False).count()
        data['is_fav'] = False
        data['is_thank'] = False
        if session.get('user_info'):
            if TopicFav.filter_by_query(topic_id=data['id'], user_id=session['user_info']['id']).first():
                data['is_fav'] = True
            if TopicThank.filter_by_query(topic_id=data['id'], user_id=session['user_info']['id']).first():
                data['is_thank'] = True
            comment_thank_objs = CommentThank.query.filter(
                CommentThank.comment_id.in_(set([i['id'] for i in comment_list])),
                CommentThank.available == 1
            )
            comment_thank_id_list = [i.comment_id for i in comment_thank_objs]
            for comment in comment_list:
                if comment['id'] in comment_thank_id_list:
                    comment['is_thank'] = True
        data['comments'] = comment_list
        return data

    @login_required()
    @need_params(*['title', 'sub_tab_id'])
    def post(self):
        obj = Topics.create_by_uid()
        obj.title = self.input.title
        sub_tab_obj = SubTabs.get_by_id(self.input.sub_tab_id)
        obj.sub_tab_id = self.input.sub_tab_id
        tab_obj = Tabs.get_by_id(sub_tab_obj.tab_id)
        obj.tab_id = tab_obj.id

        if self.input.content:
            obj.content = self.input.content
            obj.content_length = len(self.input.content)
        obj.user_id = session['user_info']['id']
        obj.save()


class TopicUpDownCountAPI(ApiViewHandler):
    @login_required()
    @need_params(*['uid', 'action'])
    def post(self):
        obj = Topics.get_by_uid(self.input.uid)
        if self.input.action in ['up', 'down']:
            topic_up_down_obj = TopicUpDown.filter_by_query(
                topic_id=obj.id,
                user_id=session['user_info']['id'],
                show_deleted=True
            ).first()
            if topic_up_down_obj:
                topic_up_down_obj.available = 1
            else:
                topic_up_down_obj = TopicUpDown()
                topic_up_down_obj.topic_id = obj.id
                topic_up_down_obj.user_id = session['user_info']['id']
            if self.input.action == 'up':
                topic_up_down_obj.action = True
            else:
                topic_up_down_obj.action = False
            topic_up_down_obj.save()

        return {
            'up_count': TopicUpDown.filter_by_query(topic_id=obj.id, action=True).count(),
            'down_count': TopicUpDown.filter_by_query(topic_id=obj.id, action=False).count()
        }


class TopicAppendAPI(ApiViewHandler):
    @login_required()
    @need_params(*['uid', 'content'])
    def post(self):
        obj = Topics.get_by_uid(self.input.uid)
        if obj.user_id != session['user_info']['id']:
            raise LogicError('你不可以追加别人的帖子哦')
        append_obj = TopicAppends.create_by_uid()
        append_obj.topic_id = obj.id
        append_obj.content = self.input.content
        append_obj.save()


class TopicAddView(ApiViewHandler):
    @need_params(*['uid'])
    def post(self):
        obj = Topics.get_by_uid(self.input.uid)
        obj.view_count += 1
        obj.save()


class TopicCommentAPI(ApiViewHandler):
    @login_required()
    @need_params(*['uid', 'comment'])
    def post(self):
        obj = Topics.get_by_uid(self.input.uid)
        commend_obj = Comments.create_by_uid()
        commend_obj.topic_id = obj.id
        commend_obj.content = self.input.comment
        commend_obj.user_id = session['user_info']['id']
        obj.last_reply_user_id = session['user_info']['id']
        obj.last_reply_time = self.get_datetime_now()
        obj.save()
        commend_obj.save()


class TopicFavAPI(ApiViewHandler):
    @login_required()
    def get(self):
        topic_fav_objs = TopicFav.filter_by_query(user_id=session['user_info']['id'])
        topic_fav_count = topic_fav_objs.count()
        if topic_fav_count > 100:
            page = int(self.input.page) if self.input.page else 1
            page_size = 50
            topic_fav_objs = topic_fav_objs.order_by(
                TopicFav.time_modify.desc()
            ).order_by(TopicFav.id.desc()).offset((page - 1) * page_size).limit(page_size)
        else:
            topic_fav_objs = topic_fav_objs.order_by(TopicFav.time_modify.desc()).order_by(TopicFav.id.desc())

        topic_fav_dict = {i.topic_id: i.time_modify.strftime('%Y-%m-%d %H:%M:%S') for i in topic_fav_objs}
        topic_id_list = topic_fav_dict.keys()
        topic_objs = Topics.query.filter(Topics.id.in_(set(topic_id_list)), Topics.available == 1)
        topic_list = [_t.to_dict() for _t in topic_objs]
        for topic in topic_list:
            topic['fav_time'] = topic_fav_dict[topic['id']]
        # 排序
        filtered_topic_id_list = [i['id'] for i in topic_list]
        topic_id_sort_dict = {
            value: index
            for index, value in enumerate(topic_id_list) if value in filtered_topic_id_list
        }
        topic_list = sorted(topic_list, key=lambda x: topic_id_sort_dict[x['id']])

        user_dict = {
            i.id: i.to_dict(remove_fields_list=['password'])
            for i in Users.query.filter(Users.id.in_(set(i['user_id'] for i in topic_list)), Users.available == 1)
        }
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
            _t['user'] = user_dict[_t['user_id']]
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

        return {'total': topic_fav_count, 'list': topic_list}

    @login_required()
    @need_params(*['uid', 'action'])
    def post(self):
        obj = Topics.get_by_uid(self.input.uid)
        if session['user_info']['id'] == obj.user_id:
            raise LogicError('自己不能收藏自己的主题哦')
        topic_fav_obj = TopicFav.filter_by_query(
            topic_id=obj.id,
            user_id=session['user_info']['id'],
            show_deleted=True
        ).first()
        if self.input.action == 'add':
            if topic_fav_obj:
                topic_fav_obj.available = 1
            else:
                topic_fav_obj = TopicFav()
                topic_fav_obj.topic_id = obj.id
                topic_fav_obj.user_id = session['user_info']['id']
            topic_fav_obj.save()
        elif self.input.action == 'cal':
            if topic_fav_obj:
                topic_fav_obj.available = 0
                topic_fav_obj.save()


class TopicThankAPI(ApiViewHandler):
    @login_required()
    @need_params(*['uid'])
    def post(self):
        obj = Topics.get_by_uid(self.input.uid)
        # 自己不能给自己感谢
        if session['user_info']['id'] == obj.user_id:
            raise LogicError('自己不能感谢自己哦')
        if not TopicThank.filter_by_query(topic_id=obj.id, user_id=session['user_info']['id']).first():
            thank_obj = TopicThank()
            thank_obj.topic_id = obj.id
            thank_obj.user_id = session['user_info']['id']
            thank_obj.save()


class CommentThankAPI(ApiViewHandler):
    @login_required()
    @need_params(*['uid'])
    def post(self):
        obj = Comments.get_by_uid(self.input.uid)
        # 自己不能给自己点赞
        if session['user_info']['id'] == obj.user_id:
            raise LogicError('自己不能给自己点赞哦')
        if not CommentThank.filter_by_query(comment_id=obj.id, user_id=session['user_info']['id']).first():
            thank_obj = CommentThank()
            thank_obj.comment_id = obj.id
            thank_obj.user_id = session['user_info']['id']
            thank_obj.save()


class UserFavAPI(ApiViewHandler):
    @login_required()
    def get(self):
        fav_user_id_list = [
            i.fav_user_id
            for i in UserFavUser.filter_by_query(user_id=session['user_info']['id'])
        ]
        fav_user_list = [
            i.to_dict()
            for i in Users.query.filter(Users.id.in_(set(fav_user_id_list)), Users.available == 1)
        ]
        topic_objs = Topics.query.filter(Topics.user_id.in_(set(fav_user_id_list)), Topics.available == 1)
        topic_count = topic_objs.count()
        if topic_count > 100:
            page = int(self.input.page) if self.input.page else 1
            page_size = 50
            topic_objs = topic_objs.order_by(
                Topics.time_create.desc()
            ).order_by(Topics.id.desc()).offset((page - 1) * page_size).limit(page_size)
        else:
            topic_objs = topic_objs.order_by(Topics.time_modify.desc()).order_by(Topics.id.desc())
        topic_list = [_t.to_dict() for _t in topic_objs]

        user_dict = {
            i.id: i.to_dict(remove_fields_list=['password'])
            for i in Users.query.filter(Users.id.in_(set(i['user_id'] for i in topic_list)), Users.available == 1)
        }
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
            _t['user'] = user_dict[_t['user_id']]
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

        return {'total': topic_count, 'list': topic_list, 'fav_users': fav_user_list}

    @login_required()
    @need_params(*['uid', 'action'])
    def post(self):
        obj = Users.get_by_uid(self.input.uid)
        # 自己不能关注自己
        if session['user_info']['uid'] == obj.uid:
            raise LogicError('自己不能关注自己哦')
        if self.input.action == 'add':
            user_fav_obj = UserFavUser.filter_by_query(
                fav_user_id=obj.id,
                user_id=session['user_info']['id'],
                show_deleted=True
            ).first()
            if user_fav_obj:
                user_fav_obj.available = 1
            else:
                user_fav_obj = UserFavUser()
                user_fav_obj.fav_user_id = obj.id
                user_fav_obj.user_id = session['user_info']['id']
            user_fav_obj.save()
        elif self.input.action == 'cal':
            user_fav_obj = UserFavUser.filter_by_query(
                fav_user_id=obj.id,
                user_id=session['user_info']['id']
            ).first()
            if user_fav_obj:
                user_fav_obj.available = 0
                user_fav_obj.save()
