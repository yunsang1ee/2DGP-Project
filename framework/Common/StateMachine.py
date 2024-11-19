from abc import abstractmethod, ABC
from typing import *


class State(ABC):
    @staticmethod
    @abstractmethod
    def do():
        pass
    pass


class StateMachine:
    def __init__(self, o):
        self.cur_state : State
        self.transitions : Dict[Type[State], Dict[Callable[..., int], List[Type[State]]]] = {}
        self.o = o
        self.event_que = []

    def start(self, state):
        self.cur_state = state

        print(f'Enter into {state}')
        self.cur_state.enter(self.o, ('START', 0))

    def add_event(self, e):
        self.event_que.append(e)

    def set_transitions(self, transitions: Dict[Type[State], Dict[Callable[..., int], List[Type[State]]]]):
        self.transitions : Dict[Type[State], Dict[Callable[..., int], List[Type[State]]]] = transitions

    def update(self):
        self.cur_state.do(self.o)
        if self.event_que:
            event = self.event_que.pop(0)
            self.handle_event(event)

    # def draw(self):
    #     self.cur_state.draw(self.o)

    def handle_event(self, e):
        for event, next_state in self.transitions[self.cur_state].items():
            if event(e):
                print(f'Exit from {self.cur_state}')
                self.cur_state.exit(self.o, e)
                self.cur_state = next_state
                print(f'Enter into {self.cur_state}')
                self.cur_state.enter(self.o, e)
                return
