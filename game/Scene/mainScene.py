import os

from pico2d import load_image, Image
from pygame import Vector2

from framework.Common import Object, Enums
from framework.Component.Collider.BoxCollider2D import BoxCollider2D
from framework.Component.Collider.CircleCollider import CircleCollider
from framework.Component.Collider.CollisionManager import CollisionManager
from framework.Component.Component import Component
from framework.Component.Sprite import Sprite
from framework.GameObject.GameObject import GameObject
from framework.Scene import Scene
from game.Script.LumberjackScript import LumberjackScript


class Animation(Component):
	def __init__(self, path: str):
		super().__init__(Enums.ComponentType.Animation)
		self.image = None
		pass
	
	def Update(self):
		pass
	
	def LateUpdate(self):
		pass
	
	def Render(self):
		pass
	
	def SetImage(self, path: str):
		self.image = load_image(path)
		pass
	
	pass


class MainScene(Scene.Scene):
	def __init__(self):
		super().__init__()
		pass
	
	def Update(self):
		super().Update()
		pass
	
	def LateUpdate(self):
		super().LateUpdate()
		pass
	
	def Render(self):
		super().Render()
		pass
	
	def Destroy(self):
		super().Destroy()
		pass
	
	def OnEnter(self):
		super().OnEnter()
		from framework.Application import app
		CollisionManager.CollisionLayerCheck(Enums.LayerType.Enemy, Enums.LayerType.AttackTrigger, True)
		
		background : GameObject = Object.Instantiate(Enums.LayerType.BackGround, app.screen // 2)
		sp : Sprite = background.AddComponent(Sprite)
		sp.SetImage("Background.png")
		sp.AddAction('background', 0, 1, 1, Vector2(0, 0), Vector2(2400, 1800), '')
		
		player: GameObject = Object.Instantiate(Enums.LayerType.Player, app.screen // 2)
		cd: BoxCollider2D = player.AddComponent(BoxCollider2D)
		cd.SetOffset(Vector2(0, -10))
		cd.SetSize(Vector2(0.32, 0.62))
		sp: Sprite = player.AddComponent(Sprite)
		sp.SetImage("Lumberjack.png")
		sp.AddAction('idle', 0, 6, 6
		             , Vector2(67, 1423), Vector2(72, 72), '')
		sp.AddAction('move', 0, 8, 6
		             , Vector2(67, 1314), Vector2(72, 72), '')
		sp.AddAction('attack', 0, 10, 4
		             , Vector2(67, 1168), Vector2(96, 72), '',  repeat=False)
		sp.AddAction('attackCritical', 0, 15, 4
		             , Vector2(67, 949), Vector2(96, 72), '', repeat=False)
		sc: LumberjackScript = player.AddComponent(LumberjackScript); sc.Init()
		
		
		pass
	
	def OnExit(self):
		super().OnExit()
		pass
