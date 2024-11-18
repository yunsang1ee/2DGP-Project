from abc import abstractmethod

from framework.Common.Enums import ComponentType
from framework.Component.Collider.Collider import Collider
from framework.Component.Component import Component


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
    def OnCollisionEnter(self, other : Collider):
        pass
    
    @abstractmethod
    def OnCollisionStay(self, other : Collider):
        pass
    
    @abstractmethod
    def OnCollisionExit(self, other : Collider):
        pass
    