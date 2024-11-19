from pygame import Vector2

from framework.Common import Enums
from framework.Common.InputManager import inputManager
from framework.Common.StateMachine import StateMachine, State
from framework.Common.Timer import timer
from framework.Component.Script import Script
from framework.Component.Sprite import Sprite
from framework.Component.Transform import Transform

class Idle(State):
	@staticmethod
	def do():
		
		pass
	pass
class Move(State):
	
	pass

class LumberjackScript(Script):
	def __init__(self):
		super().__init__()
		self.speed : float = 100.0
		self.statemachine : StateMachine = StateMachine(self)
		self.statemachine.set_transitions(
			{
				Idle : {# 'Input', int | str -> inputManager.GetKeyDown
					inputManager.GetKeyDown: [Move]
				}
			}
		)
	
	def Update(self):
		tr : Transform = self.GetOwner().GetComponent(Enums.ComponentType.Transform)
		sp : Sprite = self.GetOwner().GetComponent(Enums.ComponentType.Sprite)
		move : bool = False
		if inputManager.GetKey('a'):
			if sp.curAction is not 'move': sp.SetAction('move'); sp.SetFlip('move','h')
			tr.SetPosition(tr.GetPosition() - Vector2(self.speed, 0) * timer.GetDeltaTime()); move = True
		if inputManager.GetKey('d'):
			if sp.curAction is not 'move': sp.SetAction('move'); sp.SetFlip('move','')
			tr.SetPosition(tr.GetPosition() + Vector2(self.speed, 0) * timer.GetDeltaTime()); move = True
		if inputManager.GetKey('s'):
			if sp.curAction is not 'move': sp.SetAction('move')
			tr.SetPosition(tr.GetPosition() - Vector2(0, self.speed) * timer.GetDeltaTime()); move = True
		if inputManager.GetKey('w'):
			if sp.curAction is not 'move': sp.SetAction('move')
			tr.SetPosition(tr.GetPosition() + Vector2(0, self.speed) * timer.GetDeltaTime()); move = True
		
		if not move and sp.curAction == 'move':
			sp.SetAction('idle')
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
