import GameObject

# Layer by layer CollisionCheck
class Scene:
    def __init__(self):
        self.objects : list[GameObject] = []
        pass

    def Update(self):
        for obj in self.objects:
            if obj.GetState() is GameObject.GameObject.State.Alive:
                obj.Update()
        pass

    def LateUpdate(self):
        for obj in self.objects:
            if obj.GetState() is GameObject.GameObject.State.Alive:
                obj.LateUpdate()
        pass

    def Render(self):
        #self.objects.sort()
        for obj in self.objects:
            if obj.GetState() is GameObject.GameObject.State.Alive:
                obj.Render()
        pass

    def Destroy(self):
        for obj in self.objects:
            if obj.GetState() is GameObject.GameObject.State.Dead:
                self.objects.remove(obj)
        pass

    def AddObject(self, obj):
        if isinstance(obj, GameObject):
            self.objects.append(obj)
        else:
            print("Object is not a GameObject")
        pass

    def EraseObject(self, obj):
        if isinstance(obj, GameObject):
            self.objects.remove(obj)
        else:
            print("Object is not a GameObject")
        pass


    pass