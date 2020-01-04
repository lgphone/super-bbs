from collections import defaultdict
from flask import session
from super_bbs.core.viewhandler import ApiViewHandler
from super_bbs.model.tabs import Tabs, SubTabs, SubTabFav
from super_bbs.model.topics import Topics, TopicUpDown
from super_bbs.model.comments import Comments
from super_bbs.model.users import Users
from super_bbs.utils import need_params, login_required


class TabAPI(ApiViewHandler):
    def get(self):
        sub_tab_dict_list = defaultdict(list)
        for sub_tab in SubTabs.filter_by_query().order_by(SubTabs.sort_num.asc()):
            sub_tab_dict_list[sub_tab.tab_id].append(sub_tab.to_dict())
        tab_list = [t.to_dict() for t in Tabs.filter_by_query().order_by(Tabs.sort_num.asc())]
        for _d in tab_list:
            _d['sub_tabs'] = sub_tab_dict_list.get(_d['id']) or []

        return tab_list


class SubTabAPI(ApiViewHandler):
    @login_required()
    def get(self):
        data = [i.to_dict() for i in SubTabs.filter_by_query()]
        tab_dict = {
            i.id: i.to_dict()
            for i in Tabs.query.filter(Tabs.id.in_(set([i['tab_id'] for i in data])), Tabs.available == 1)
        }
        for d in data:
            d['tab'] = tab_dict[d['tab_id']]

        return data


class SubTabFavAPI(ApiViewHandler):
    @login_required()
    def get(self):
        fav_sub_tab_id_list = [i.sub_tab_id for i in SubTabFav.filter_by_query(user_id=session['user_info']['id'])]
        sub_tab_list = [
            i.to_dict()
            for i in SubTabs.query.filter(SubTabs.id.in_(set(fav_sub_tab_id_list)), SubTabs.available == 1)
        ]
        topic_sub_tab_dict = dict()
        for topic_obj in Topics.query.filter(
                Topics.sub_tab_id.in_(set([i['id'] for i in sub_tab_list])),
                Topics.available == 1
        ):
            if topic_sub_tab_dict.get(topic_obj.sub_tab_id):
                topic_sub_tab_dict[topic_obj.sub_tab_id] += 1
            else:
                topic_sub_tab_dict[topic_obj.sub_tab_id] = 1
        for sub_tab in sub_tab_list:
            sub_tab['topic_count'] = topic_sub_tab_dict.get(sub_tab['id'], 0)

        return sub_tab_list

    @login_required()
    @need_params(*['tab', 'action'])
    def post(self):
        obj = SubTabs.get_by_query(name=self.input.tab)
        if self.input.action == 'add':
            sub_tab_fav_obj = SubTabFav.filter_by_query(
                sub_tab_id=obj.id,
                user_id=session['user_info']['id'],
                show_deleted=True
            ).first()
            if sub_tab_fav_obj:
                sub_tab_fav_obj.available = 1
            else:
                sub_tab_fav_obj = SubTabFav()
                sub_tab_fav_obj.sub_tab_id = obj.id
                sub_tab_fav_obj.user_id = session['user_info']['id']
            sub_tab_fav_obj.save()
        elif self.input.action == 'cal':
            sub_tab_fav_obj = SubTabFav.filter_by_query(
                sub_tab_id=obj.id,
                user_id=session['user_info']['id']
            ).first()
            if sub_tab_fav_obj:
                sub_tab_fav_obj.available = 0
                sub_tab_fav_obj.save()


class TabMixedAPI(ApiViewHandler):
    @need_params('tab')
    def get(self):
        data = dict()
        sub_tab_info = SubTabs.get_by_query(name=self.input.tab).to_dict()
        sub_tab_info['tab'] = Tabs.get_by_id(sub_tab_info['tab_id']).to_dict()
        sub_tab_info['other_tabs'] = [i.to_dict() for i in SubTabs.filter_by_query(tab_id=sub_tab_info['tab_id'])]
        data['sub_tab_info'] = sub_tab_info

        topic_objs = Topics.filter_by_query(sub_tab_id=sub_tab_info['id']).order_by(Topics.time_create.desc())
        topic_count = topic_objs.count()
        if topic_count > 100:
            page = int(self.input.page) if self.input.page else 1
            page_size = 50
            topic_objs = topic_objs.offset((page - 1) * page_size).limit(page_size)
        topic_list = [_t.to_dict() for _t in topic_objs]

        user_dict = {
            i.id: i.to_dict(remove_fields_list=['password'])
            for i in Users.query.filter(
                Users.id.in_(set(i['user_id'] for i in topic_list)),
                Users.available == 1
            )
        }

        last_reply_user_dict = {
            i.id: i.to_dict(remove_fields_list=['password'])
            for i in Users.query.filter(
                Users.id.in_(set(i['last_reply_user_id'] for i in topic_list)),
                Users.available == 1
            )
        }

        comment_count_dict = dict()
        comment_objs = Comments.query.filter(
            Comments.topic_id.in_(set(i['id'] for i in topic_list)),
            Comments.available == 1
        )
        for c in comment_objs:
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

        for _d in topic_list:
            _d['user'] = user_dict[_d['user_id']]
            if _d['last_reply_user_id']:
                _d['last_reply_user'] = last_reply_user_dict[_d['last_reply_user_id']]
            _d['comment_count'] = comment_count_dict.get(_d['id'], 0)
            # 获取up和down数量
            if up_down_dict_list.get(_d['id']):
                _d['up_count'] = len([i for i in up_down_dict_list[_d['id']] if i is True])
                _d['down_count'] = len([i for i in up_down_dict_list[_d['id']] if i is False])
            else:
                _d['up_count'] = 0
                _d['down_count'] = 0

        data['total'] = topic_count
        data['list'] = topic_list
        if session.get('is_login'):
            if SubTabFav.filter_by_query(
                    user_id=session['user_info']['id'],
                    sub_tab_id=sub_tab_info['id']
            ).first():
                data['is_fav'] = True
            else:
                data['is_fav'] = False
        return data
