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
		sc: LumberjackScript = player.AddComponent(LumberjackScript); sc.Init()
		
		pass
	
	def OnExit(self):
		super().OnExit()
		pass
