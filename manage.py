import os
import json
from flask_script import Manager
from flask_migrate import MigrateCommand
from super_bbs.app import create_app
from super_bbs.model.users import Users
from super_bbs.model.tabs import Tabs, SubTabs
from super_bbs.constants import BASE_DIR

app = create_app()

manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.option('--username', dest='username', help='admin username', default='admin')
@manager.option('--password', dest='password', help='admin password', default='admin')
def init_app(username, password):
    # check
    if Users.filter_by_query(role_id=1).first():
        print('重复初始化！退出')
        exit(1)
    # create admin
    user_obj = Users.create_by_uid()
    user_obj.username = username
    user_obj.email = 'admin@admin.com'
    user_obj.role_id = 1
    user_obj.set_password(password)
    user_obj.save()
    # create base tab
    with open(os.path.join(BASE_DIR, 'tabs.json'), 'r') as f:
        tab_data = json.loads(f.read())
        for t in tab_data:
            t_obj = Tabs.create_by_uid()
            t_obj.name = t['name']
            t_obj.zh = t['zh']
            if t.get('sort_num'):
                t_obj.sort_num = t['sort_num']
            t_obj.save()
            for st in t.get('sub_tabs'):
                st_obj = SubTabs.create_by_uid()
                st_obj.tab_id = t_obj.id
                st_obj.name = st['name']
                st_obj.zh = st['zh']
                if st.get('sort_num'):
                    st_obj.sort_num = st['sort_num']
                st_obj.desc = st['desc']
                st_obj.save()

    print(f'init success! admin username: {username}, password: {password}')


@manager.command
def update_tabs():
    # update base tab
    with open(os.path.join(BASE_DIR, 'tabs.json'), 'r') as f:
        tab_data = json.loads(f.read())
        for t in tab_data:
            if not Tabs.filter_by_query(name=t['name']).first():
                t_obj = Tabs.create_by_uid()
            else:
                t_obj = Tabs.get_by_query(name=t['name'])
            t_obj.name = t['name']
            t_obj.zh = t['zh']
            if t.get('sort_num'):
                t_obj.sort_num = t['sort_num']
            t_obj.save()
            for st in t.get('sub_tabs'):
                if not SubTabs.filter_by_query(name=st['name']).first():
                    st_obj = SubTabs.create_by_uid()
                else:
                    st_obj = SubTabs.get_by_query(name=st['name'])
                st_obj.tab_id = t_obj.id
                st_obj.name = st['name']
                st_obj.zh = st['zh']
                if st.get('sort_num'):
                    st_obj.sort_num = st['sort_num']
                st_obj.desc = st['desc']
                st_obj.save()

    print('update tabs success !')


if __name__ == '__main__':
    manager.run()
