import enum

import Enums
from Component import Component


class GameObject:
    class State(enum.Enum):
        Alive = 0; Paused = 1; Dead = 2
        pass


    def __init__(self, layer = Enums.LayerType.Non):
        self.components : list[Component] = [None for _ in range(Enums.ComponentType.End.value)]
        self.state = self.State.Alive
        self.layer = layer
        pass

    def Update(self):
        for component in self.components:
            if component is None: continue
            component.Update()
        pass

    def LateUpdate(self):
        for component in self.components:
            if component is None: continue
            component.LateUpdate()
        pass

    def Render(self):
        for component in self.components:
            if component is None: continue
            component.Render()
        pass

    def SetState(self, state): self.state = state
    def GetState(self): return self.state
    def SetLayer(self, layer): self.layer = layer
    def GetLayer(self): return self.layer

    pass