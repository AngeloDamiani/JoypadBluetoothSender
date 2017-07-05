import abc

class IJoypadObserver(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def update(self, data):
        pass
