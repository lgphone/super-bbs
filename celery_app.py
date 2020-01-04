from datetime import datetime
from celery import Celery, Task
from celery.schedules import crontab
from super_bbs.app import create_app
from super_bbs.model.users import CeleryTaskLogs

flask_app = create_app()
flask_app.app_context().push()

schedule_config = {
    'CELERYBEAT_SCHEDULE': {
        'clean_celery_log': {
            'task': 'super_bbs.controller.account.tasks.clean_celery_log',
            'schedule': 10 if flask_app.config['DEBUG'] else crontab(minute=10, hour=3)
        }
    }
}


class BaseTask(Task):
    """
        celery 基类, 继承Task
    """

    def __call__(self, *args, **kwargs):
        log_obj = CeleryTaskLogs()
        log_obj.task_id = self.request.id
        log_obj.task_name = self.name
        log_obj.save()
        return super(BaseTask, self).__call__(*args, **kwargs)

    def on_success(self, retval, task_id, args, kwargs):
        log_obj = CeleryTaskLogs.get_by_query(task_id=task_id)
        log_obj.done = True
        log_obj.time_done = datetime.now()
        log_obj.task_status = True
        if retval:
            log_obj.retval = str(retval)
        if args:
            log_obj.args = str(args)
        if kwargs:
            log_obj.kwargs = str(kwargs)
        log_obj.save()

        return super(BaseTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('fail task: {0}'.format(task_id))
        log_obj = CeleryTaskLogs.get_by_query(task_id=task_id)
        log_obj.done = True
        log_obj.time_done = datetime.now()
        log_obj.task_status = False
        if args:
            log_obj.args = str(args)
        if kwargs:
            log_obj.kwargs = str(kwargs)
        if exc:
            log_obj.exc = str(exc)
        if einfo:
            log_obj.einfo = str(einfo)
        log_obj.save()

        return super(BaseTask, self).on_failure(exc, task_id, args, kwargs, einfo)


celery = Celery(flask_app.import_name, task_cls=BaseTask)
celery.conf.update(flask_app.config)
celery.conf.update(schedule_config)

# 导入task注册
celery.autodiscover_tasks([
    'super_bbs.controller.account.task'
])
