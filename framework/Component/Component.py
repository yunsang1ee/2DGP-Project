from abc import abstractmethod, ABC

from framework.Common.Enums import ComponentType


class Component(ABC):
    def __init__(self, compoType : ComponentType):
        from framework.GameObject.GameObject import GameObject
        self.ownerObject : GameObject = None
        self.type : ComponentType = compoType
        pass

    @abstractmethod
    def Update(self):
        pass

    @abstractmethod
    def LateUpdate(self):
        pass

    @abstractmethod
    def Render(self):
        pass
    
    def SetOwner(self, owner) -> None: self.ownerObject = owner
    def GetOwner(self): return self.ownerObject
    def GetType(self) -> ComponentType: return self.type