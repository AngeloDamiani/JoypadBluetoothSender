import abc

class Ui(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def start(self):
        pass
