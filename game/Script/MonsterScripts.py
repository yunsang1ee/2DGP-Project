import random
from abc import ABC, abstractmethod
from random import randint
from typing import Tuple

from pygame import Vector2

from framework.Common import Enums, Object
from framework.Common.StateMachine import StateMachine, State
from framework.Common.Timer import timer
from framework.Component.Collider.BoxCollider2D import BoxCollider2D
from framework.Component.Script import Script
from framework.Component.Sprite import Sprite
from framework.Component.Transform import Transform
from framework.GameObject.GameObject import GameObject
from game.Script.LumberjackScript import AttackTrigger
from game.Script.SuppliesScript import EnergyEggScript


def playerFound(event : Tuple[str, int | str]):
	return event[0] == 'PlayerFound'
def playerMissing(event : Tuple[str, int | str]):
	return event[0] == 'PlayerMissing'
def reached(event : Tuple[str, int | str]):
	return event[0] == 'Reached'
def damaged(event : Tuple[str, int]):
	return event[0] == 'Damaged'
def endAnimation(event : Tuple[str, int | str]):
	return event[0] == 'EndAnimation'

class Spawn(State):
	
	@staticmethod
	def enter(own: GameObject, event: Tuple[str, int | str]):
		sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
		sp.SetAction('spawn')
		
		pass
	
	@staticmethod
	def exit(own: GameObject, event: Tuple[str, int | str]):
		pass
	
	@staticmethod
	def do(own: GameObject):
		sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
		if sp.action[sp.curAction].isComplete:
			sc : ZombieScript = own.GetComponent(Enums.ComponentType.Script)
			sc.statemachine.add_event(('EndAnimation', 0))
		pass
	
class Idle(State):
	@staticmethod
	def enter(own: GameObject, event: Tuple[str, int | str]):
		sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
		sp.SetAction('idle')
		pass
	
	@staticmethod
	def exit(own: GameObject, event: Tuple[str, int | str]):
		pass
	
	@staticmethod
	def do(own: GameObject):
		from framework.Application import app
		playerPos : Vector2 = app.activeScene.player.GetComponent(Enums.ComponentType.Transform).GetPosition()
		myPos : Vector2 = own.GetComponent(Enums.ComponentType.Transform).GetPosition()
		
		sc : MonsterScript = own.GetComponent(Enums.ComponentType.Script)
		sc.randMoveTimer.x += timer.GetDeltaTime()
		if (playerPos - myPos).length() <= sc.speed * 10.0:
			sc.statemachine.add_event(('PlayerFound', True))
		elif sc.randMoveTimer.x >= sc.randMoveTimer.y:
			sc.statemachine.add_event(('PlayerFound', False))
		pass
	
class Move(State):
	
	@staticmethod
	def enter(own: GameObject, event: Tuple[str, int | str]):
		sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
		sc : MonsterScript = own.GetComponent(Enums.ComponentType.Script)
		
		sp.SetAction('move')
		sc.randMoveTimer.x = 0.0
		if event[1] is True:
			sc.randMoveDir = None
		else:
			sc.randMoveDir = Vector2(1.0, 0.0).rotate(random.uniform(0.0, 360.0))
			if sc.randMoveDir.x < 0: sp.SetAllFlip('h')
			else: sp.SetAllFlip('')
		pass
	
	@staticmethod
	def exit(own: GameObject, event: Tuple[str, int | str]):
		pass
	
	@staticmethod
	def do(own: GameObject):
		sc : MonsterScript = own.GetComponent(Enums.ComponentType.Script)
		tr : Transform = own.GetComponent(Enums.ComponentType.Transform)
		sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
		
		from framework.Application import app
		playerPos : Vector2 = app.activeScene.player.GetComponent(Enums.ComponentType.Transform).GetPosition()
		myPos : Vector2 = tr.GetPosition()
		distVec : Vector2 = playerPos - myPos
	
		if sc.randMoveDir is None:
			if distVec.length() <= sc.speed * 10.0:
				if playerPos.x < myPos.x: sp.SetAllFlip('h')
				else: sp.SetAllFlip('')
				tr.SetPosition(myPos + distVec.normalize() * sc.speed * timer.GetDeltaTime())
			else:
				sc.statemachine.add_event(('PlayerMissing', 0))
		else:
			sc.randMoveTimer.x += timer.GetDeltaTime()
			if sc.randMoveTimer.x >= sc.randMoveTimer.y:
				sc.randMoveTimer.x = 0.0
				sc.randMoveTimer.y = random.uniform(0.5, 2.0)
				sc.statemachine.add_event(('PlayerMissing', 0))
			else:
				tr.SetPosition(myPos + sc.randMoveDir.normalize() * sc.speed * timer.GetDeltaTime())
				if (playerPos - myPos).length() <= sc.speed * 10.0:
					sc.randMoveTimer.x = 0.0
					sc.statemachine.add_event(('PlayerFound', True))
				
		pass
	
class Attack(State): #TODO: BossAttack special processing
	@staticmethod
	def enter(own: GameObject, event: Tuple[str, int | str]):
		sc : MonsterScript = own.GetComponent(Enums.ComponentType.Script)
		sp = own.GetComponent(Enums.ComponentType.Sprite)
		if sp.name == 'boss':
			pass
		else:
			sp.SetAction('attack')
		pass
	
	@staticmethod
	def exit(own: GameObject, event: Tuple[str, int | str]):
		sc : MonsterScript = own.GetComponent(Enums.ComponentType.Script)
		sc.attackTrigger = None
		pass
	
	@staticmethod
	def do(own: GameObject):
		sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
		sc : MonsterScript = own.GetComponent(Enums.ComponentType.Script)
		if sc.attackTrigger not in (None, True):
			Object.Destroy(sc.attackTrigger)
			sc.attackTrigger = True
		if sp.action[sp.curAction].isComplete:
			sc.statemachine.add_event(('EndAnimation', 0))
		elif sp.action[sp.curAction].curFrame > sp.action[sp.curAction].frameCount // 2 and sc.attackTrigger is None:
			tr : Transform = own.GetComponent(Enums.ComponentType.Transform)
			size : Vector2 = Vector2(0.3, 0.62)
			offset : Vector2 = Vector2(40, 0)
			offsetFactor : float = 1 if sp.action[sp.curAction].flip == '' else -1
			triggerPosition : Vector2 = tr.GetPosition() + offset * offsetFactor
			
			sc.attackTrigger : AttackTrigger = Object.Instantiate(AttackTrigger, Enums.LayerType.EnemyAttackTrigger,  triggerPosition)
			sc.attackTrigger.damage = sc.damage
			cd : BoxCollider2D = sc.attackTrigger.AddComponent(BoxCollider2D)
			cd.SetSize(size)
			cd.SetOffset(own.GetComponent(Enums.ComponentType.Collider).GetOffset())
		pass

class Damaged(State):
	damagedTimer : Vector2 = Vector2(0, 0.1)
	@staticmethod
	def enter(own: GameObject, event: Tuple[str, int | str]):
		sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
		if event[1] <= 0.0:
			if sp.name == 'Warthog' and randint(1, 10000) <= 10000:
				sp.SetAction('special')
			else:
				sp.SetAction('death')
		else:
			sp.SetAction('idle')
			sp.image.opacify(0.7)
		pass
	
	@staticmethod
	def exit(own: GameObject, event: Tuple[str, int | str]):
		pass
	
	@staticmethod
	def do(own: GameObject):
		sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
		if sp.action[sp.curAction].isComplete:
			from framework.Application import app
			from game.Scene.mainScene import MainScene
			if sp.curAction == 'death':
				scene : MainScene = app.activeScene
				own.SetState(GameObject.State.Paused)
				sc = own.GetComponent(Enums.ComponentType.Script)
				if sc is ZombieScript : scene.ReturnZombie(own)
				elif sc is WarthogScript : scene.ReturnWarthog(own)
			elif sp.curAction == 'special':
				tr : Transform = own.GetComponent(Enums.ComponentType.Transform)
				egg = Object.Instantiate(GameObject, Enums.LayerType.Supplies, tr.GetPosition())
				sc = egg.AddComponent(EnergyEggScript); sc.Init()

				own.SetState(GameObject.State.Paused)
				scene : MainScene = app.activeScene
				scene.ReturnWarthog(own)
				pass
			else:
				Damaged.damagedTimer.x += timer.GetDeltaTime()
				if Damaged.damagedTimer.x >= Damaged.damagedTimer.y:
					Damaged.damagedTimer.x = 0.0
					sc = own.GetComponent(Enums.ComponentType.Script)
					sp.image.opacify(1.0)
					sc.statemachine.add_event(('EndAnimation', 0))
		pass


class MonsterScript(Script, ABC):
	def __init__(self, health : float, speed : float, damage : float):
		super().__init__()
		self.health : float = health
		self.speed : float = speed
		self.damage : float = damage
		self.attackTrigger : AttackTrigger | bool | None = None
		self.randMoveTimer : Vector2 = Vector2(0, 0.5)
		self.randMoveDir : Vector2 | None = None
	@abstractmethod
	def Init(self):
		pass
	pass

class ZombieScript(MonsterScript):
	def __init__(self):
		super().__init__(20.0, 30.0, 7.0)
		self.statemachine : StateMachine = None
		
	
	def Update(self):
		self.statemachine.Update()
		pass
	
	def LateUpdate(self):
		pass
	
	def Render(self):
		pass
	
	def OnCollisionEnter(self, other: 'Collider'):
		from game.Script.LumberjackScript import AttackTrigger
		otherObj : GameObject | AttackTrigger = other.GetOwner()
		
		if otherObj.GetLayer() == Enums.LayerType.AttackTrigger and self.statemachine.cur_state is not Damaged:
			self.health -= otherObj.damage
			self.statemachine.add_event(('Damaged', self.health))
		pass
	
	def OnCollisionStay(self, other: 'Collider'):
		from game.Script.LumberjackScript import AttackTrigger
		otherObj : GameObject | AttackTrigger = other.GetOwner()
		if otherObj.GetLayer() == Enums.LayerType.Player or otherObj.GetLayer() == Enums.LayerType.Obstacle:
			self.statemachine.add_event(('Reached', 0))
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
		             , Vector2(65, 1429), Vector2(136, 72), '', repeat=False)
		sp.AddAction('idle', 0, 4, 6
		             , Vector2(65, 1137), Vector2(72, 72), '')
		sp.AddAction('attack', 0, 7, 6
		             , Vector2(65, 918), Vector2(72, 72), '')
		sp.AddAction('death', 0, 9, 4
		             , Vector2(65, 772), Vector2(110, 72), '', repeat=False)
		sp.AddAction('move', 0, 8, 6
		             , Vector2(65, 74), Vector2(72, 72), '')

		self.statemachine = StateMachine(self.GetOwner(), Spawn)
		self.statemachine.set_transitions(
			{
				Spawn: {
					endAnimation : Idle
				},
				Idle: {
					playerFound: Move, reached: Attack, damaged: Damaged
				},
				Move: {
					playerMissing: Idle, playerFound: Move, reached: Attack, damaged: Damaged
				},
				Attack: {
					endAnimation: Idle, playerFound: Move, damaged: Damaged
				},
				Damaged: {
					endAnimation: Idle
				}
			}
		)
		pass
	
	def Regen(self):
		sp: Sprite = self.GetOwner().GetComponent(Enums.ComponentType.Sprite)
		sp.SetAction('spawn')
		self.health = 20.0 * (1 + timer.GetRunTime() * (1 / 600))
		self.damage = 7.0 * (1 + timer.GetRunTime() * (0.5 / 600))
		pass
	
	pass

class WarthogScript(MonsterScript):
	def __init__(self):
		super().__init__(40.0, 30.0, 7.0)
		self.statemachine : StateMachine = None
		pass
	
	def Update(self):
		self.statemachine.Update()
		pass
	
	def LateUpdate(self):
		pass
	
	def Render(self):
		pass
	
	def OnCollisionEnter(self, other: 'Collider'):
		from game.Script.LumberjackScript import AttackTrigger
		otherObj : GameObject | AttackTrigger = other.GetOwner()
		
		if otherObj.GetLayer() == Enums.LayerType.AttackTrigger and self.statemachine.cur_state is not Damaged:
			self.health -= otherObj.damage
			self.statemachine.add_event(('Damaged', self.health))
		pass
	
	def OnCollisionStay(self, other: 'Collider'):
		from game.Script.LumberjackScript import AttackTrigger
		otherObj : GameObject | AttackTrigger = other.GetOwner()
		if otherObj.GetLayer() == Enums.LayerType.Player or otherObj.GetLayer() == Enums.LayerType.Obstacle:
			self.statemachine.add_event(('Reached', 0))
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

		self.statemachine = StateMachine(self.GetOwner(), Idle)
		self.statemachine.set_transitions(
			{
				Idle: {
					playerFound: Move, reached: Attack, damaged: Damaged
				},
				Move: {
					playerMissing: Idle, playerFound: Move, reached: Attack, damaged: Damaged
				},
				Attack: {
					endAnimation: Idle, playerFound: Move, damaged: Damaged
				},
				Damaged: {
					endAnimation: Idle
				}
			}
		)
		pass
	
	def Regen(self):
		sp: Sprite = self.GetOwner().GetComponent(Enums.ComponentType.Sprite)
		sp.SetAction('idle')
		self.health = 40.0 * (1 + timer.GetRunTime() * (1 / 600))
		self.damage = 7.0 * (1 + timer.GetRunTime() * (0.5 / 600))
		pass
	
	pass

class BossScript(MonsterScript):
	def __init__(self):
		super().__init__(500.0, 15.0, 15.0)
		self.statemachine : StateMachine = None
		pass
	
	def Update(self):
		self.statemachine.Update()
		pass
	
	def LateUpdate(self):
		pass
	
	def Render(self):
		pass
	
	def OnCollisionEnter(self, other: 'Collider'):
		from game.Script.LumberjackScript import AttackTrigger
		otherObj : GameObject | AttackTrigger = other.GetOwner()
		if otherObj.GetLayer() == Enums.LayerType.Player or otherObj.GetLayer() == Enums.LayerType.Obstacle:
			self.statemachine.add_event(('Reached', 0))
		
		elif otherObj.GetLayer() == Enums.LayerType.AttackTrigger:
			self.health -= otherObj.damage
			self.statemachine.add_event(('Damaged', self.health))
		pass
	
	def OnCollisionStay(self, other: 'Collider'):
		pass
	
	def OnCollisionExit(self, other: 'Collider'):
		pass
	
	def Init(self):
		pass

	def Regen(self):
		sp: Sprite = self.GetOwner().GetComponent(Enums.ComponentType.Sprite)
		sp.SetAction('idle')
		self.health = 250.0 * (1 + timer.GetRunTime() * (1 / 600))
		self.damage = 10.0 * (1 + timer.GetRunTime() * (0.5 / 600))
		pass
	
	