import time
import datetime

class BaseModel(object):

    table_name = None
    attributes = ()

    def __init__(self, **kwargs):
        self.__dict__['db'] = kwargs.pop('db')

        self._check_attributes(kwargs.keys())
        for key, value in kwargs.items():
            self.__dict__[key] = value

    def _check_attributes(self, attributes):
        disallowed = set(attributes) - set(self.attributes)
        if disallowed:
            raise AttributeError(', '.join(disallowed))
        return True

    def _check_attribute(self, attribute):
        if not attribute in self.attributes:
            raise AttributeError(attribute)

    def __setattr__(self, key, value):
        self._check_attribute(key)
        self.__dict__[key] = value

    def _load_data(self, model_id):
        data = self.db.get(self.table_name, self.attributes, model_id)
        for key, value in data.items():
            if not key in self.__dict__.keys():
                self.__dict__[key] = value


    def __getattr__(self, key):
        self._check_attribute(key)

        if not key in self.__dict__.keys():
            #TODO: handle a missing id
            self._load_data(self.__dict__['id'])

        return self.__dict__[key]

    def save(self):
        data = {}
        for key in self.attributes:
            try:
                data[key] = self.__dict__[key]
            except KeyError:
                pass
        self.db.add(self.table_name, data)


class BaseCollection(object):

    model_class = None
    extra_query = None
    extra_args = None

    def __init__(self, db):
        self.db = db

    def _get_models(self):
        data = self.db.get_all(self.model_class.table_name,
                              self.model_class.attributes,
                              self.extra_query,
                              self.extra_args)
        return [self.model_class(db=self.db, **d) for d in data]

    def __iter__(self):
        return self._get_models().__iter__()



class Result(BaseModel):

    table_name = 'results'
    attributes = ('id', 'name', 'duration', 'begin_timestamp')


class ResultCollection(BaseCollection):
    model_class = Result

    def __init__(self, db, window):
        super(ResultCollection, self).__init__(db)
        now = int(time.mktime(datetime.datetime.utcnow().timetuple()))
        self.begin_timestamp_min = now - window
        self.extra_args = (self.begin_timestamp_min,)
        self.extra_query = "where begin_timestamp >= ?"
