from pico2d import *
from pygame import Vector2

from Scene import Scene
from InputManager import inputManager
from Timer import timer


class Application:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        cls = type(self)
        if hasattr(cls, "_init"): return

        self.screen : Vector2 = Vector2()
        self.__scenes : dict[str, Scene] = {}
        self.activeScene : Scene = None
        cls._init = True

    def Init(self, width, height):
        self.screen = width, height
        pass

    def HandleEvents(self):
        events = get_events()
        if len(events) == 0: return False

        for event in events:
            if event.type == SDL_QUIT:
                sys.exit()
            elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                sys.exit()
            else:
                inputManager.EventProcessing(event)
        return True

    def Run(self):
        self.HandleEvents()

        inputManager.BeforeUpdate()
        timer.Update()
        timer.GetDeltaTime()
        print(timer.GetCurrentFrameNum())
        self.Update()
        self.LateUpdate()
        self.Render()
        self.Destroy()
        inputManager.AfterUpdate()
        pass

    def Update(self):
        self.activeScene.Update()

        pass

    def LateUpdate(self):
        self.activeScene.LateUpdate()
        pass

    def Render(self):
        self.activeScene.Render()
        pass

    def Destroy(self):
        self.activeScene.Destroy()
        pass

    def Release(self):
        pass

    def CreateScene(self, name, scene : Scene):
        if(self.__scenes.get(name) != None): sys.exit("Exist this key")

        self.__scenes[name] = scene
        pass

    def LoadScene(self, name):
        if(self.__scenes.get(name) == None): sys.exit("Not found scene")

        if(self.activeScene != None): self.activeScene.OnExit()
        self.activeScene = self.__scenes[name]
        self.activeScene.OnEnter()
        pass

app = Application()