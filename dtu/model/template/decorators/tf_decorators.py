from functools import wraps

__root_template = None


def root_tf(cls):
    original_init = cls.__init__

    @wraps(original_init)
    def wrapped_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        self.template.root_template = self.template
        global __root_template
        __root_template = self.template

    cls.__init__ = wrapped_init
    return cls


def sub_tf(cls):
    original_init = cls.__init__

    @wraps(original_init)
    def wrapped_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        global __root_template
        self.template.root_template = __root_template

    cls.__init__ = wrapped_init
    return cls