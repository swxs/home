class BaseMemorizer(object):
    def __init__(self, dao) -> None:
        super().__init__()
        self.dao = dao
        self.model = dao.__model__
