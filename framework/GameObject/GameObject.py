import enum

from typing import Dict
from framework.Common import Enums
from framework.Component.Component import Component


class GameObject:
    class State(enum.Enum):
        Alive = 0; Paused = 1; Dead = 2
        pass

    def __init__(self, layer = Enums.LayerType.Non):
        self.components : Dict[int, Component] = {}
        self.state = self.State.Alive
        self.layer = layer
        pass

    def Update(self):
        for component in self.components.values():
            component.Update()
        pass

    def LateUpdate(self):
        for component in self.components.values():
            component.LateUpdate()
        pass

    def Render(self):
        for component in self.components.values():
            component.Render()
        pass
 
    def AddComponent(self, component: Component) -> Component:
        component = component()
        component.SetOwner(self)
        self.components[component.GetType().value] = component
        return self.components[component.GetType().value]

    def SetComponent(self, component: Component) -> Component:
        component.SetOwner(self)
        self.components[component.GetType().value] = component
        return self.components[component.GetType().value]
    
    def GetComponent(self, component: Enums.ComponentType) -> Component | None:
        if component.value in self.components:
            component = self.components[component.value]
            return component
        else: return None

    def SetState(self, state): self.state = state
    def GetState(self): return self.state
    def SetLayer(self, layer): self.layer = layer
    def GetLayer(self): return self.layer

    pass