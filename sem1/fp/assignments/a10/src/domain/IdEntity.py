class IdEntity(object):
    def __init__(self, object_id: int):
        self._id = object_id

    @property
    def id(self):
        return self._id