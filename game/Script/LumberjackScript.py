from pygame import Vector2

from framework.Common import Enums
from framework.Common.InputManager import inputManager
from framework.Common.Timer import timer
from framework.Component.Script import Script
from framework.Component.Transform import Transform


class LumberjackScript(Script):
	def __init__(self):
		super().__init__()
		self.speed : float = 100.0
		pass
	
	def Update(self):
		tr : Transform = self.GetOwner().GetComponent(Enums.ComponentType.Transform)
		if inputManager.GetKey('a'):
			tr.SetPosition(tr.GetPosition() - Vector2(self.speed, 0) * timer.GetDeltaTime())
		if inputManager.GetKey('d'):
			tr.SetPosition(tr.GetPosition() + Vector2(self.speed, 0) * timer.GetDeltaTime())
		if inputManager.GetKey('s'):
			tr.SetPosition(tr.GetPosition() - Vector2(0, self.speed) * timer.GetDeltaTime())
		if inputManager.GetKey('w'):
			tr.SetPosition(tr.GetPosition() + Vector2(0, self.speed) * timer.GetDeltaTime())
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
