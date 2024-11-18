from pygame import Vector2

from framework.Component import Component
from framework.Common.Enums import ComponentType


class Transform(Component.Component):
    def __init__(self):
        super().__init__(ComponentType.Transform)
        self.__position : Vector2 = Vector2(0, 0)
        self.__rotation : float = 0.0
        self.__scale : Vector2 = Vector2(1, 1)
        pass
    
    def Update(self):
        super().Update()
        pass

    def LateUpdate(self):
        super().LateUpdate()
        pass

    def Render(self):
        super().Render()
        pass
    
    def SetPosition(self, value : Vector2): self.__position = value
    def SetRotation(self, value : float): self.__rotation = value
    def SetScale(self, value : Vector2): self.__scale = value
    
    def GetPosition(self) -> Vector2: return self.__position
    def GetRotation(self) -> float: return self.__rotation
    def GetScale(self) -> Vector2: return self.__scale