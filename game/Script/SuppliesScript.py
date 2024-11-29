from abc import ABC, abstractmethod

from pygame import Vector2

from framework.Common import Enums, Object
from framework.Component.Script import Script
from framework.Component.Sprite import Sprite
from framework.GameObject.GameObject import GameObject


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
		             , Vector2(65, 329), Vector2(64, 198), '')
		sp.AddAction('idle', 0, 1, 1
		             , Vector2(65, 528), Vector2(64, 66), '')
		sp.AddAction('touched', 0, 6, 3
		             , Vector2(65, 65), Vector2(128, 64), '', repeat=False)
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


class TomatoScript(SuppliesScript):
	"""
	Hungry Warning Point 50 (50 -> player Speed <= Monster Speed)
	10 tmt/m
	10 Hp/tmt
	-0.8 Hp/s -> -48 Hp/m
	-2.0 Hp/LeftClick
	(5s Timer)  average 10 tomatoGen/m -> 5~20 Gen
	-> Gen/10s -> 6 Gen/m -> average 2 tomato/Gen -> 1 ~ 4 Gen
	"""
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


class EnergyEggScript(SuppliesScript):
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


class EnergyScript(SuppliesScript):
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
	
	