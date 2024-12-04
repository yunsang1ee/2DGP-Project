from abc import ABC, abstractmethod
from random import randint

from pico2d import load_wav, Music
from pygame import Vector2

from framework.Common import Enums, Object
from framework.Common.InputManager import inputManager
from framework.Common.Timer import timer
from framework.Component.Collider.BoxCollider2D import BoxCollider2D
from framework.Component.Collider.CircleCollider import CircleCollider
from framework.Component.Script import Script
from framework.Component.Sprite import Sprite
from framework.Component.Transform import Transform
from framework.GameObject.GameObject import GameObject

from game.Script.LumberjackScript import LumberjackScript


class SuppliesScript(Script, ABC):
	itemGetSound : Music = None
	def __init__(self):
		super().__init__()
		if not SuppliesScript.itemGetSound: SuppliesScript.itemGetSound = load_wav('./resource/itemGet.wav'); SuppliesScript.itemGetSound.set_volume(32)
		pass
	
	@abstractmethod
	def Init(self):
		pass
	pass

class MedikitScript(SuppliesScript):
	def __init__(self):
		super().__init__()
		pass
	
	def Init(self):
		sp: Sprite = self.GetOwner().AddComponent(Sprite)
		sp.SetImage("Medikit.png")
		sp.AddAction('drop', 0, 10, 6
					 , Vector2(65, 329), Vector2(64, 198), '', repeat=False)
		sp.AddAction('idle', 0, 1, 1
					 , Vector2(65, 528), Vector2(64, 66), '', repeat=False)
		sp.AddAction('touched', 0, 6, 3
					 , Vector2(65, 65), Vector2(128, 64), '', 20, False)
		sp.SetAction('drop')
		sp.SetOffset(Vector2(0, 81))
		cd : BoxCollider2D = self.GetOwner().AddComponent(BoxCollider2D)
		cd.SetSize(Vector2(0.0, 0.0))
		cd.SetOffset(Vector2(-10000.0, -10000.0))
		pass

	def Update(self):
		sp : Sprite = self.GetOwner().GetComponent(Enums.ComponentType.Sprite)
		if sp.action[sp.curAction].isComplete:
			if sp.curAction == 'drop':
				sp.SetAction('idle')
				sp.SetOffset(Vector2(0, 0))
				cd : BoxCollider2D = self.GetOwner().GetComponent(Enums.ComponentType.Collider)
				cd.SetSize(Vector2(0.30, 0.28))
				cd.SetOffset(Vector2(0.0, 0.0))
			elif sp.curAction == 'touched':
				Object.Destroy(self.GetOwner())
		pass
	
	def LateUpdate(self):
		pass
	
	def Render(self):
		pass
	
	def OnCollisionEnter(self, other: 'Collider'):
		otherObj : GameObject = other.GetOwner()
		sp : Sprite = self.GetOwner().GetComponent(Enums.ComponentType.Sprite)
		if otherObj.GetLayer() == Enums.LayerType.Player and sp.curAction == 'idle':
			sc : LumberjackScript = otherObj.GetComponent(Enums.ComponentType.Script)
			sc.medikitCount += 1
			SuppliesScript.itemGetSound.play()
			sp.SetAction('touched')
		pass
	
	def OnCollisionStay(self, other: 'Collider'):
		pass
	
	def OnCollisionExit(self, other: 'Collider'):
		pass

class TomatoScript(SuppliesScript):
	"""
	Hungry Warning Point 50 (50 -> player Speed <= Monster Speed)
	10 tmt/m
	10 Hp/tmt
	-0.8 Hp/s -> -48 Hp/m
	-2.0 Hp/LeftClick
	(10s Timer)  average 10 tomato/m -> 5~15 Gen
	-> Gen/10s -> 5 Gen/m -> average 2 tomato/Gen -> 1 ~ 3 Gen
	"""
	def __init__(self):
		super().__init__()
		pass
	
	def Init(self):
		sp: Sprite = self.GetOwner().AddComponent(Sprite)
		sp.SetImage("Tomato.png")
		sp.AddAction('drop', 0, 13, 6
					 , Vector2(65, 528), Vector2(64, 198), '', repeat=False)
		sp.AddAction('idle', 0, 1, 1
					 , Vector2(65, 727), Vector2(72, 64), '', repeat=False)
		sp.AddAction('touched', 0, 6, 3
					 , Vector2(65, 65), Vector2(128, 64), '', 20, False)
		sp.SetAction('drop')
		sp.SetOffset(Vector2(0, 77))
		cd : BoxCollider2D = self.GetOwner().AddComponent(BoxCollider2D)
		cd.SetSize(Vector2(0.0, 0.0))
		cd.SetOffset(Vector2(-10000.0, -10000.0))
		pass

	def Update(self):
		sp : Sprite = self.GetOwner().GetComponent(Enums.ComponentType.Sprite)
		if sp.action[sp.curAction].isComplete:
			if sp.curAction == 'drop':
				sp.SetAction('idle')
				sp.SetOffset(Vector2(0, 0))
				cd : BoxCollider2D = self.GetOwner().GetComponent(Enums.ComponentType.Collider)
				cd.SetSize(Vector2(0.24, 0.36))
				cd.SetOffset(Vector2(0.0, 0.0))
			elif sp.curAction == 'touched':
				Object.Destroy(self.GetOwner())
		pass
	
	def LateUpdate(self):
		pass
	
	def Render(self):
		pass
	
	def OnCollisionEnter(self, other: 'Collider'):
		otherObj : GameObject = other.GetOwner()
		sp : Sprite = self.GetOwner().GetComponent(Enums.ComponentType.Sprite)
		if otherObj.GetLayer() == Enums.LayerType.Player and sp.curAction == 'idle':
			sc : LumberjackScript = otherObj.GetComponent(Enums.ComponentType.Script)
			sc.tomatoCount += 1
			SuppliesScript.itemGetSound.play()
			sp.SetAction('touched')
		pass
	
	def OnCollisionStay(self, other: 'Collider'):
		pass
	
	def OnCollisionExit(self, other: 'Collider'):
		pass

class TimberScript(SuppliesScript):
	def __init__(self):
		super().__init__()
		pass
	
	def Init(self):
		sp: Sprite = self.GetOwner().AddComponent(Sprite)
		sp.SetImage("Timber.png")
		sp.AddAction('1', 0, 1, 1
					 , Vector2(0, 0), Vector2(48, 41), '', repeat=False)
		cd : BoxCollider2D = self.GetOwner().AddComponent(BoxCollider2D)
		cd.SetSize(Vector2(0.48, 0.41))
		pass
	
	def Update(self):
		pass
	
	def LateUpdate(self):
		pass
	
	def Render(self):
		pass
	
	def OnCollisionEnter(self, other: 'Collider'):
		otherObj : GameObject = other.GetOwner()
		if otherObj.GetLayer() == Enums.LayerType.Player:
			sc : LumberjackScript = otherObj.GetComponent(Enums.ComponentType.Script)
			sc.timberCount += 1
			SuppliesScript.itemGetSound.play()
			Object.Destroy(self.GetOwner())
		pass
	
	def OnCollisionStay(self, other: 'Collider'):
		pass
	
	def OnCollisionExit(self, other: 'Collider'):
		pass

class TreeScript(SuppliesScript):
	damagedSound : Music = None
	def __init__(self):
		super().__init__()
		self.count = 3
		if not TreeScript.damagedSound: TreeScript.damagedSound = load_wav('./resource/TreeCollision.wav')
		pass
	
	def Init(self):
		sp: Sprite = self.GetOwner().AddComponent(Sprite)
		sp.SetImage("Tree.png")
		sp.AddAction('1', 0, 1, 1
					 , Vector2(0, 0), Vector2(265, 408), '', repeat=False)
		sp.AddAction('2', 0, 1, 1
					 , Vector2(266, 0), Vector2(265, 408), '', repeat=False)
		sp.SetAction(str(randint(1, 2)))
		sp.SetOffset(Vector2(0, 120 * 0.6))
		
		cd : BoxCollider2D = self.GetOwner().AddComponent(BoxCollider2D)
		cd.SetSize(Vector2(0.6, 1.1) * 0.6)
		
		tr : Transform = self.GetOwner().GetComponent(Enums.ComponentType.Transform)
		tr.SetScale(Vector2(0.6, 0.6))
		pass
	
	def Update(self):
		pass
	
	def LateUpdate(self):
		pass
	
	def Render(self):
		pass
	
	def OnCollisionEnter(self, other: 'Collider'):
		otherObj : GameObject = other.GetOwner()
		if otherObj.GetLayer() == Enums.LayerType.AttackTrigger:
			self.count -= 1
			self.damagedSound.play()
			if self.count <= 0:
				for _ in range(randint(2, 3)):
					tr : Transform = self.GetOwner().GetComponent(Enums.ComponentType.Transform)
					timber = Object.Instantiate(GameObject, Enums.LayerType.Supplies
												, tr.GetPosition() + Vector2(randint(-10, 10), randint(-10, 10)))
					sc = timber.AddComponent(TimberScript); sc.Init()
				Object.Destroy(self.GetOwner())
		pass
	
	def OnCollisionStay(self, other: 'Collider'):
		pass
	
	def OnCollisionExit(self, other: 'Collider'):
		pass
	
class BoxScript(SuppliesScript):
	damagedSound : Music = None
	def __init__(self):
		super().__init__()
		self.health : float = 55.0
		self.damagedTimer : Vector2 = Vector2(1.1, 1.0)
		if not BoxScript.damagedSound: BoxScript.damagedSound = load_wav('./resource/TreeCollision.wav'); BoxScript.damagedSound.set_volume(32)
		pass
	
	def Init(self):
		sp: Sprite = self.GetOwner().AddComponent(Sprite)
		sp.SetImage("Box.png")
		sp.AddAction('1', 0, 9, 3
					 , Vector2(83, 216), Vector2(109, 107), '', 0, False)
		cd : BoxCollider2D = self.GetOwner().AddComponent(BoxCollider2D)
		cd.SetOffset(Vector2(0, -25) * 0.5)
		cd.SetSize(Vector2(1.0, 0.5) * 0.5)
		
		tr : Transform = self.GetOwner().GetComponent(Enums.ComponentType.Transform)
		tr.SetScale(Vector2(0.5, 0.5))
		pass
	
	def Update(self):
		if self.damagedTimer.x < self.damagedTimer.y:
			self.damagedTimer.x += timer.GetDeltaTime()
		else:
			sp : Sprite = self.GetOwner().GetComponent(Enums.ComponentType.Sprite)
			sp.image.opacify(1.0)
		pass
	
	def LateUpdate(self):
		pass
	
	def Render(self):
		pass
	
	def OnCollisionEnter(self, other: 'Collider'):
		otherObj = other.GetOwner()
		if otherObj.GetLayer() in (Enums.LayerType.EnemyAttackTrigger, Enums.LayerType.BossSpecialAttackTrigger)\
			and self.damagedTimer.x >= self.damagedTimer.y:
			sp : Sprite = self.GetOwner().GetComponent(Enums.ComponentType.Sprite)
			sp.image.opacify(0.7)
			self.damagedTimer.x = 0.0
			self.health -= otherObj.damage
			BoxScript.damagedSound.play()
			if self.health <= 0:
				Object.Destroy(self.GetOwner())
			else:
				sp.action[sp.curAction].curFrame = (100 - ((self.health / 50) * 100)) * 9 // 100
		pass
	
	def OnCollisionStay(self, other: 'Collider'):
		pass
	
	def OnCollisionExit(self, other: 'Collider'):
		pass


class EnergyEggScript(SuppliesScript):
	def __init__(self):
		super().__init__()
		self.spawnSphereTimer : Vector2 = Vector2(0.0, 3.0)
		pass
	
	def Init(self):
		sp : Sprite = self.GetOwner().AddComponent(Sprite)
		sp.SetImage("Egg.png")
		sp.AddAction('spawnSphere', 0, 8, 6
					 , Vector2(65, 147), Vector2(72, 72), '', repeat=False)
		sp.AddAction('idle2', 0, 5, 6
					 , Vector2(65, 220), Vector2(72, 72), '', repeat=False)
		sp.AddAction('idle', 0, 6, 6
					 , Vector2(65, 293), Vector2(72, 72), '', repeat=False)
		pass

	def Update(self):
		sp : Sprite = self.GetOwner().GetComponent(Enums.ComponentType.Sprite)
		if sp.curAction == 'spawnSphere':
			if sp.action[sp.curAction].isComplete:
				tr = self.GetOwner().GetComponent(Enums.ComponentType.Transform)
				sphere = Object.Instantiate(GameObject, Enums.LayerType.Supplies, tr.GetPosition())
				sc = sphere.AddComponent(EnergyScript); sc.Init()
				cd : CircleCollider = sphere.AddComponent(CircleCollider)
				cd.SetOffset(Vector2(0, -16))
				cd.SetSize(Vector2(0.3, 0.3))
				Object.Destroy(self.GetOwner())
		else:
			self.spawnSphereTimer.x += timer.GetDeltaTime()
			if self.spawnSphereTimer.x >= self.spawnSphereTimer.y:
				sp.SetAction('spawnSphere')
			elif sp.action[sp.curAction].isComplete:
				sp.SetAction('idle' if randint(1, 10000) <= 7000 else 'idle2')
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

class EnergyScript(SuppliesScript):
	def __init__(self):
		super().__init__()
		pass
	
	def Init(self):
		sp : Sprite = self.GetOwner().AddComponent(Sprite)
		sp.SetImage("Energy_Sphere.png")
		sp.AddAction('touched', 0, 10,6
					 , Vector2(65, 74), Vector2(72, 72), '', 20, False)
		sp.AddAction('idle', 0, 4,6
					 , Vector2(65, 147), Vector2(72, 72), '')
		pass

	def Update(self):
		sp : Sprite = self.GetOwner().GetComponent(Enums.ComponentType.Sprite)
		if sp.curAction == 'touched' and sp.action[sp.curAction].isComplete:
			Object.Destroy(self.GetOwner())
			
		pass
	
	def LateUpdate(self):
		pass
	
	def Render(self):
		pass
	
	def OnCollisionEnter(self, other: 'Collider'):
		otherObj : GameObject = other.GetOwner()
		if otherObj.GetLayer() == Enums.LayerType.Player:
			from game.Script.LumberjackScript import LumberjackScript
			sc : LumberjackScript = otherObj.GetComponent(Enums.ComponentType.Script)
			sp : Sprite = self.GetOwner().GetComponent(Enums.ComponentType.Sprite)
			if sp.name == 'Lumberjack':
				sc.energyCount += 1
			else:
				energyToHealth = min(100.0 - sc.health, 20)
				sc.health += energyToHealth
				sc.energyCount += max((20.0 - energyToHealth) / 20.0, 0.0)
			sp.SetAction('touched')
			SuppliesScript.itemGetSound.play()
		pass
	
	def OnCollisionStay(self, other: 'Collider'):
		pass
	
	def OnCollisionExit(self, other: 'Collider'):
		pass
	
class GeneratorScript(SuppliesScript):
	def __init__(self):
		super().__init__()
		pass
	
	def Init(self):
		sp: Sprite = self.GetOwner().AddComponent(Sprite)
		sp.SetImage("Generator.png")
		sp.AddAction('spawn', 0, 5, 6
					 , Vector2(65, 325), Vector2(64, 64), '', repeat=False)
		sp.AddAction('idle', 0, 3, 6
					 , Vector2(65, 390), Vector2(64, 64), '')
		sp.AddAction('action', 0, 5, 6
					 , Vector2(65, 260), Vector2(64, 64), '')
		sp.AddAction('death', 0, 9, 6
					 , Vector2(65, 65), Vector2(68, 64), '', repeat=False)
		sp.SetAction('spawn')
		
		cd : BoxCollider2D = self.GetOwner().AddComponent(BoxCollider2D)
		cd.SetSize(Vector2(0.0, 0.0))
		cd.SetOffset(Vector2(-10000.0, -10000.0))
		pass
	
	def Update(self):
		sp : Sprite = self.GetOwner().GetComponent(Enums.ComponentType.Sprite)
		if sp.action[sp.curAction].isComplete:
			if sp.curAction == 'spawn':
				cd : BoxCollider2D = self.GetOwner().GetComponent(Enums.ComponentType.Collider)
				cd.SetSize(Vector2(0.4, 0.5))
				cd.SetOffset(Vector2(0, 7))
			elif sp.curAction == 'death':
				Object.Destroy(self.GetOwner())
		pass
	
	def LateUpdate(self):
		pass
	
	def Render(self):
		pass
	
	def OnCollisionEnter(self, other: 'Collider'):
		otherObj = other.GetOwner()
		if otherObj.GetLayer() == Enums.LayerType.Player:
			sc : LumberjackScript = otherObj.GetComponent(Enums.ComponentType.Script)
			sc.generateReached = True
		pass
	
	def OnCollisionStay(self, other: 'Collider'):
		otherObj = other.GetOwner()
		if otherObj.GetLayer() == Enums.LayerType.Player:
			otherSP : Sprite = otherObj.GetComponent(Enums.ComponentType.Sprite)
			sp : Sprite = self.GetOwner().GetComponent(Enums.ComponentType.Sprite)
			if otherSP.name == 'Juggernaut' and sp.curAction == 'action':
				sp.SetAction('death')
			elif otherSP.name == 'Lumberjack' and sp.curAction != 'action' and inputManager.GetKey('e'):
				sp.SetAction('action')
		pass
	
	def OnCollisionExit(self, other: 'Collider'):
		otherObj = other.GetOwner()
		if otherObj.GetLayer() == Enums.LayerType.Player:
			sc : LumberjackScript = otherObj.GetComponent(Enums.ComponentType.Script)
			sc.generateReached = False
			otherSP : Sprite = otherObj.GetComponent(Enums.ComponentType.Sprite)
			sp : Sprite = self.GetOwner().GetComponent(Enums.ComponentType.Sprite)
			if otherSP.name == 'Lumberjack': sp.SetAction('idle')
		pass