from super_bbs.core.extensions import db
from super_bbs.core.basehandler import BaseHandler, BaseError
from flask import current_app
import copy
import datetime


class DBMixin(BaseHandler):
    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    @classmethod
    def create_by_uid(cls, **kwargs):
        instance = cls(**kwargs)
        instance.uid = cls.generate_hash_uuid(12)
        return instance

    @classmethod
    def get_by_id(cls, _id):
        instance = db.session.query(cls).filter_by(id=_id, available=1).first()
        if not instance:
            raise BaseError(cls.__name__ + ' Not Find')
        return instance

    @classmethod
    def get_by_uid(cls, uid):
        instance = db.session.query(cls).filter_by(uid=uid, available=1).first()
        if not instance:
            raise BaseError(cls.__name__ + ' Not Find')
        return instance

    @classmethod
    def get_by_query(cls, show_deleted=False, **query_dict):
        if show_deleted is False:
            query_dict['available'] = 1
        instance = db.session.query(cls).filter_by(**query_dict).first()
        if not instance:
            raise BaseError(cls.__name__ + ' Not Find')
        return instance

    @classmethod
    def filter_by_query(cls, show_deleted=False, **query_dict):
        if query_dict.get('available'):
            query_dict.pop('available')

        if show_deleted is False:
            query_dict['available'] = 1

        tmp = copy.deepcopy(query_dict)
        for k in tmp:
            if k not in cls.__dict__:
                query_dict.pop(k)
        return db.session.query(cls).filter_by(**query_dict)

    @classmethod
    def create_from_dict(cls, d):
        assert isinstance(d, dict)
        instance = cls(**d)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in list(kwargs.items()):
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except Exception as e:
                current_app.logger.error(e)
                db.session.rollback()
                raise e
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e

        return self

    def to_dict(self, fields_list=None, remove_fields_list=None, remove_available=True):
        if remove_fields_list:
            column_list = [column for column in self.__dict__ if column not in remove_fields_list]
        elif fields_list:
            column_list = [column for column in self.__dict__ if column in fields_list]
        else:
            column_list = self.__dict__

        data = copy.deepcopy({column_name: getattr(self, column_name)
                              for column_name in column_list})

        if data.get('_sa_instance_state'):
            data.pop('_sa_instance_state')

        if remove_available and data.get('available'):
            data.pop('available')

        for k, v in data.items():
            if isinstance(v, datetime.datetime):
                data[k] = v.strftime('%Y-%m-%d %H:%M:%S')

        return data

    @classmethod
    def create_or_update(cls, query_dict, update_dict=None):
        instance = db.session.query(cls).filter_by(**query_dict).first()
        if instance:
            if update_dict is not None:
                return instance.update(**update_dict)
            else:
                return instance
        else:
            query_dict.update(update_dict or {})
            return cls.create(**query_dict)


class BaseModal(DBMixin, db.Model):
    """
    BaseModal
    """
    __abstract__ = True
