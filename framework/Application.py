from pico2d import *
from pygame import Vector2

from framework.Component.Camera import Camera
from framework.Component.Collider.CollisionManager import CollisionManager
from framework.Scene import Scene
from framework.Common.InputManager import inputManager
from framework.Common.Timer import timer


def HandleEvents():
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
        self.running : bool = True
        cls._init = True

    def Init(self, width, height):
        self.screen = Vector2(width, height)
        pass
    
    def Run(self):
        HandleEvents() # Event Processing

        inputManager.BeforeUpdate()         # Input PreProcessing
        timer.Update()                      # Target Frame Lock

        self.Update()
        self.LateUpdate()
        self.Render()
        self.Destroy()

        inputManager.AfterUpdate()          # Input PostProcessing
        pass

    def Update(self):
        CollisionManager.Update()
        self.activeScene.Update()
        pass

    def LateUpdate(self):
        CollisionManager.LateUpdate()
        self.activeScene.LateUpdate()
        pass

    def Render(self):
        clear_canvas()
        CollisionManager.Render()
        self.activeScene.Render()
        update_canvas()
        pass

    def Destroy(self):
        self.activeScene.Destroy()
        pass

    def Release(self):
        pass

    def CreateScene(self, name, scene : Scene):
        if self.__scenes.get(name) is not None: sys.exit("Exist this key")

        self.__scenes[name] = scene
        pass

    def LoadScene(self, name):
        if self.__scenes.get(name) is None: sys.exit("Not found scene")

        if self.activeScene is not None: self.activeScene.OnExit()
        self.activeScene = self.__scenes[name]
        self.activeScene.OnEnter()
        pass
    
    def Close(self):
        self.running = False

app = Application()
mainCamera : Camera = None