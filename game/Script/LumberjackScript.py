from random import randint
from typing import Tuple

from pygame import Vector2

from framework.Common import Enums
from framework.Common.InputManager import inputManager
from framework.Common.StateMachine import StateMachine, State
from framework.Common.Timer import timer
from framework.Component.Script import Script
from framework.Component.Sprite import Sprite
from framework.Component.Transform import Transform
from framework.GameObject.GameObject import GameObject


def moveKeyDown(event : Tuple[str, int | str]):
	return event[0] is 'InputDown'\
		and event[1] in ('w', 'a', 's', 'd')\
		and inputManager.GetKeyDown(event[1])
def notMove(event : Tuple[str, int | str]):
	return event[0] is 'NotMove'
def endAnimation(event : Tuple[str, int | str]):
	return event[0] is 'EndAnimation'
def attackKeyDown(event : Tuple[str, int | str]):
	return event[0] is 'Attack'\
		and event[1] >= 20.0\
		and inputManager.GetKeyDown(inputManager.kMouseLeft)

class Idle(State):
	@staticmethod
	def enter(own, event):
		sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
		sp.SetAction('idle')
		pass
	
	@staticmethod
	def exit(own, event):
		pass
		
	@staticmethod
	def do(own):
		
		pass

class Move(State):
	@staticmethod
	def enter(own, event):
		# tr : Transform = own.GetComponent(Enums.ComponentType.Transform)
		sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
		sp.SetAction('move')
		if event[1] is 'a': sp.SetFlip('move', 'h')
		elif event[1] is 'd': sp.SetFlip('move', '')
		pass
	
	@staticmethod
	def exit(own, event):
		pass
	
	@staticmethod
	def do(own):
		tr : Transform = own.GetComponent(Enums.ComponentType.Transform)
		sc : LumberjackScript = own.GetComponent(Enums.ComponentType.Script)
		# delta : Vector2 = Vector2(1, 0).rotate(tr.GetRotation()) * sc.speed * timer.GetDeltaTime()
		# tr.SetPosition(tr.GetPosition() + delta)
		delta = Vector2()
		if inputManager.GetKey('w'):
			delta += Vector2(0, sc.speed)
		if inputManager.GetKey('a'):
			delta += Vector2(-sc.speed, 0)
		if inputManager.GetKey('s'):
			delta += Vector2(0, -sc.speed)
		if inputManager.GetKey('d'):
			delta += Vector2(sc.speed, 0)
		if delta == Vector2(0, 0):
			sc.statemachine.add_event(('NotMove', 0))
		elif delta.x > 0: own.GetComponent(Enums.ComponentType.Sprite).SetFlip('move', '')
		elif delta.x < 0: own.GetComponent(Enums.ComponentType.Sprite).SetFlip('move', 'h')
		tr.SetPosition(tr.GetPosition() + delta * timer.GetDeltaTime())
		pass

class Attack(State):
	@staticmethod
	def enter(own: GameObject, event: Tuple[str, int | str]):
		sc : LumberjackScript = own.GetComponent(Enums.ComponentType.Script)
		critical = randint(0, 10000)
		if critical < sc.hungry * 100 / 2:
			sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
			sp.SetAction('attack')
			sp.SetActionSpeed('attack', int(sc.hungry / 4))
		else:
			sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
			sp.SetAction('attackCritical')
			sp.SetActionSpeed('attackCritical', int(sc.hungry / 4))
			pass
		pass
	
	@staticmethod
	def exit(own: GameObject, event: Tuple[str, int | str]):
		pass
	
	@staticmethod
	def do(own: GameObject):
		sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
		if sp.action[sp.curAction].isComplete:
			sc : LumberjackScript = own.GetComponent(Enums.ComponentType.Script)
			
			inputDown = inputManager.GetKeyDown
			if inputDown('w'): sc.statemachine.add_event(('InputDown', 'w'))
			if inputDown('a'): sc.statemachine.add_event(('InputDown', 'a'))
			if inputDown('d'): sc.statemachine.add_event(('InputDown', 'd'))
			if inputDown('s'): sc.statemachine.add_event(('InputDown', 's'))
			sc.statemachine.add_event(('EndAnimation', 0))
		pass


class LumberjackScript(Script):
	def __init__(self):
		super().__init__()
		self.speed : float = 100.0
		self.hungry : float = 100.0
		self.statemachine : StateMachine = None
	
	def Init(self):
		self.statemachine = StateMachine(self.GetOwner(), Idle)
		self.statemachine.set_transitions(
			{
				Idle : {# 'Input', int | str -> inputManager.GetKeyDown(int | str) -> nextState[returnVal]
					moveKeyDown: Move, attackKeyDown: Attack
				},
				Move : {
					notMove: Idle, attackKeyDown: Attack
				},
				Attack : {
					endAnimation: Idle, moveKeyDown: Move
				},
			}
		)
	
	def Update(self):
		inputDown = inputManager.GetKeyDown
		if inputDown('w') : self.statemachine.add_event(('InputDown', 'w'))
		if inputDown('a') : self.statemachine.add_event(('InputDown', 'a'))
		if inputDown('d') : self.statemachine.add_event(('InputDown', 'd'))
		if inputDown('s') : self.statemachine.add_event(('InputDown', 's'))
		if inputDown(inputManager.kMouseLeft) :
			self.statemachine.add_event(('Attack', inputManager.kMouseLeft))
		self.statemachine.Update()
		pass
	
	def LateUpdate(self):
		pass
	
	def Render(self):
		pass
	
	def OnCollisionEnter(self, other: 'Collider'):
		pass
	
	def OnCollisionStay(self, other: 'Collider'):
		pass
	
	def OnCollisionExit(self, other: 'Collider'):
		pass
