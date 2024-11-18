from collections import defaultdict
from typing import Dict

from pygame import Vector2

from framework.Application import app
from framework.Common import Enums
from framework.Component.Collider.Collider import Collider
from framework.Component.Transform import Transform
from framework.GameObject.GameObject import GameObject
from framework.Scene.Scene import Scene


class CollisionManager:
	# collisionLayerMatrix : Dict[tuple[Enums.LayerType, Enums.LayerType], bool] #Python Style?
	collisionLayerMatrix = [[False] * Enums.LayerType.End.value for _ in range(Enums.LayerType.End.value)]
	collision_map : Dict[tuple[Collider, Collider], bool] = defaultdict(bool)
	
	@staticmethod
	def __init__():
		pass
	
	@staticmethod
	def Update():
		scene = app.activeScene
		for row in range(Enums.LayerType.End.value):
			for col in range(row, Enums.LayerType.End.value):
				if CollisionManager.collisionLayerMatrix[row][col]:
					CollisionManager.layerCollision(scene, Enums.LayerType(row), Enums.LayerType(col))
		pass
	
	@staticmethod
	def LateUpdate():
		pass
	
	@staticmethod
	def Render():
		pass
	
	@staticmethod
	def CollisionLayerCheck(left: Enums.LayerType, right: Enums.LayerType, enable: bool) -> None:
		row, col = (left.value, right.value) if left.value <= right.value else (right.value, left.value)
		CollisionManager.collisionLayerMatrix[row][col] = enable
		pass
	
	@staticmethod
	def layerCollision(scene : Scene, left: Enums.LayerType, right: Enums.LayerType) -> None:
		lefts : list[GameObject] = scene.GetGameObjects(left)
		rights : list[GameObject] = scene.GetGameObjects(right)

		for leftObj in lefts:
			if leftObj.GetState() is not GameObject.State.Alive: continue
			
			leftCD = leftObj.GetComponent(Enums.ComponentType.Collider)
			if leftCD is None: continue

			for rightObj in rights:
				if not rightObj.GetState() is not GameObject.State.Alive: continue
				
				rightCD = rightObj.GetComponent(Enums.ComponentType.Collider)
				if rightCD is None or leftObj == rightObj: continue

				CollisionManager.colliderCollision(leftCD, rightCD)

	@staticmethod
	def colliderCollision(left: Collider, right: Collider) -> None:
		id_key = (left, right)
		if id_key not in CollisionManager.collision_map:
			CollisionManager.collision_map[id_key] = False

		if CollisionManager.intersect(left, right):
			if not CollisionManager.collision_map[id_key]:
				left.OnCollisionEnter(right)
				right.OnCollisionEnter(left)
				CollisionManager.collision_map[id_key] = True
			else:
				left.OnCollisionStay(right)
				right.OnCollisionStay(left)
		elif CollisionManager.collision_map[id_key]:
			left.OnCollisionExit(right)
			right.OnCollisionExit(left)
			CollisionManager.collision_map[id_key] = False

	@staticmethod
	def intersect(left: Collider, right: Collider) -> bool:
		leftTr : Transform = left.GetOwner().GetComponent(Enums.ComponentType.Transform)
		rightTr : Transform = right.GetOwner().GetComponent(Enums.ComponentType.Transform)

		leftPosition = leftTr.GetPosition() + left.GetOffset()
		rightPosition = rightTr.GetPosition() + right.GetOffset()

		leftSize = left.GetSize() * 100
		rightSize = right.GetSize() * 100

		leftType = left.GetCollisionType()
		rightType = right.GetCollisionType()

		if leftType == Enums.ColliderType.Box2D and rightType == Enums.ColliderType.Box2D:
			leftBoxCenter = leftPosition + (leftSize / 2.0)
			rightBoxCenter = rightPosition + (rightSize / 2.0)
			if (abs(leftBoxCenter.x - rightBoxCenter.x) < abs(leftSize.x / 2.0 + rightSize.x / 2.0) and
					abs(leftBoxCenter.y - rightBoxCenter.y) < abs(leftSize.y / 2.0 + rightSize.y / 2.0)):
				return True
		elif leftType == Enums.ColliderType.Circle and rightType == Enums.ColliderType.Circle:
			leftCircleCenter : Vector2 = leftPosition + (leftSize / 2.0)
			rightCircleCenter : Vector2  = rightPosition + (rightSize / 2.0)
			distance : float = (leftCircleCenter - rightCircleCenter).length()
			if distance < ((leftSize.x / 2.0) + (rightSize.x / 2.0)):
				return True
		elif ((leftType == Enums.ColliderType.Box2D and rightType == Enums.ColliderType.Circle) or
				(Enums.ColliderType.Circle and rightType == Enums.ColliderType.Box2D)):
			circleCenter : Vector2 = rightPosition + (rightSize / 2.0) if leftType == Enums.ColliderType.Box2D \
				else leftPosition + (leftSize / 2.0)
			boxPosition : Vector2 = leftPosition if leftType == Enums.ColliderType.Box2D else rightPosition
			boxSize : Vector2 = leftSize if leftType == Enums.ColliderType.Box2D else rightSize

			boxRightBottom : Vector2 = boxPosition + boxSize + (rightSize / 2.0)
			boxLeftTop : Vector2 = boxPosition - (rightSize / 2.0)

			if (boxLeftTop.x < circleCenter.x < boxRightBottom.x and
					boxLeftTop.y < circleCenter.y < boxRightBottom.y):
				return True

		return False

	@staticmethod
	def clear() -> None:
		CollisionManager.collision_map.clear()
		CollisionManager.collision_layer_matrix = [[False] * Enums.LayerType.End.value for _ in range(Enums.LayerType.End.value)]