from google.appengine.ext import ndb


class Item(ndb.Model):

    value = ndb.StringProperty()


class ValueCount(ndb.Model):

    count = ndb.IntegerProperty()

    @classmethod
    def increment(cls, value):
        try:
            vc = cls.get_by_id(value)
            vc.count += 1
        except AttributeError:
            vc = cls(id=value, count=1)
        vc.put()

    @classmethod
    def decrement(cls, value):
        vc = cls.get_by_id(value)
        vc.count = vc.count - 1 if vc.count > 0 else 0
        vc.put()
