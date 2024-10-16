from abc import ABC, abstractmethod

class AuthenticatorBase(ABC):
    @abstractmethod
    def GetAuthtoken(self):
        pass
