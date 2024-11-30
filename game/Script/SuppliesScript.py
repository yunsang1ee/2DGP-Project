from abc import ABC, abstractmethod
from random import randint
from timeit import repeat

from pygame import Vector2

from framework.Common import Enums, Object
from framework.Common.Enums import LayerType
from framework.Common.Timer import timer
from framework.Component.Collider.BoxCollider2D import BoxCollider2D
from framework.Component.Script import Script
from framework.Component.Sprite import Sprite
from framework.Component.Transform import Transform
from framework.GameObject.GameObject import GameObject
from game.Script.LumberjackScript import LumberjackScript


class SuppliesScript(Script, ABC):
	def __init__(self):
		super().__init__()
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
			Object.Destroy(self.GetOwner())
		pass
	
	def OnCollisionStay(self, other: 'Collider'):
		pass
	
	def OnCollisionExit(self, other: 'Collider'):
		pass

class TreeScript(SuppliesScript):
	def __init__(self):
		super().__init__()
		self.count = 3
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


class EnergyEggScript(SuppliesScript):
	def __init__(self):
		super().__init__()
		self.spawnSphereTimer : Vector2 = Vector2(0.0, 3.0)
		pass
	
	def Init(self):
		sp : Sprite = self.GetOwner().AddComponent(Sprite)
		sp.SetImage("Egg.png")
		sp.AddAction('idle', 0, 6, 6
		             , Vector2(65, 293), Vector2(72, 72), '', repeat=False)
		sp.AddAction('idle2', 0, 5, 6
		             , Vector2(65, 220), Vector2(72, 72), '', repeat=False)
		sp.AddAction('spawnSphere', 0, 8, 6
		             , Vector2(65, 147), Vector2(72, 72), '', repeat=False)
		pass

	def Update(self):
		sp : Sprite = self.GetOwner().GetComponent(Enums.ComponentType.Script)
		if sp.curAction == 'spawnSphere':
			if sp.action[sp.curAction].isComplete:
				sphere = Object.Instantiate(GameObject, Enums.LayerType.Supplies)
				sc = sphere.AddComponent(EnergyScript); sc.Init()
				cd : BoxCollider2D = self.GetOwner().AddComponent(BoxCollider2D)
				cd.SetOffset(Vector2(0, 16))
				cd.SetSize(Vector2(0.43, 0.41))
				Object.Destroy(self.GetOwner())
		else:
			self.spawnSphereTimer.x += timer.GetDeltaTime()
			if self.spawnSphereTimer.x >= self.spawnSphereTimer.y:
				sp.SetAction('spawnSphere')
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
		sp.AddAction('idle', 0, 4,6
		             , Vector2(65, 147), Vector2(72, 72), '')
		sp.AddAction('touched', 0, 10,6
		             , Vector2(65, 74), Vector2(72, 72), '')
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
			from game.Script.LumberjackScript import LumberjackScript
			sc : LumberjackScript = otherObj.GetComponent(Enums.ComponentType.Script)
			sc.energyCount += 1
			Object.Destroy(self.GetOwner())
		pass
	
	def OnCollisionStay(self, other: 'Collider'):
		pass
	
	def OnCollisionExit(self, other: 'Collider'):
		pass
	
	
class Generator(SuppliesScript):
	def __init__(self):
		super().__init__()
		pass
	
	def Init(self):
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