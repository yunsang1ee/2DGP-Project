from typing import Final

from pico2d import *
from pygame import Vector2


class InputManager:
    kMouseLeft : Final = 352
    kMouseMiddle : Final = 353
    kMouseRight : Final = 354

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            self.__keys : list[int] = [0b0000 for _ in range(355)]
            self.__mousePosition : Vector2 = Vector2(0,0)
            cls._init = True
        pass

    class KeyState:
        kDownBit : Final = 0b0001
        kPressedBit : Final = 0b0010
        kUpBit : Final = 0b0100
        pass

    def keyCodeOffset(self, code : int | str):
        if type(code) == str: return ord(code)
        if type(code) != int:
            assert code
        if code > len(self.__keys):
            code &= 0x01FF
            code = 128 + (code - 0x0039)
        return code

    def GetKeyDown(self, code : int | str):
        code = self.keyCodeOffset(code)
        return self.__keys[code] & InputManager.KeyState.kDownBit != 0

    def GetKey(self, code : int | str):
        code = self.keyCodeOffset(code)
        return self.__keys[code] & InputManager.KeyState.kPressedBit != 0

    def GetKeyUp(self, code : int | str):
        code = self.keyCodeOffset(code)
        return self.__keys[code] & InputManager.KeyState.kUpBit != 0

    def BeforeUpdate(self):
        for index in range(len(self.__keys)):
            if self.GetKeyDown(index):
               self.__keys[index] |= InputManager.KeyState.kPressedBit
            if self.GetKeyUp(index):
                self.__keys[index] &= (~InputManager.KeyState.kPressedBit)
        pass

    def AfterUpdate(self):
        for index in range(len(self.__keys)):
            if self.GetKeyDown(index):
                self.__keys[index] &= (~InputManager.KeyState.kDownBit)
            if self.GetKeyUp(index):
                self.__keys[index] &= (~InputManager.KeyState.kPressedBit)
                self.__keys[index] &= (~InputManager.KeyState.kUpBit)
        pass

    def EventProcessing(self, event : Event):
        if event.type == SDL_KEYDOWN and event.key is not None:
            self.__keys[self.keyCodeOffset(event.key)] |= InputManager.KeyState.kDownBit
        elif event.type == SDL_KEYUP and event.key is not None:
            self.__keys[self.keyCodeOffset(event.key)] |= InputManager.KeyState.kUpBit
        elif event.type == SDL_MOUSEBUTTONDOWN:
            self.__keys[351 + event.button] |= InputManager.KeyState.kDownBit
        elif event.type == SDL_MOUSEBUTTONUP:
            self.__keys[351 + event.button] |= InputManager.KeyState.kUpBit
        elif event.type == SDL_MOUSEMOTION:
            from framework.Application import app
            self.__mousePosition = event.x, app.screen.y - event.y
        pass
    pass


inputManager = InputManager()