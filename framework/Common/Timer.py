import time


class Timer:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        cls = type(self)
        if hasattr(cls, "_init"): return

        self.__curTime = 0
        self.targetFPS = 144
        self.curFPS = 0
        self.prevTime = time.perf_counter()
        self.deltaTime = 0
        cls._init = True

    def Update(self):
        curTime = time.perf_counter()
        self.deltaTime = curTime - self.prevTime
        while self.deltaTime < 1.0 / self.targetFPS:
            curTime = time.perf_counter()
            self.deltaTime = curTime - self.prevTime
        self.prevTime = time.perf_counter()

        self.curFPS += 1
        self.__curTime += self.deltaTime
        if self.__curTime > 1.0:
            self.curFPS = 0
            self.__curTime = 0
        pass

    def GetDeltaTime(self): return self.deltaTime
    def GetCurrentFrameNum(self): return self.curFPS

    pass

timer = Timer()