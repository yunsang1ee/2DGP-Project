from abc import abstractmethod

from framework.Common.Enums import ComponentType
from framework.GameObject.GameObject import GameObject


class Component:
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

    def SetOwner(self, owner): self.ownerObject = owner
    def GetOwner(self) -> GameObject: return self.ownerObject
    def GetType(self) -> ComponentType: return self.type