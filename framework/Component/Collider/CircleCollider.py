from pico2d import *
from pygame import Vector2

from framework.Common import Enums
from framework.Component.Collider.Collider import Collider
from framework.Component.Transform import Transform

def draw_circle(center : Vector2, radius):
	for angle in range(0, 360, 1):
		rad = math.radians(angle)
		dx = int(radius * math.cos(rad))
		dy = int(radius * math.sin(rad))
		draw_rectangle(center.x + dx, center.y + dy, center.x + dx, center.y + dy)
		
class CircleCollider(Collider):
	def __init__(self):
		super().__init__(Enums.ColliderType.Circle)
		pass
	
	def Update(self):
		pass
	
	def LateUpdate(self):
		pass
	
	def Render(self):
		if not self.isRender() : return
		
		tr : Transform = self.GetOwner().GetComponent(Enums.ComponentType.Transform)
		position = tr.GetPosition() + self.GetOffset()
		from framework.Application import mainCamera
		if mainCamera: position = mainCamera.CalculatePosition(position)
		size = self.GetSize() * 100 // 2
		draw_circle(position, min(size.x, size.y))
		pass