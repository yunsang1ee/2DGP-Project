from random import randint
from typing import Tuple

from pygame import Vector2

from framework.Common import Enums, Object
from framework.Common.InputManager import inputManager
from framework.Common.StateMachine import StateMachine, State
from framework.Common.Timer import timer
from framework.Component.Collider import Collider
from framework.Component.Collider.BoxCollider2D import BoxCollider2D
from framework.Component.Script import Script
from framework.Component.Sprite import Sprite
from framework.Component.Transform import Transform
from framework.GameObject.GameObject import GameObject


def moveKeyDown(event : Tuple[str, int | str]):
	return event[0] is 'InputDown'\
		and event[1] in ('w', 'a', 's', 'd')\
		and inputManager.GetKeyDown(event[1])
def moveKeyPressed(event : Tuple[str, int | str]):
	return event[0] is 'InputPressed'\
		and event[1] in ('w', 'a', 's', 'd')\
		and inputManager.GetKey(event[1])
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
		sc : LumberjackScript = own.GetComponent(Enums.ComponentType.Script)
		sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
		sp.SetAction('move')
		sp.SetActionSpeed('move', int(sc.hungry / 10))
		flip : str = 'None'
		if event[1] is 'a': flip = 'h'
		elif event[1] is 'd': flip = ''
		if flip is not 'None':
			sp.SetFlip('idle', flip)
			sp.SetFlip('move', flip)
			sp.SetFlip('attack', flip)
			sp.SetFlip('attackCritical', flip)
		pass
	
	@staticmethod
	def exit(own, event):
		pass
	
	@staticmethod
	def do(own):
		tr : Transform = own.GetComponent(Enums.ComponentType.Transform)
		sc : LumberjackScript = own.GetComponent(Enums.ComponentType.Script)
		sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
		# delta : Vector2 = Vector2(1, 0).rotate(tr.GetRotation()) * sc.speed * timer.GetDeltaTime()
		# tr.SetPosition(tr.GetPosition() + delta)
		delta = Vector2()
		if inputManager.GetKey('w'):
			delta += Vector2(0, sc.hungry)
		if inputManager.GetKey('a'):
			delta += Vector2(-sc.hungry, 0)
		if inputManager.GetKey('s'):
			delta += Vector2(0, -sc.hungry)
		if inputManager.GetKey('d'):
			delta += Vector2(sc.hungry, 0)
			
		flip : str = 'None'
		if delta == Vector2(0, 0):
			sc.statemachine.add_event(('NotMove', 0))
		elif delta.x > 0: flip = ''
		elif delta.x < 0: flip = 'h'
		if flip is not 'None':
			sp.SetFlip('idle', flip)
			sp.SetFlip('move', flip)
			sp.SetFlip('attack', flip)
			sp.SetFlip('attackCritical', flip)
		tr.SetPosition(tr.GetPosition() + delta * timer.GetDeltaTime())
		pass

class Attack(State):
	AttackTrigger : GameObject = None
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
			if Attack.AttackTrigger is not None:
				Object.Destroy(Attack.AttackTrigger)
				Attack.AttackTrigger = None
			
			sc : LumberjackScript = own.GetComponent(Enums.ComponentType.Script)
			inputPressed = inputManager.GetKey
			if inputPressed('w'): sc.statemachine.add_event(('InputPressed', 'w'))
			elif inputPressed('a'): sc.statemachine.add_event(('InputPressed', 'a'))
			elif inputPressed('d'): sc.statemachine.add_event(('InputPressed', 'd'))
			elif inputPressed('s'): sc.statemachine.add_event(('InputPressed', 's'))
			else: sc.statemachine.add_event(('EndAnimation', 0))
		elif sp.action[sp.curAction].curFrame <= sp.action[sp.curAction].frameCount // 2:
			inputDown = inputManager.GetKeyDown
			flip: str = 'None'
			if inputDown('a'): flip = 'h'
			elif inputDown('d'): flip = ''
			if flip is not 'None':
				sp.SetFlip('idle', flip)
				sp.SetFlip('move', flip)
				sp.SetFlip('attack', flip)
				sp.SetFlip('attackCritical', flip)
		elif Attack.AttackTrigger is None:
			tr : Transform = own.GetComponent(Enums.ComponentType.Transform)
			size : Vector2 = Vector2(0.3, 0.62)
			offset : Vector2 = Vector2(40, 0)
			if sp.curAction is 'attackCritical': offset.x += size.x * 50; size *= 1.5
			offsetFactor : float = 1 if sp.action[sp.curAction].flip is '' else -1
			triggerPosition : Vector2 = tr.GetPosition() + offset * offsetFactor
			Attack.AttackTrigger = Object.Instantiate(Enums.LayerType.AttackTrigger, triggerPosition)
			cd : BoxCollider2D = Attack.AttackTrigger.AddComponent(BoxCollider2D)
			cd.SetSize(size)
			cd.SetOffset(own.GetComponent(Enums.ComponentType.Collider).GetOffset())
		pass


class LumberjackScript(Script):
	def __init__(self):
		super().__init__()
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
					endAnimation: Idle, moveKeyPressed: Move
				},
			}
		)

	def Update(self):
		inputDown = inputManager.GetKeyDown
		if inputDown('w') : self.statemachine.add_event(('InputDown', 'w'))
		elif inputDown('a') : self.statemachine.add_event(('InputDown', 'a'))
		elif inputDown('d') : self.statemachine.add_event(('InputDown', 'd'))
		elif inputDown('s') : self.statemachine.add_event(('InputDown', 's'))
		if inputDown(inputManager.kMouseLeft):
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
