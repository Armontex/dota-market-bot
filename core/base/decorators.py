def abstract_pydantic_model(cls):
    """Декоратор, запрещающий создание экземпляров декорируемого класса."""
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        if type(self) is cls:
            raise TypeError(f"{cls.__name__} is abstract and cannot be instantiated")
        original_init(self, *args, **kwargs)

    cls.__init__ = new_init
    return cls
