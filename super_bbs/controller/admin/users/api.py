from super_bbs.core.viewhandler import ApiViewHandler
from super_bbs.model.users import Users
from super_bbs.utils import need_params, login_required


class UserAPI(ApiViewHandler):
    @login_required(admin=True)
    def get(self):
        if self.input.uid:
            obj = Users.get_by_uid(self.input.uid)
            data = obj.to_dict(remove_fields_list=['password'])
        else:
            data = Users.filter_by_query()
            if self.input.sk_ and self.input.sv_:
                data = data.filter(getattr(Users, self.input.sk_).like(f'%{self.input.sv_}%'))

            if self.input.odb_ and self.input.odt_ in ['asc', 'desc']:
                data = data.order_by(getattr(getattr(Users, self.input.odb_), self.input.odt_)())
            else:
                data = data.order_by(Users.time_create.desc())

            total = None
            if self.input.page and self.input.page_size:
                total = data.count()
                data = data.offset(
                    (int(self.input.page) - 1) * int(self.input.page_size)
                ).limit(int(self.input.page_size))

            data = [_t.to_dict(remove_fields_list=['password']) for _t in data]

            if total is not None:
                data = {'total': total, 'list': data}

        return data

    @login_required(admin=True)
    @need_params(*['uid'])
    def put(self):
        obj = Users.get_by_uid(self.input.uid)
        if self.input.status:
            obj.status = self.input.status
        if self.input.role_id:
            obj.role_id = self.input.role_id
        obj.save()
