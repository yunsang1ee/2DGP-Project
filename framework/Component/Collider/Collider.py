from abc import abstractmethod, ABC

from pygame import Vector2

from framework.Common import Enums
from framework.Common.Enums import ComponentType
from framework.Component import Script
from framework.Component.Component import Component


class Collider(Component, ABC):
    __isRendering : bool = False
    collisionID : int = 0
    
    def __init__(self, type : Enums.ColliderType):
        super().__init__(ComponentType.Collider)
        self.__type : Enums.ColliderType = type
        self.__offset : Vector2 = Vector2(0, 0)
        self.__size : Vector2 = Vector2(0, 0)
        self.__id = Collider.collisionID; Collider.collisionID += 1
        pass
    
    def __hash__(self):
        return hash(self.__id)
    
    def __eq__(self, other):
        if isinstance(other, Collider):
            return self.__id == other.__id
        return False

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
    def OnCollisionEnter(self, other: 'Collider'):
        sc : Script = self.GetOwner().GetComponent(ComponentType.Script)
        sc.OnCollisionEnter(other)
        pass
    
    @abstractmethod
    def OnCollisionStay(self, other: 'Collider'):
        sc : Script = self.GetOwner().GetComponent(ComponentType.Script)
        sc.OnCollisionStay(other)
        pass
    
    @abstractmethod
    def OnCollisionExit(self, other: 'Collider'):
        sc : Script = self.GetOwner().GetComponent(ComponentType.Script)
        sc.OnCollisionExit(other)
        pass
    
    
    def SetOffset(self, offset : Vector2):
        self.__offset = offset
        pass
    def SetSize(self, size : Vector2):
        self.__size = size
        pass
    
    def GetCollisionType(self):
        return self.__type
    
    def GetID(self):
        return self.__id
    
    def GetOffset(self):
        return self.__offset
    
    def GetSize(self):
        return self.__size

    @staticmethod
    def ToggleRender():
        Collider.__isRendering = not Collider.__isRendering
        
    @staticmethod
    def SetRender(flag : bool):
        Collider.__isRendering = flag