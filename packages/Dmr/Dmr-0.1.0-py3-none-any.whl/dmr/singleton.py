from datetime import datetime

class Central_data(object): 
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Central_data, cls).__new__(cls)
        return cls.instance

    @property
    def init_time(self):
        if not hasattr(self,'_init_time'):
            self._init_time = datetime.now()
        return self._init_time

    @init_time.setter
    def init_time(self, init_time):
        self._init_time = init_time