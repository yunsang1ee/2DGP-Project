import enum
from abc import abstractmethod, ABC

from typing import Dict
from framework.Common import Enums
from framework.Component import Component


class GameObject(ABC):
    class State(enum.Enum):
        Alive = 0; Paused = 1; Dead = 2
        pass


    def __init__(self, layer = Enums.LayerType.Non):
        self.components : Dict[int, Component] = {}
        self.state = self.State.Alive
        self.layer = layer
        pass

    @abstractmethod
    def Update(self):
        for component in self.components.values():
            component.Update()
        pass

    @abstractmethod
    def LateUpdate(self):
        for component in self.components.values():
            component.LateUpdate()
        pass

    @abstractmethod
    def Render(self):
        for component in self.components.values():
            component.Render()
        pass

    def AddComponent(self, component: Component):
        component.SetOwner(self)
        self.components[component.GetType().value] = component
        return self.components[component.GetType().value]

    def GetComponent(self, component: Component) -> Component:
        component = self.components[component.GetType().value]
        return component

    def SetState(self, state): self.state = state
    def GetState(self): return self.state
    def SetLayer(self, layer): self.layer = layer
    def GetLayer(self): return self.layer

    pass