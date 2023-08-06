class Log2DB(object):
    @staticmethod
    def get_instance(class_,*args, **kwargs):
        return class_(*args, **kwargs)