from abc import abstractmethod

from framework.Common import Enums
from framework.GameObject import GameObject


# Layer by layer CollisionCheck
class Scene:
    def __init__(self):
        self.objects : list[GameObject] = []
        pass

    @abstractmethod
    def Update(self):
        for obj in self.objects:
            if obj.GetState() is GameObject.GameObject.State.Alive:
                obj.Update()
        pass

    @abstractmethod
    def LateUpdate(self):
        for obj in self.objects:
            if obj.GetState() is GameObject.GameObject.State.Alive:
                obj.LateUpdate()
        pass

    @abstractmethod
    def Render(self):
        #self.objects.sort()
        for obj in self.objects:
            if obj.GetState() is GameObject.GameObject.State.Alive:
                obj.Render()
        pass

    @abstractmethod
    def Destroy(self):
        for obj in self.objects:
            if obj.GetState() is GameObject.GameObject.State.Dead:
                self.objects.remove(obj)
        pass

    @abstractmethod
    def OnEnter(self):
        pass

    @abstractmethod
    def OnExit(self):
        pass
  
    def AddObject(self, obj):
        if isinstance(obj, GameObject.GameObject):
            self.objects.append(obj)
        else:
            print("Object is not a GameObject")
        pass

    def EraseObject(self, obj):
        if isinstance(obj, GameObject.GameObject):
            self.objects.remove(obj)
        else:
            print("Object is not a GameObject")
        pass

    def GetGameObjects(self, layer : Enums.LayerType) -> list[GameObject]:
        return [obj for obj in self.objects if obj.GetLayer() == layer]

    pass