import os
from inspect import stack
from random import randint

from pico2d import load_image, Image
from pygame import Vector2

from framework.Application import app
from framework.Common import Object, Enums
from framework.Common.Timer import timer
from framework.Component.Collider.BoxCollider2D import BoxCollider2D
from framework.Component.Collider.CircleCollider import CircleCollider
from framework.Component.Collider.CollisionManager import CollisionManager
from framework.Component.Component import Component
from framework.Component.Sprite import Sprite
from framework.Component.Transform import Transform
from framework.GameObject.GameObject import GameObject
from framework.Scene import Scene
from game.Script.LumberjackScript import LumberjackScript
from game.Script.Monster import ZombieScript, WarthogScript


class MainScene(Scene.Scene):
	def __init__(self):
		super().__init__()
		self.player : GameObject = None
		self.zombies : list[GameObject] = []
		self.warthogs : list[GameObject] = []
		self.EnemyGenTimer : Vector2 = Vector2(0, )
		pass
	
	def Update(self):
		self.EnemyGenTimer.x += timer.GetDeltaTime()
		if self.EnemyGenTimer.x >= self.EnemyGenTimer.y:
			self.EnemyGenTimer.x = 0.0
			for _ in range(5):
				special = randint(1, 10000)
				enemy : GameObject = None
				if special < 8000:
					enemy = self.zombies[-1]
				else:
					enemy = self.warthogs[-1]
					
				tr : Transform = enemy.GetComponent(Enums.ComponentType.Transform)
				playerTr : Transform = self.player.GetComponent(Enums.ComponentType.Transform)
				minPos = playerTr.GetPosition() - app.screen
				maxPos = playerTr.GetPosition() + app.screen
				tr.SetPosition(Vector2(
					randint(max(-700, int(minPos.x)), min(1500, maxPos.x))
					, randint(max(-500, int(minPos.y)), min(1100, maxPos.y))
					)
				)
				
				enemy.SetState(GameObject.State.Alive)
			
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
		CollisionManager.CollisionLayerCheck(Enums.LayerType.Enemy, Enums.LayerType.AttackTrigger, True)
		CollisionManager.CollisionLayerCheck(Enums.LayerType.Player, Enums.LayerType.Enemy, True)
		CollisionManager.CollisionLayerCheck(Enums.LayerType.Player, Enums.LayerType.EnemyAttackTrigger, True)
		
		background : GameObject = Object.Instantiate(Enums.LayerType.BackGround, app.screen // 2)
		sp : Sprite = background.AddComponent(Sprite)
		sp.SetImage("Background.png")
		sp.AddAction('background', 0, 1, 1, Vector2(0, 0), Vector2(2400, 1800), '')
		
		self.player: GameObject = Object.Instantiate(Enums.LayerType.Player, app.screen // 2)
		sc: LumberjackScript = self.player.AddComponent(LumberjackScript); sc.Init()
		
		for _ in range(120):
			zombie : GameObject = Object.Instantiate(Enums.LayerType.Enemy, Vector2())
			sc : ZombieScript = zombie.AddComponent(ZombieScript); sc.Init()
			zombie.SetState(GameObject.State.Paused)
			self.zombies.append(zombie)
		
		for _ in range(30):
			warthog : GameObject = Object.Instantiate(Enums.LayerType.Enemy, Vector2())
			sc : ZombieScript = warthog.AddComponent(WarthogScript); sc.Init()
			warthog.SetState(GameObject.State.Paused)
			self.warthogs.append(warthog)
		
		pass
	
	def OnExit(self):
		super().OnExit()
		pass
	
	def ReturnZombie(self, zombie: GameObject):
		self.zombies.append(zombie)
		
	def ReturnWarthog(self, warthog: GameObject):
		self.warthogs.append(warthog)