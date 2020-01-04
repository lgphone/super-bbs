from collections import defaultdict
from super_bbs.core.viewhandler import ApiViewHandler, LogicError
from super_bbs.model.tabs import Tabs, SubTabs
from super_bbs.utils import need_params, login_required


class TabAPI(ApiViewHandler):
    @login_required(admin=True)
    def get(self):
        if self.input.uid:
            obj = Tabs.get_by_uid(self.input.uid)
            data = obj.to_dict()
            data['sub_tabs'] = [i.to_dict() for i in SubTabs.filter_by_query(tab_id=data['id'])]
        else:
            data = Tabs.filter_by_query()
            if self.input.sk_ and self.input.sv_:
                data = data.filter(getattr(Tabs, self.input.sk_).like(f'%{self.input.sv_}%'))

            if self.input.odb_ and self.input.odt_ in ['asc', 'desc']:
                data = data.order_by(getattr(getattr(Tabs, self.input.odb_), self.input.odt_)())
            else:
                data = data.order_by(Tabs.time_create.asc())

            total = None
            if self.input.page and self.input.page_size:
                total = data.count()
                data = data.offset(
                    (int(self.input.page) - 1) * int(self.input.page_size)
                ).limit(int(self.input.page_size))

            data = [_t.to_dict() for _t in data]

            sub_tab_dict_list = defaultdict(list)
            for sub_tab in SubTabs.filter_by_query().order_by(SubTabs.sort_num.asc()):
                sub_tab_dict_list[sub_tab.tab_id].append(sub_tab.to_dict())

            for _d in data:
                _d['sub_tabs'] = sub_tab_dict_list.get(_d['id']) or []

            if total is not None:
                data = {'total': total, 'list': data}

        return data

    @login_required(admin=True)
    @need_params(*['name', 'zh'])
    def post(self):
        obj = Tabs.create_by_uid()
        if not self.is_valid_name(self.input.name):
            raise LogicError('name 参数格式只能为英文')
        obj.name = self.input.name
        obj.zh = self.input.zh
        if self.input.sort_num:
            obj.sort_num = self.input.sort_num

        obj.save()

    @login_required(admin=True)
    @need_params(*['uid'])
    def put(self):
        obj = Tabs.get_by_uid(self.input.uid)
        if self.input.name:
            if not self.is_valid_name(self.input.name):
                raise LogicError('name 参数格式只能为英文')
            obj.name = self.input.name
        if self.input.zh:
            obj.zh = self.input.zh
        if self.input.sort_num:
            obj.sort_num = self.input.sort_num
        obj.save()

    @login_required(admin=True)
    @need_params(*['uid'])
    def delete(self):
        obj = Tabs.get_by_uid(self.input.uid)
        if SubTabs.filter_by_query(tab_id=obj.id).all():
            raise LogicError('存在子类别无法删除')
        obj.update(available=0)


class SubTabAPI(ApiViewHandler):
    @login_required(admin=True)
    def get(self):
        if self.input.uid:
            obj = SubTabs.get_by_uid(self.input.uid)
            data = obj.to_dict()
            data['tab'] = Tabs.get_by_id(obj.tab_id).to_dict()
        else:
            if self.input.tab_id:
                data = SubTabs.filter_by_query(tab_id=self.input.tab_id)
            else:
                data = SubTabs.filter_by_query()
            if self.input.sk_ and self.input.sv_:
                data = data.filter(getattr(SubTabs, self.input.sk_).like(f'%{self.input.sv_}%'))

            if self.input.odb_ and self.input.odt_ in ['asc', 'desc']:
                data = data.order_by(getattr(getattr(SubTabs, self.input.odb_), self.input.odt_)())
            else:
                data = data.order_by(SubTabs.time_create.desc())

            total = None
            if self.input.page and self.input.page_size:
                total = data.count()
                data = data.offset(
                    (int(self.input.page) - 1) * int(self.input.page_size)
                ).limit(int(self.input.page_size))

            data = [_t.to_dict() for _t in data]
            tab_dict = {
                i.id: i.to_dict()
                for i in Tabs.filter_by_query()
            }

            for d in data:
                d['tab'] = tab_dict[d['tab_id']]

            if total is not None:
                data = {'total': total, 'list': data}

        return data

    @login_required(admin=True)
    @need_params(*['tab_id', 'name', 'zh'])
    def post(self):
        obj = SubTabs.create_by_uid()
        _tab_obj = Tabs.get_by_id(self.input.tab_id)
        obj.tab_id = self.input.tab_id
        if not self.is_valid_name(self.input.name):
            raise LogicError('name 参数格式只能为英文')
        obj.name = self.input.name
        obj.zh = self.input.zh
        if self.input.desc:
            obj.desc = self.input.desc
        if self.input.sort_num:
            obj.sort_num = self.input.sort_num
        obj.save()

    @login_required(admin=True)
    @need_params(*['uid'])
    def put(self):
        obj = SubTabs.get_by_uid(self.input.uid)
        if self.input.name:
            if not self.is_valid_name(self.input.name):
                raise LogicError('name 参数格式只能为英文')
            obj.name = self.input.name
        if self.input.zh:
            obj.zh = self.input.zh
        if self.input.desc:
            obj.name = self.input.desc
        if self.input.sort_num:
            obj.sort_num = self.input.sort_num
        obj.save()

    @login_required(admin=True)
    @need_params(*['uid'])
    def delete(self):
        obj = SubTabs.get_by_uid(self.input.uid)
        obj.update(available=0)
