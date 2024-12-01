from pygame import Vector2

from framework.Common import Enums
from framework.Component.Component import Component
from framework.Component.Transform import Transform
from framework.GameObject.GameObject import GameObject


class Camera(Component):
	def __init__(self):
		super().__init__(Enums.ComponentType.Camera)
		self.distance : Vector2 = Vector2(0, 0)
		from framework.Application import app
		self.resolution : Vector2 = app.screen
		self.lookPosition : Vector2 = Vector2(0, 0)
		self.target : GameObject | None = None
		self.minPosition : Vector2 = Vector2(0, 0)
		self.maxPosition : Vector2 = self.resolution
		self.xMin = False; self.xMax = False
		self.yMin = False; self.yMax = False
		pass
	
	def Update(self):
		if self.target:
			tr : Transform = self.target.GetComponent(Enums.ComponentType.Transform)
			self.lookPosition = tr.GetPosition()
		else:
			tr : Transform = self.GetOwner().GetComponent(Enums.ComponentType.Transform)
			self.lookPosition = tr.GetPosition()
		
		prevLookPosition = self.lookPosition
		self.lookPosition = Vector2(
			max(self.minPosition.x, min(self.maxPosition.x, self.lookPosition.x)),
			max(self.minPosition.y, min(self.maxPosition.y, self.lookPosition.y))
		)
		
		self.xMin = self.lookPosition.x == self.minPosition.x
		self.xMax = self.lookPosition.x == self.maxPosition.x
		if self.lookPosition.x == prevLookPosition.x:
			self.xMin = False
			self.xMax = False
		
		self.yMin = self.lookPosition.y == self.minPosition.y
		self.yMax = self.lookPosition.y == self.maxPosition.y
		if self.lookPosition.y == prevLookPosition.y:
			self.yMin = False
			self.yMax = False

		self.distance = self.lookPosition - (self.resolution / 2.0)
		pass

	def LateUpdate(self):
		pass
	
	def Render(self):
		pass
	
	def SetMinMax(self, minPosition : Vector2, maxPosition : Vector2):
		self.minPosition = minPosition
		self.maxPosition = maxPosition
	
	def SetTarget(self, target : GameObject):
		self.target = target
		
	def CalculatePosition(self, position : Vector2) -> Vector2:
		return position - self.distance