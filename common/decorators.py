import warnings


def abstract_pydantic_model[T: type](cls: T) -> T:
    """Декоратор, запрещающий создание экземпляров декорируемого класса."""
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        if type(self) is cls:
            raise TypeError(f"{cls.__name__} is abstract and cannot be instantiated")
        original_init(self, *args, **kwargs)

    cls.__init__ = new_init
    return cls


def emit_runtime_warning[T: type](cls: T) -> T:
    """
    Берет сообщение из атрибута __deprecated__, который ставит @deprecated,
    и добавляет warning в __init__.
    """
    message = getattr(cls, "__deprecated__", None)

    if message is None:
        message = f"{cls.__name__} is deprecated."

    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        warnings.warn(message, category=DeprecationWarning, stacklevel=2)
        original_init(self, *args, **kwargs)

    cls.__init__ = new_init
    return cls
