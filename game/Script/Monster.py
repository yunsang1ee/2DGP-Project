from typing import Tuple

from pygame import Vector2

from framework.Common.StateMachine import StateMachine, State
from framework.Component.Collider.BoxCollider2D import BoxCollider2D
from framework.Component.Script import Script
from framework.Component.Sprite import Sprite
from framework.GameObject.GameObject import GameObject

def playerFound(event : Tuple[str, int | str]):
	return event[0] is 'PlayerFound'
def playerMissing(event : Tuple[str, int | str]):
	return event[0] is 'PlayerMissing'
def playerReached(event : Tuple[str, int | str]):
	return event[0] is 'PlayerReached'
def endAnimation(event : Tuple[str, int | str]):
	return event[0] is 'EndAnimation'

class Spawn(State):
	
	@staticmethod
	def enter(own: GameObject, event: Tuple[str, int | str]):
		pass
	
	@staticmethod
	def exit(own: GameObject, event: Tuple[str, int | str]):
		pass
	
	@staticmethod
	def do(own: GameObject):
		pass
	
class Idle(State):
	
	@staticmethod
	def enter(own: GameObject, event: Tuple[str, int | str]):
		pass
	
	@staticmethod
	def exit(own: GameObject, event: Tuple[str, int | str]):
		pass
	
	@staticmethod
	def do(own: GameObject):
		pass
	
class Attack(State):
	
	@staticmethod
	def enter(own: GameObject, event: Tuple[str, int | str]):
		pass
	
	@staticmethod
	def exit(own: GameObject, event: Tuple[str, int | str]):
		pass
	
	@staticmethod
	def do(own: GameObject):
		pass
	
class Move(State):
	
	@staticmethod
	def enter(own: GameObject, event: Tuple[str, int | str]):
		pass
	
	@staticmethod
	def exit(own: GameObject, event: Tuple[str, int | str]):
		pass
	
	@staticmethod
	def do(own: GameObject):
		pass


class ZombieScript(Script):
	def __init__(self):
		super().__init__()
		self.statemachine : StateMachine = None
		
	
	def Update(self):
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

	def Init(self):
		cd: BoxCollider2D = self.GetOwner().AddComponent(BoxCollider2D)
		cd.SetOffset(Vector2(0, -8))
		cd.SetSize(Vector2(0.72, 0.56))
		
		sp: Sprite = self.GetOwner().AddComponent(Sprite)
		sp.SetImage("Zombie.png")
		sp.AddAction('spawn', 0, 12, 3
		             , Vector2(65, 1211), Vector2(136, 72), '', repeat=False)
		sp.AddAction('idle', 0, 4, 6
		             , Vector2(65, 919), Vector2(72, 72), '')
		sp.AddAction('idle2', 0, 9, 6
		             , Vector2(65, 846), Vector2(72, 72), '')
		sp.AddAction('attack', 0, 7, 6
		             , Vector2(65, 700), Vector2(72, 72), '')
		sp.AddAction('death', 0, 9, 4
		             , Vector2(65, 554), Vector2(110, 72), '', repeat=False)
		sp.AddAction('move', 0, 8, 6
		             , Vector2(65, 74), Vector2(72, 72), '')

		self.statemachine = StateMachine(self.GetOwner(), Spawn)
		self.statemachine.set_transitions(
			{
				Spawn: {
					endAnimation : Idle
				},
				Idle: {
					playerFound: Move, playerReached: Attack
				},
				Move: {
					playerMissing: Idle, playerReached: Attack
				},
				Attack: {
					endAnimation: Idle, playerFound: Move
				},
			}
		)
	pass

class WarthogScript(Script):
	def __init__(self):
		super().__init__()
		self.statemachine : StateMachine = None
		pass
	
	def Update(self):
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
	
	def Init(self):
		cd: BoxCollider2D = self.GetOwner().AddComponent(BoxCollider2D)
		cd.SetOffset(Vector2(0, -8))
		cd.SetSize(Vector2(0.72, 0.56))
		
		sp: Sprite = self.GetOwner().AddComponent(Sprite)
		sp.SetImage("Warthog.png")
		sp.AddAction('idle', 0, 6, 6
		             , Vector2(65, 585), Vector2(72, 72), '')
		sp.AddAction('move', 0, 8, 6
		             , Vector2(65, 512), Vector2(72, 72), '')
		sp.AddAction('attack', 0, 6, 6
		             , Vector2(65, 366), Vector2(72, 72), '')
		sp.AddAction('special', 0, 8, 6
		             , Vector2(65, 293), Vector2(72, 72), '', repeat=False)
		sp.AddAction('death', 0, 10, 4
		             , Vector2(65, 147), Vector2(102, 72), '', repeat=False)
	
	pass

class BossScript(Script):
	def __init__(self):
		super().__init__()
		self.statemachine : StateMachine = None
		pass
	
	def Update(self):
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
	
	pass