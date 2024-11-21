from abc import abstractmethod, ABC
from typing import *

from framework.GameObject.GameObject import GameObject


class State(ABC):
    @staticmethod
    @abstractmethod
    def enter(own : GameObject, event : Tuple[str, int | str]):
        pass
    @staticmethod
    @abstractmethod
    def exit(own : GameObject, event : Tuple[str, int | str]):
        pass
    @staticmethod
    @abstractmethod
    def do(own : GameObject):
        pass
    pass


class StateMachine:
    def __init__(self, o, state):
        self.o = o
        self.cur_state : State = state
        self.cur_state.enter(self.o, ('start', 0))
        self.transitions : Dict[Type[State], Dict[Callable[..., int], Type[State]]] = {}
        self.event_que = []

    def add_event(self, e):
        self.event_que.append(e)

    def set_transitions(self, transitions: Dict[Type[State], Dict[Callable[..., int], Type[State]]]):
        self.transitions : Dict[Type[State], Dict[Callable[..., int], Type[State]]] = transitions

    def Update(self):
        self.cur_state.do(self.o)
        if self.event_que:
            event = self.event_que.pop(0)
            self.handle_event(event)

    # def draw(self):
    #     self.cur_state.draw(self.o)

    def handle_event(self, e):
        for event, next_state in self.transitions[self.cur_state].items():
            if event(e):
                self.cur_state.exit(self.o, e)
                self.cur_state = next_state
                self.cur_state.enter(self.o, e)
                return
