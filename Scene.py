import GameObject

# Layer by layer CollisionCheck
class Scene:
    def __init__(self):
        self.objects = []

        pass

    def Update(self):
        for obj in self.objects: obj.Update()
        pass

    def LateUpdate(self):
        for obj in self.objects: obj.LateUpdate()
        pass

    def Render(self):
        #self.objects.sort()
        for obj in self.objects: obj.Render()
        pass

    def Destroy(self):
        for obj in self.objects: obj.Destroy()
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