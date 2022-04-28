class CRUDMixin:
    @classmethod
    def create(cls, **kwargs):
        return cls(**kwargs)

    @classmethod
    def patch(cls, **kwargs):
        if "id" in kwargs:
            id = kwargs.pop("id")

        record = cls.query.filter(cls.id == id).first()

        for key, value in kwargs.items():
            if hasattr(cls, key):
                setattr(record, key, value)

        return record

    @classmethod
    def destroy(cls, id):
        value = cls.query.filter(cls.id == id)
        value.delete()
        return id
