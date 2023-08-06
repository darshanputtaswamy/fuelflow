import abc
class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self):
        raise NotImplementedError