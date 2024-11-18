from framework.Common import Enums
from framework.Component.Collider.Collider import Collider


class CircleCollider(Collider):
	def __init__(self):
		super().__init__(Enums.ColliderType.Circle)
		pass
	
	def Update(self):
		pass
	
	def LateUpdate(self):
		pass
	
	def Render(self):
		pass