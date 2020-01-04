from flask import session
from super_bbs.core.viewhandler import ApiViewHandler
from super_bbs.model.topics import Topics
from super_bbs.model.users import Users
from super_bbs.model.comments import Comments
from super_bbs.utils import need_params, login_required


class CommentAPI(ApiViewHandler):
    @login_required(admin=True)
    def get(self):
        if self.input.uid:
            obj = Comments.get_by_uid(self.input.uid)
            data = obj.to_dict()
            data['user'] = Users.get_by_id(data['user_id']).to_dict(remove_fields_list=['password'])
            data['topic'] = Topics.get_by_id(data['topic_id']).to_dict()
        else:
            data = Comments.filter_by_query()
            if self.input.tab_id:
                data.filter_by_query(tab_id=self.input.tab_id)
            elif self.input.sub_tab_id:
                data.filter_by_query(sub_tab_id=self.input.sub_tab_id)
            if self.input.sk_ and self.input.sv_:
                data = data.filter(getattr(Comments, self.input.sk_).like(f'%{self.input.sv_}%'))

            if self.input.odb_ and self.input.odt_ in ['asc', 'desc']:
                data = data.order_by(getattr(getattr(Comments, self.input.odb_), self.input.odt_)())
            else:
                data = data.order_by(Comments.time_create.desc())

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
            topic_dict = {
                i.id: i.to_dict()
                for i in Topics.query.filter(
                    Topics.id.in_(set(i['topic_id'] for i in data)),
                    Topics.available == 1
                )
            }

            for _d in data:
                _d['user'] = user_dict[_d['user_id']]
                _d['topic'] = topic_dict[_d['topic_id']]

            if total is not None:
                data = {'total': total, 'list': data}

        return data

    @login_required(admin=True)
    @need_params(*['uid'])
    def put(self):
        obj = Comments.get_by_uid(self.input.uid)
        if self.input.content:
            obj.content = self.input.content
        if self.input.like_count:
            obj.like_count = self.input.like_count
        obj.save()

    @login_required(admin=True)
    @need_params(*['uid'])
    def delete(self):
        obj = Comments.get_by_uid(self.input.uid)
        obj.update(available=0)
