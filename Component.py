from Enums import ComponentType


class Component:
    def __init__(self, type : ComponentType):
        from GameObject import GameObject
        self.ownerObject : GameObject = None
        self.type : ComponentType = type
        pass

    def Update(self):
        pass

    def LateUpdate(self):
        pass

    def Render(self):
        pass

    def GetOwner(self): return self.ownerObject
    def GetType(self): return self.type