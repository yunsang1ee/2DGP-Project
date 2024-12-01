from pico2d import draw_rectangle
from sdl2.sdlgfx import filledCircleColor

from framework.Common import Enums
from framework.Component.Collider.Collider import Collider
from framework.Component.Transform import Transform


class BoxCollider2D(Collider):
	def __init__(self):
		super().__init__(Enums.ColliderType.Box2D)
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
		draw_rectangle  (position.x - size.x
		               , position.y - size.y
		               , position.x + size.x
		               , position.y + size.y)