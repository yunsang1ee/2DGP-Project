from Scene import Scene


class Application:
    def __init__(self):
        self.scenes : dict[str, Scene] = {}
        pass

    def Init(self):
        pass

    def Input(self):

        pass

    def Run(self):
        self.Update()
        self.LateUpdate()
        self.Render()
        self.Destroy()
        pass

    def Update(self):

        pass

    def LateUpdate(self):

        pass

    def Render(self):

        pass

    def Destroy(self):

        pass

    def Release(self):

        pass

    def CreateScene(self, name, scene):
        self.scenes[name] = scene
        pass

    def LoadScene(self, name, scene):
        self.scenes[name] = scene
        pass

app = Application()