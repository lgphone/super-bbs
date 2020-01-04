from collections import defaultdict
from flask import session
from super_bbs.core.viewhandler import ApiViewHandler
from super_bbs.model.topics import Topics, TopicAppends, Tags, TopicToTag, TopicUpDown
from super_bbs.model.users import Users
from super_bbs.model.tabs import Tabs, SubTabs
from super_bbs.model.comments import Comments
from super_bbs.utils import need_params, login_required


class TopicAPI(ApiViewHandler):
    @login_required(admin=True)
    def get(self):
        if self.input.uid:
            obj = Topics.get_by_uid(self.input.uid)
            data = obj.to_dict()
            data['user'] = Users.get_by_id(data['user_id']).to_dict(remove_fields_list=['password'])
            if data['last_reply_user_id']:
                data['last_reply_user'] = Users.get_by_id(data['last_reply_user_id']).to_dict(remove_fields_list=['password'])
            data['tab'] = Tabs.get_by_id(data['tab_id']).to_dict()
            data['sub_tab'] = SubTabs.get_by_id(data['sub_tab_id']).to_dict()
            data['appends'] = [i.to_dict() for i in TopicAppends.filter_by_query(topic_id=data['id'])]
            comment_list = [i.to_dict() for i in Comments.filter_by_query(topic_id=data['id'])]
            comment_user_dict = {
                i.id: i.to_dict()
                for i in Users.query.filter(
                    Users.id.in_(set(i['user_id'] for i in comment_list)),
                    Users.available == 1
                )
            }
            for comment in comment_list:
                comment['user'] = comment_user_dict[comment['user_id']]
            data['comments'] = comment_list
            data['comment_count'] = len(comment_list)
            data['up_count'] = TopicUpDown.filter_by_query(topic_id=data['id'], action=True).count()
            data['down_count'] = TopicUpDown.filter_by_query(topic_id=data['id'], action=False).count()
        else:
            data = Topics.filter_by_query()
            if self.input.tab_id:
                data.filter_by_query(tab_id=self.input.tab_id)
            elif self.input.sub_tab_id:
                data.filter_by_query(sub_tab_id=self.input.sub_tab_id)
            if self.input.sk_ and self.input.sv_:
                data = data.filter(getattr(Topics, self.input.sk_).like(f'%{self.input.sv_}%'))

            if self.input.odb_ and self.input.odt_ in ['asc', 'desc']:
                data = data.order_by(getattr(getattr(Topics, self.input.odb_), self.input.odt_)())
            else:
                data = data.order_by(Topics.time_create.desc())

            total = None
            if self.input.page and self.input.page_size:
                total = data.count()
                data = data.offset(
                    (int(self.input.page) - 1) * int(self.input.page_size)
                ).limit(int(self.input.page_size))

            data = [_t.to_dict() for _t in data]

            user_dict = {
                i.id: i.to_dict(remove_fields_list=['password'])
                for i in Users.query.filter(
                    Users.id.in_(set(i['user_id'] for i in data)),
                    Users.available == 1
                )
            }

            last_reply_user_dict = {
                i.id: i.to_dict(remove_fields_list=['password'])
                for i in Users.query.filter(
                    Users.id.in_(set(i['last_reply_user_id'] for i in data)),
                    Users.available == 1
                )
            }

            tab_dict = {
                i.id: i.to_dict()
                for i in Tabs.query.filter(
                    Tabs.id.in_(set(i['tab_id'] for i in data)),
                    Tabs.available == 1
                )
            }

            sub_tab_dict = {
                i.id: i.to_dict()
                for i in SubTabs.query.filter(
                    SubTabs.id.in_(set(i['sub_tab_id'] for i in data)),
                    SubTabs.available == 1
                )
            }

            comment_count_dict = dict()
            for c in Comments.query.filter(Comments.topic_id.in_(set(i['id'] for i in data)), Comments.available == 1):
                if comment_count_dict.get(c.topic_id):
                    comment_count_dict[c.topic_id] += 1
                else:
                    comment_count_dict[c.topic_id] = 1

            up_down_dict_list = defaultdict(list)
            for up_down_obj in TopicUpDown.query.filter(
                    TopicUpDown.topic_id.in_(set(i['id'] for i in data)),
                    TopicUpDown.available == 1
            ):
                up_down_dict_list[up_down_obj.topic_id].append(up_down_obj.action)

            for _d in data:
                _d['user'] = user_dict[_d['user_id']]
                if _d['last_reply_user_id']:
                    _d['last_reply_user'] = last_reply_user_dict[_d['last_reply_user_id']]
                _d['tab'] = tab_dict[_d['tab_id']]
                _d['sub_tab'] = sub_tab_dict[_d['sub_tab_id']]
                _d['comment_count'] = comment_count_dict.get(_d['id'], 0)
                # 获取up和down数量
                if up_down_dict_list.get(_d['id']):
                    _d['up_count'] = len([i for i in up_down_dict_list[_d['id']] if i is True])
                    _d['down_count'] = len([i for i in up_down_dict_list[_d['id']] if i is False])
                else:
                    _d['up_count'] = 0
                    _d['down_count'] = 0

            if total is not None:
                data = {'total': total, 'list': data}

        return data

    @login_required(admin=True)
    @need_params(*['uid'])
    def put(self):
        obj = Topics.get_by_uid(self.input.uid)
        if self.input.title:
            obj.title = self.input.title
        if self.input.content:
            obj.content = self.input.content
            obj.content_length = len(self.input.content)
        if self.input.sub_tab_id:
            sub_tab_obj = SubTabs.get_by_id(self.input.sub_tab_id)
            obj.sub_tab_id = sub_tab_obj.id
            obj.tab_id = sub_tab_obj.tab_id
        obj.save()

    @login_required(admin=True)
    @need_params(*['uid'])
    def delete(self):
        obj = Topics.get_by_uid(self.input.uid)
        for tmp_obj in TopicAppends.filter_by_query(topic_id=obj.id):
            tmp_obj.update(available=0)
        for tmp_obj in Comments.filter_by_query(topic_id=obj.id):
            tmp_obj.update(available=0)
        obj.update(available=0)
