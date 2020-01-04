from collections import defaultdict
from flask import session
from super_bbs.core.viewhandler import ApiViewHandler
from super_bbs.model.topics import Topics, TopicUpDown
from super_bbs.model.users import Users
from super_bbs.model.tabs import Tabs, SubTabs, SubTabFav
from super_bbs.model.comments import Comments


class IndexMixedAPI(ApiViewHandler):
    def get(self):
        data = dict()
        sub_tab_dict_list = defaultdict(list)
        for sub_tab in SubTabs.filter_by_query().order_by(SubTabs.sort_num.asc()):
            sub_tab_dict_list[sub_tab.tab_id].append(sub_tab.to_dict())
        tab_list = [t.to_dict() for t in Tabs.filter_by_query().order_by(Tabs.sort_num.asc())]
        for _d in tab_list:
            _d['sub_tabs'] = sub_tab_dict_list.get(_d['id']) or []

        data['tabs'] = tab_list

        if self.input.tab:
            tab_obj = Tabs.filter_by_query(name=self.input.tab).first()
            if not tab_obj:
                tab_obj = Tabs.get_by_query(name='tech')
        else:
            tab_obj = Tabs.get_by_query(name='tech')
        topic_objs = Topics.filter_by_query(tab_id=tab_obj.id).order_by(Topics.time_create.desc())
        data['tab_topic_count'] = topic_objs.count()
        topic_list = [_t.to_dict() for _t in topic_objs[:80]]
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

        data['topics'] = topic_list
        data['user_count'] = Users.filter_by_query().count()
        data['topic_count'] = Topics.filter_by_query().count()
        data['comment_count'] = Comments.filter_by_query().count()

        today_time_start = self.strptime(self.get_datetime_now().strftime('%Y-%m-%d'), '%Y-%m-%d')
        today_topic_list = [
            i.to_dict() for i in Topics.query.filter(Topics.time_create >= today_time_start, Topics.available == 1)
        ]
        if today_topic_list:
            today_comment_dict = dict()
            for _c in Comments.query.filter(
                    Comments.topic_id.in_(set([i['id'] for i in today_topic_list])),
                    Comments.available == 1
            ):
                if today_comment_dict.get(_c.topic_id):
                    today_comment_dict[_c.topic_id] += 1
                else:
                    today_comment_dict[_c.topic_id] = 1

            for today_topic in today_topic_list:
                today_topic['comment_count'] = today_comment_dict.get(today_topic['id'], 0)

            today_hot_topic_list = sorted(today_topic_list, key=lambda x: x['comment_count'], reverse=True)
            if len(today_hot_topic_list) >= 10:
                today_hot_topic_list = today_hot_topic_list[:10]
        else:
            today_hot_topic_list = []

        data['hot_topics'] = today_hot_topic_list
        if session.get('is_login'):
            fav_sub_tab_id_list = [i.sub_tab_id for i in SubTabFav.filter_by_query(user_id=session['user_info']['id'])]
            sub_tab_list = [
                i.to_dict()
                for i in SubTabs.query.filter(SubTabs.id.in_(set(fav_sub_tab_id_list)), SubTabs.available == 1)
            ]
            data['fav_tabs'] = sub_tab_list

        return data
