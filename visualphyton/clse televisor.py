from abc import ABC, abstractmethod


class dispositivoselectricos(ABC):
    @abstractmethod
    def encender(self):
        pass
    @abstractmethod
    def espagar(self):
        pass



class televisor():

    def encender(self):
        print("televisor encendido")
    def apagar(self):
        print("televisor apagado")
tv=televisor()
tv.apagar()