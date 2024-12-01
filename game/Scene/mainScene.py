from random import randint

from pico2d import *
from pygame import Vector2

from framework.Application import app
from framework.Common import Object, Enums
from framework.Common.Timer import timer
from framework.Component.Camera import Camera
from framework.Component.Collider.CollisionManager import CollisionManager
from framework.Component.Component import Component
from framework.Component.Sprite import Sprite
from framework.Component.Transform import Transform
from framework.GameObject.GameObject import GameObject
from framework.Scene import Scene
from game.Script.LumberjackScript import LumberjackScript
from game.Script.MonsterScripts import ZombieScript, WarthogScript
from game.Script.SuppliesScript import TomatoScript, MedikitScript, TreeScript, GeneratorScript
from game.Script.UIScript import UIScript

class MainScene(Scene.Scene):
	def __init__(self):
		super().__init__()
		self.player : GameObject = None
		self.zombies : list[GameObject] = []
		self.warthogs : list[GameObject] = []
		self.enemyGenTimer : Vector2 = Vector2(0, 6.0)
		# 50 MPM(mob per minute) -> bossTimer == 10 minute -> (50 * 0.2 = 10) * 10 = 100 -> 100 * 0.1 = 10 energy
		self.suppliesGenTimer : Vector2 = Vector2(0, 10.0)
		self.font20 : Font = load_font('game/resource/ThornFont.ttf', 20)
		self.font40 : Font = load_font('game/resource/ThornFont.ttf', 40)
		self.font72 : Font = load_font('game/resource/ThornFont.ttf', 72)
		pass
	
	def Update(self):
		self.genEnemy()
		
		"""
		Hungry Warning Point 50 (50 -> player Speed <= Monster Speed)
		10 tmt/m
		10 Hp/tmt
		-0.8 Hp/s -> -48 Hp/m
		-2.0 Hp/LeftClick
		(10s Timer)  average 10 tomato/m -> 5~15 Gen
		-> Gen/10s -> 5 Gen/m -> average 2 tomato/Gen -> 1 ~ 3 Gen
		"""
		self.genSupplies()
		
		def function(obj : GameObject):
			layer = obj.GetLayer()
			tr : Transform = obj.GetComponent(Enums.ComponentType.Transform)
			y = tr.GetPosition().y if tr is not None else 0
			return (layer != Enums.LayerType.BackGround
			        , layer == Enums.LayerType.UI
			        , -y)
		self.objects.sort(key=function)
		
		super().Update()
		pass
	
	def genSupplies(self):
		self.suppliesGenTimer.x += timer.GetDeltaTime()
		if self.suppliesGenTimer.x >= self.suppliesGenTimer.y:
			self.suppliesGenTimer.x = 0.0
			special = randint(1, 10000)
			count = math.ceil(special / 3333)
			
			playerTr: Transform = self.player.GetComponent(Enums.ComponentType.Transform)
			minPos = playerTr.GetPosition() - app.screen
			maxPos = playerTr.GetPosition() + app.screen
			
			for _ in range(count):
				tomato: GameObject = Object.Instantiate(GameObject, Enums.LayerType.Supplies, Vector2(
					randint(max(-700, int(minPos.x)), min(1500, int(maxPos.x)))
					, randint(max(-500, int(minPos.y)), min(1100, int(maxPos.y)))))
				sc = tomato.AddComponent(TomatoScript);sc.Init()
			
			special = randint(1, 10000)
			if special <= 1294:
				medikit = Object.Instantiate(GameObject, Enums.LayerType.Supplies, Vector2(
					randint(max(-700, int(minPos.x)), min(1500, int(maxPos.x)))
					, randint(max(-500, int(minPos.y)), min(1100, int(maxPos.y)))))
				sc = medikit.AddComponent(MedikitScript);sc.Init()
				
			special = randint(1, 10000)
			if special <= 3333:
				for _ in range(randint(2, 3)):
					tree = Object.Instantiate(GameObject, Enums.LayerType.Tree, Vector2(
						randint(max(-700, int(minPos.x)), min(1500, int(maxPos.x)))
						, randint(max(-500, int(minPos.y)), min(1100, int(maxPos.y)))))
					sc : TreeScript = tree.AddComponent(TreeScript); sc.Init()
					
			special = randint(1, 10000)
			if special <= 10000:
				generator = Object.Instantiate(GameObject, Enums.LayerType.Supplies, Vector2(
					randint(max(-700, int(minPos.x)), min(1500, int(maxPos.x)))
					, randint(max(-500, int(minPos.y)), min(1100, int(maxPos.y)))))
				sc : GeneratorScript = generator.AddComponent(GeneratorScript); sc.Init()
	
	def genEnemy(self):
		self.enemyGenTimer.x += timer.GetDeltaTime()
		if self.enemyGenTimer.x >= self.enemyGenTimer.y:
			self.enemyGenTimer.x = 0.0
			for _ in range(5):
				special = randint(1, 10000)
				enemy: GameObject = None
				sc = None
				if special <= 8000:
					if len(self.zombies) > 0:
						enemy = self.zombies.pop()
						sc: ZombieScript = enemy.GetComponent(Enums.ComponentType.Script)
				else:
					if len(self.warthogs) > 0:
						enemy = self.warthogs.pop()
						sc: WarthogScript = enemy.GetComponent(Enums.ComponentType.Script)
				if enemy is None: continue
				
				sc.Regen()
				
				tr: Transform = enemy.GetComponent(Enums.ComponentType.Transform)
				playerTr: Transform = self.player.GetComponent(Enums.ComponentType.Transform)
				minPos = playerTr.GetPosition() - app.screen
				maxPos = playerTr.GetPosition() + app.screen
				tr.SetPosition(Vector2(
					randint(max(-700, int(minPos.x)), min(1500, int(maxPos.x)))
					, randint(max(-500, int(minPos.y)), min(1100, int(maxPos.y))))
				)
				
				enemy.SetState(GameObject.State.Alive)
	
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
		CollisionManager.CollisionLayerCheck(Enums.LayerType.Enemy, Enums.LayerType.Player, True)
		CollisionManager.CollisionLayerCheck(Enums.LayerType.Player, Enums.LayerType.EnemyAttackTrigger, True)
		CollisionManager.CollisionLayerCheck(Enums.LayerType.Player, Enums.LayerType.Supplies, True)
		CollisionManager.CollisionLayerCheck(Enums.LayerType.AttackTrigger, Enums.LayerType.Tree, True)
		CollisionManager.CollisionLayerCheck(Enums.LayerType.Enemy, Enums.LayerType.Obstacle, True)
		CollisionManager.CollisionLayerCheck(Enums.LayerType.Obstacle, Enums.LayerType.EnemyAttackTrigger, True)
		
		ui : GameObject = Object.Instantiate(GameObject, Enums.LayerType.UI); ui.AddComponent(UIScript)
		
		background : GameObject = Object.Instantiate(GameObject, Enums.LayerType.BackGround, app.screen // 2)
		sp : Sprite = background.AddComponent(Sprite)
		sp.SetImage("Background.png")
		sp.AddAction('background', 0, 1, 1, Vector2(0, 0), Vector2(2400, 1800), '')
		
		self.player: GameObject = Object.Instantiate(GameObject, Enums.LayerType.Player, app.screen // 2)
		sc: LumberjackScript = self.player.AddComponent(LumberjackScript); sc.Init()
		
		camera = Object.Instantiate(GameObject, Enums.LayerType.Camera)
		
		from framework import Application
		Application.mainCamera = camera.AddComponent(Camera)
		Application.mainCamera.SetTarget(self.player)
		
		for _ in range(120):
			zombie : GameObject = Object.Instantiate(GameObject, Enums.LayerType.Enemy, Vector2())
			sc : ZombieScript = zombie.AddComponent(ZombieScript); sc.Init()
			zombie.SetState(GameObject.State.Paused)
			self.zombies.append(zombie)
		# TEST ZOMBIE
		# enemy = self.zombies[-1]
		# sc : ZombieScript = enemy.GetComponent(Enums.ComponentType.Script)
		# sc.Regen()
		# tr: Transform = enemy.GetComponent(Enums.ComponentType.Transform)
		# playerTr: Transform = self.player.GetComponent(Enums.ComponentType.Transform)
		# minPos = playerTr.GetPosition() - app.screen
		# maxPos = playerTr.GetPosition() + app.screen
		# tr.SetPosition(Vector2(
		# 	randint(max(-700, int(minPos.x)), min(1500, int(maxPos.x)))
		# 	, randint(max(-500, int(minPos.y)), min(1100, int(maxPos.y))))
		# )
		# enemy.SetState(GameObject.State.Alive)
		#
		for _ in range(30):
			warthog : GameObject = Object.Instantiate(GameObject, Enums.LayerType.Enemy, Vector2())
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