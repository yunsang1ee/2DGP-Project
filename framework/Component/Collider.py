from abc import abstractmethod

from framework.Common.Enums import ComponentType
from framework.Component.Component import Component
from framework.GameObject.GameObject import GameObject


class Collider(Component):
    def __init__(self):
        super().__init__(ComponentType.Collider)
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

