import enum
import Enums


class GameObject:
    class State(enum.Enum):
        Alive = 0; Paused = 1; Dead = 2
        pass


    def __init__(self, layer = Enums.LayerType.Non):
        self.state = self.State.Alive
        self.layer = layer
        pass

    def Update(self):

        pass

    def LateUpdate(self):

        pass

    def Render(self):

        pass

    def Destroy(self):

        pass

    def SetState(self, state): self.state = state
    def GetState(self): return self.state
    def SetLayer(self, layer): self.layer = layer
    def GetLayer(self): return self.layer

    pass