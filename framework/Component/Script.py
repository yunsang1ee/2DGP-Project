from abc import abstractmethod

from framework.Common.Enums import ComponentType
from framework.Component.Component import Component
from framework.GameObject.GameObject import GameObject


class Script(Component):
    def __init__(self):
        super().__init__(ComponentType.Script)
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
    
    @abstractmethod
    def OnCollisionEnter(self, other : GameObject):
        pass
    
    @abstractmethod
    def OnCollisionStay(self, other : GameObject):
        pass
    
    @abstractmethod
    def OnCollisionExit(self, other : GameObject):
        pass
    