from random import randint
from typing import Tuple

from pygame import Vector2

from framework.Common import Enums, Object
from framework.Common.InputManager import inputManager
from framework.Common.StateMachine import StateMachine, State
from framework.Common.Timer import timer
from framework.Component.Collider import Collider
from framework.Component.Collider.BoxCollider2D import BoxCollider2D
from framework.Component.Collider.CollisionManager import CollisionManager
from framework.Component.Script import Script
from framework.Component.Sprite import Sprite
from framework.Component.Transform import Transform
from framework.GameObject.GameObject import GameObject


def moveKeyDown(event : Tuple[str, int | str]):
	return event[0] == 'InputDown'\
		and event[1] in ('w', 'a', 's', 'd')\
		and inputManager.GetKeyDown(event[1])
def moveKeyPressed(event : Tuple[str, int | str]):
	return event[0] == 'InputPressed'\
		and event[1] in ('w', 'a', 's', 'd')\
		and inputManager.GetKey(event[1])
def itemUse(event : Tuple[str, int | str]):
	return event[0] == 'ItemUse'\
		and event[1] in ('e', 'q')\
		and inputManager.GetKeyDown(event[1])
def notMove(event : Tuple[str, int | str]):
	return event[0] == 'NotMove'
def endAnimation(event : Tuple[str, int | str]):
	return event[0] == 'EndAnimation'
def damaged(event : Tuple[str, int]):
	return event[0] == 'Damaged'
def attackKeyDown(event : Tuple[str, int]):
	return event[0] == 'Attack'\
		and inputManager.GetKeyDown(inputManager.kMouseLeft)
def boxKeyDown(event : Tuple[str, int]):
	return event[0] == 'Box'\
		and inputManager.GetKeyDown(inputManager.kMouseRight)

class Idle(State):
	onKey : bool = False
	@staticmethod
	def enter(own, event):
		sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
		sp.SetAction('idle')
		if event[0] == 'NotMove':
			Idle.onKey = event[1]
		pass
	
	@staticmethod
	def exit(own, event):
		sc : LumberjackScript = own.GetComponent(Enums.ComponentType.Script)
		sc.evolutionTimer.x = 0.0
		pass
		
	@staticmethod
	def do(own):
		sc : LumberjackScript = own.GetComponent(Enums.ComponentType.Script)
		sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
		
		if Idle.onKey:
			inputPressed = inputManager.GetKey
			if inputPressed('w') and not inputPressed('s'): sc.statemachine.add_event(('InputPressed', 'w'))
			if inputPressed('a') and not inputPressed('d'): sc.statemachine.add_event(('InputPressed', 'a'))
			if inputPressed('d') and not inputPressed('a'): sc.statemachine.add_event(('InputPressed', 'd'))
			if inputPressed('s') and not inputPressed('w'): sc.statemachine.add_event(('InputPressed', 's'))
			
		if sp.name == 'Juggernaut': return
		if (sc.generateReached
				and sc.energyCount >= 5
				and sp.name == 'Lumberjack'
				and inputManager.GetKey('e')
		):
			sc.evolutionTimer.x += timer.GetDeltaTime()
			if sc.evolutionTimer.x >= sc.evolutionTimer.y:
				sc.evolutionTimer.x = 0.0
				sc.hungry = 100.0
				sc.health = 100.0
				sc.SwapSprite()
		elif inputManager.GetKeyDown('e') and sc.tomatoCount > 0:
			sc.statemachine.add_event(('ItemUse', 'e'))
		elif inputManager.GetKeyDown('q') and sc.medikitCount > 0:
			sc.statemachine.add_event(('ItemUse', 'q'))
		pass

class Move(State):
	isNotBossHighlight : int = 1
	@staticmethod
	def enter(own, event):
		sc : LumberjackScript = own.GetComponent(Enums.ComponentType.Script)
		sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
		sp.SetAction('move')
		sp.SetActionSpeed('move', int(sc.hungry / 10))
		flip : str = 'None'
		if event[1] == 'a': flip = 'h'
		elif event[1] == 'd': flip = ''
		if flip != 'None':
			sp.SetAllFlip(flip)
		pass
	
	@staticmethod
	def exit(own, event):
		pass
	
	@staticmethod
	def do(own):
		tr : Transform = own.GetComponent(Enums.ComponentType.Transform)
		sc : LumberjackScript = own.GetComponent(Enums.ComponentType.Script)
		sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
		delta = Vector2()
		isMove = False
		if inputManager.GetKey('w'):
			delta += Vector2(0, sc.hungry); isMove = True
		if inputManager.GetKey('a'):
			delta += Vector2(-sc.hungry, 0); isMove = True
		if inputManager.GetKey('s'):
			delta += Vector2(0, -sc.hungry); isMove = True
		if inputManager.GetKey('d'):
			delta += Vector2(sc.hungry, 0); isMove = True
		
		flip : str = 'None'
		if delta == Vector2(0, 0):
			sc.statemachine.add_event(('NotMove', isMove))
		elif delta.x > 0: flip = ''
		elif delta.x < 0: flip = 'h'
		if flip != 'None':
			sp.SetAllFlip(flip)
		nextPos = tr.GetPosition() + delta * timer.GetDeltaTime() * Move.isNotBossHighlight
		from framework import Application
		CameraPos = Application.mainCamera.CalculatePosition(nextPos)
		from framework.Application import app
		xValid : bool = (0 < CameraPos.x < app.screen.x)
		yValid : bool = (0 < CameraPos.y < app.screen.y)
		if not xValid:
			delta.x = 0.0
		if not yValid:
			delta.y = 0.0
		nextPos = tr.GetPosition() + delta * timer.GetDeltaTime() * Move.isNotBossHighlight
		
		tr.SetPosition(nextPos)
		
		if sp.name == 'Juggernaut': return
		if inputManager.GetKeyDown('e') and sc.tomatoCount > 0:
			sc.statemachine.add_event(('ItemUse', 'e'))
		elif inputManager.GetKeyDown('q') and sc.medikitCount > 0:
			sc.statemachine.add_event(('ItemUse', 'q'))
		pass

class AttackTrigger(GameObject) :
	def __init__(self):
		super().__init__()
		self.damage : float = 0.0

class Attack(State):
	AttackTrigger : AttackTrigger = None
	enterPos : Vector2 = None
	@staticmethod
	def enter(own: GameObject, event: Tuple[str, int | str]):
		sc : LumberjackScript = own.GetComponent(Enums.ComponentType.Script)
		sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
		critical = randint(1, 10000)
		if critical < sc.hungry * 100 / 2:
			sp.SetAction('attack')
			sp.SetActionSpeed('attack', int(sc.hungry / 4))
		else:
			sp.SetAction('attackCritical')
			sp.SetActionSpeed('attackCritical', int(sc.hungry / 4))
			if sp.name == 'Juggernaut':
				sp.SetOffset(Vector2(0, 20))
				tr : Transform = own.GetComponent(Enums.ComponentType.Transform)
				Attack.enterPos = tr.GetPosition()
		if sp.name == 'Lumberjack':
			sc.hungry = max(sc.hungry - 1.5, 0.0)
		else:
			sc.energyCount = max(sc.energyCount - 1.5 * 0.05, 0)
		pass
	
	@staticmethod
	def exit(own: GameObject, event: Tuple[str, int | str]):
		if Attack.AttackTrigger is not None:
			Object.Destroy(Attack.AttackTrigger)
			Attack.AttackTrigger = None
		sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
		if (sp.name == 'Juggernaut') and (sp.curAction == 'attackCritical'):
			cd : BoxCollider2D = own.GetComponent(Enums.ComponentType.Collider)
			tr : Transform = own.GetComponent(Enums.ComponentType.Transform)
			tr.SetPosition(Attack.enterPos + Vector2(cd.GetSize().x * (-110 if sp.action[sp.curAction].flip == '' else 110), 6))
			sp.SetOffset(Vector2(0, 0))
		
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
		elif sp.action[sp.curAction].curFrame \
			<= ((sp.action[sp.curAction].frameCount // 2) if sp.name == 'Lumberjack' else 8):
			inputDown = inputManager.GetKeyDown
			flip: str = 'None'
			if inputDown('a'): flip = 'h'
			elif inputDown('d'): flip = ''
			if flip != 'None':
				sp.SetAllFlip(flip)
				
			if (sp.name == 'Juggernaut') and (sp.curAction == 'attackCritical'):
				tr: Transform = own.GetComponent(Enums.ComponentType.Transform)
				cd: BoxCollider2D = own.GetComponent(Enums.ComponentType.Collider)
				tr.SetPosition(Attack.enterPos
				               + (Vector2(cd.GetSize().x * (-110 if sp.action[sp.curAction].flip == '' else 110), 6)
				               * sp.action[sp.curAction].curFrame / 8.0))
				
		elif Attack.AttackTrigger is None:
			tr: Transform = own.GetComponent(Enums.ComponentType.Transform)
			size: Vector2 = Vector2(0.3, 0.62)
			offset: Vector2 = Vector2(30, 0)
			if sp.curAction == 'attackCritical': offset.x += size.x * 50; size *= 1.5
			
			if sp.name == 'Juggernaut': size *= 2; offset *= 1.5
			
			offsetFactor: float = 1 if sp.action[sp.curAction].flip == '' else -1
			triggerPosition: Vector2 = tr.GetPosition() + offset * offsetFactor
			Attack.AttackTrigger = Object.Instantiate(AttackTrigger, Enums.LayerType.AttackTrigger, triggerPosition)
			Attack.AttackTrigger.damage = 12.0 if sp.curAction == 'attackCritical' else 8.0
			cd: BoxCollider2D = Attack.AttackTrigger.AddComponent(BoxCollider2D)
			cd.SetSize(size)
			cd.SetOffset(own.GetComponent(Enums.ComponentType.Collider).GetOffset())
		pass

class Damaged(State):
	deathTimer : Vector2 = Vector2(0, 2.0)
	damagedTimer : Vector2 = Vector2(0.6, 0.5)
	@staticmethod
	def enter(own: GameObject, event: Tuple[str, int | str]):
		sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
		if event[1] <= 0.0:
			if sp.name == 'Lumberjack':
				sp.SetAction('death')
				return
			else:
				sc : LumberjackScript = own.GetComponent(Enums.ComponentType.Script)
				sc.health = 0.0
				sc.energyCount -= 0.5
				if sc.energyCount <= 0:
					sp.SetAction('death')
					return
		else:
			sp.SetAction('idle')
		CollisionManager.CollisionLayerCheck(Enums.LayerType.Player, Enums.LayerType.EnemyAttackTrigger, False)
		Damaged.damagedTimer.x = 0.0
		sp.image.opacify(0.7)
		pass
	
	@staticmethod
	def exit(own: GameObject, event: Tuple[str, int | str]):
		pass
	
	@staticmethod
	def do(own: GameObject):
		sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
		sc : LumberjackScript = own.GetComponent(Enums.ComponentType.Script)
		if sp.action[sp.curAction].isComplete:
			if sp.curAction == 'death':
				Damaged.deathTimer.x += timer.GetDeltaTime()
				if Damaged.deathTimer.x >= Damaged.deathTimer.y:
					from framework.Application import app
					app.Close()
			else:
				sc.statemachine.add_event(('NotMove', True))
		elif sp.name == 'Juggernaut' and sp.curAction != 'death':
			sc.statemachine.add_event(('NotMove', True))
		pass
	pass

class ItemUse(State):
	useKey : str = ''
	@staticmethod
	def enter(own: GameObject, event: Tuple[str, int | str]):
		sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
		sp.SetAction('itemUse')
		ItemUse.useKey = event[1]
		pass
	
	@staticmethod
	def exit(own: GameObject, event: Tuple[str, int | str]):
		pass
	
	@staticmethod
	def do(own: GameObject):
		sp : Sprite = own.GetComponent(Enums.ComponentType.Sprite)
		if sp.action[sp.curAction].isComplete:
			sc : LumberjackScript = own.GetComponent(Enums.ComponentType.Script)
			if ItemUse.useKey == 'e':
				sc.tomatoCount -= 1
				sc.hungry = min(sc.hungry + 20.0, 100.0)
			elif ItemUse.useKey == 'q':
				sc.medikitCount -= 1
				sc.health = min(sc.health + 25.0, 100.0)
			sc = own.GetComponent(Enums.ComponentType.Script)
			sc.statemachine.add_event(('NotMove', True))
		pass

class LumberjackScript(Script):
	bossAttackCollision : bool = False
	def __init__(self):
		super().__init__()
		self.swapSprite : Sprite = None
		
		self.health : float = 100.0
		self.hungry : float = 100.0
		# self.isVenom : bool = False
		
		self.medikitCount : int = 0
		self.tomatoCount : int = 0
		
		self.timberCount : int = 0
		
		self.energyCount : int = 50
		self.generateReached : bool = False
		self.evolutionTimer : Vector2 = Vector2(0.0, 5.0)
		
		self.statemachine : StateMachine = None
	
	def Update(self):
		inputDown = inputManager.GetKeyDown
		if inputDown('w') : self.statemachine.add_event(('InputDown', 'w'))
		elif inputDown('a') : self.statemachine.add_event(('InputDown', 'a'))
		elif inputDown('d') : self.statemachine.add_event(('InputDown', 'd'))
		elif inputDown('s') : self.statemachine.add_event(('InputDown', 's'))
		
		if inputManager.GetKeyUp('e'): self.evolutionTimer.x = 0.0
		
		if inputDown(inputManager.kMouseLeft):
			self.statemachine.add_event(('Attack', inputManager.kMouseLeft))
		if inputDown(inputManager.kMouseRight):
			self.statemachine.add_event(('Box', inputManager.kMouseRight))
		
		sp: Sprite = self.GetOwner().GetComponent(Enums.ComponentType.Sprite)
		if Damaged.damagedTimer.x < Damaged.damagedTimer.y:
			Damaged.damagedTimer.x += timer.GetDeltaTime()
			if Damaged.damagedTimer.x >= Damaged.damagedTimer.y:
				CollisionManager.CollisionLayerCheck(Enums.LayerType.Player, Enums.LayerType.EnemyAttackTrigger, True)
				sp.image.opacify(1.0)
		
		if sp.name == 'Lumberjack':
			self.hungry = max(self.hungry
							  - (0.8 if self.statemachine.cur_state is Move else 0.4) * timer.GetDeltaTime(), 0.0)
		else:
			self.energyCount = max(self.energyCount
							  - (0.8 if self.statemachine.cur_state is Move else 0.4) * 0.05 * timer.GetDeltaTime(), 0.0)
			if self.energyCount <= 0.0 and self.health > 0.0:
				self.energyCount = 0.0
				self.health = 100.0
				self.SwapSprite()
		self.statemachine.Update()
		pass

	def LateUpdate(self):
		pass
	
	def Render(self):
		pass
	
	def OnCollisionEnter(self, other: 'Collider'):
		otherObj = other.GetOwner()
		if otherObj.GetLayer() == Enums.LayerType.EnemyAttackTrigger and self.statemachine.cur_state is not Damaged:
			self.health -= otherObj.damage
			self.statemachine.add_event(('Damaged', self.health))
		if otherObj.GetLayer() == Enums.LayerType.BossSpecialAttackTrigger\
				and self.statemachine.cur_state is not Damaged:
			print(f'{LumberjackScript.bossAttackCollision=}')
			if LumberjackScript.bossAttackCollision:
				if self.statemachine.cur_state is not Damaged: self.health -= otherObj.damage
				self.statemachine.add_event(('Damaged', self.health))
			else: LumberjackScript.bossAttackCollision = True
		pass
	
	def OnCollisionStay(self, other: 'Collider'):
		pass
	
	def OnCollisionExit(self, other: 'Collider'):
		pass
	
	def Init(self):
		cd: BoxCollider2D = self.GetOwner().AddComponent(BoxCollider2D)
		cd.SetOffset(Vector2(0, -10))
		cd.SetSize(Vector2(0.32, 0.62))
		
		sp: Sprite = self.GetOwner().AddComponent(Sprite)
		sp.SetImage("Juggernaut.png")
		sp.AddAction('idle', 0, 7, 6
					 , Vector2(65, 3174), Vector2(72, 72), '')
		sp.AddAction('move', 0, 12, 6
					 , Vector2(65, 2992), Vector2(72, 72), '')
		sp.AddAction('attack', 0, 16, 4
					 , Vector2(65, 2846), Vector2(100, 72), '', repeat=False)
		sp.AddAction('attackCritical', 0, 21, 2
					 , Vector2(65, 2526), Vector2(204, 100), '', repeat=False)
		sp.AddAction('death', 0, 29, 2
					 , Vector2(65, 1415), Vector2(210, 100), '', repeat=False)
		sp.SetAction('idle')
		self.swapSprite = sp
		
		sp: Sprite = self.GetOwner().AddComponent(Sprite)
		sp.SetImage("Lumberjack.png")
		sp.AddAction('idle', 0, 6, 6
					 , Vector2(67, 1423), Vector2(72, 72), '')
		sp.AddAction('move', 0, 8, 6
					 , Vector2(67, 1314), Vector2(72, 72), '')
		sp.AddAction('attack', 0, 10, 4
					 , Vector2(67, 1168), Vector2(96, 72), '', repeat=False)
		sp.AddAction('attackCritical', 0, 15, 4
					 , Vector2(67, 949), Vector2(96, 72), '', repeat=False)
		sp.AddAction('itemUse', 0, 13, 6
					 , Vector2(67, 657), Vector2(72, 72), '', repeat=False)
		sp.AddAction('death', 0, 16, 3
					 , Vector2(67, 438), Vector2(134, 72), '', repeat=False)
		self.statemachine = StateMachine(self.GetOwner(), Idle)
		self.statemachine.set_transitions(
			{
				Idle: {
					moveKeyDown: Move, moveKeyPressed: Move, attackKeyDown: Attack, damaged : Damaged
					, itemUse: ItemUse,
				},
				Move: {
					notMove: Idle, attackKeyDown: Attack, damaged : Damaged, itemUse: ItemUse
				},
				Attack: {
					endAnimation: Idle, moveKeyPressed: Move, damaged : Damaged
				},
				Damaged: {
					notMove: Idle
				},
				ItemUse: {
					notMove: Idle, damaged : Damaged
				},
			}
		)

	def SwapSprite(self):
		origin = self.GetOwner().GetComponent(Enums.ComponentType.Sprite)
		self.GetOwner().SetComponent(self.swapSprite); self.swapSprite = origin
		pass
	
	@staticmethod
	def SetBossAttackFalse():
		LumberjackScript.bossAttackCollision = False
		pass