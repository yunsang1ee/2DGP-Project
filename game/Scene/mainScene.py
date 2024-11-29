from random import randint

from pico2d import *
from pygame import Vector2

from framework.Application import app
from framework.Common import Object, Enums
from framework.Common.Timer import timer
from framework.Component.Collider.CollisionManager import CollisionManager
from framework.Component.Sprite import Sprite
from framework.Component.Transform import Transform
from framework.GameObject.GameObject import GameObject
from framework.Scene import Scene
from game.Script.LumberjackScript import LumberjackScript
from game.Script.MonsterScripts import ZombieScript, WarthogScript
from game.Script.UIScript import UIScript


class MainScene(Scene.Scene):
	def __init__(self):
		super().__init__()
		self.player : GameObject = None
		self.zombies : list[GameObject] = []
		self.warthogs : list[GameObject] = []
		self.EnemyGenTimer : Vector2 = Vector2(0, 6.0)
		# 50 MPM(mob per minute) -> bossTimer == 10 minute -> (50 * 0.2 = 10) * 10 = 100 -> 100 * 0.1 = 10 energy
		self.font20 : Font = load_font('game/resource/ThornFont.ttf', 20)
		self.font40 : Font = load_font('game/resource/ThornFont.ttf', 40)
		self.font72 : Font = load_font('game/resource/ThornFont.ttf', 72)
		pass
	
	def Update(self):
		self.EnemyGenTimer.x += timer.GetDeltaTime()
		if self.EnemyGenTimer.x >= self.EnemyGenTimer.y:
			self.EnemyGenTimer.x = 0.0
			for _ in range(5):
				special = randint(1, 10000)
				enemy : GameObject = None
				sc = None
				if special < 8000:
					if len(self.zombies) > 0:
						enemy = self.zombies.pop()
						sc : ZombieScript = enemy.GetComponent(Enums.ComponentType.Script)
				else:
					if len(self.warthogs) > 0:
						enemy = self.warthogs.pop()
						sc : WarthogScript = enemy.GetComponent(Enums.ComponentType.Script)
				if enemy is None: continue

				sc.Regen()

				tr : Transform = enemy.GetComponent(Enums.ComponentType.Transform)
				playerTr : Transform = self.player.GetComponent(Enums.ComponentType.Transform)
				minPos = playerTr.GetPosition() - app.screen
				maxPos = playerTr.GetPosition() + app.screen
				tr.SetPosition(Vector2(
					randint(max(-700, int(minPos.x)), min(1500, int(maxPos.x)))
					, randint(max(-500, int(minPos.y)), min(1100, int(maxPos.y))))
				)

				enemy.SetState(GameObject.State.Alive)
		
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
		CollisionManager.CollisionLayerCheck(Enums.LayerType.Enemy, Enums.LayerType.Obstacle, True)
		CollisionManager.CollisionLayerCheck(Enums.LayerType.Obstacle, Enums.LayerType.EnemyAttackTrigger, True)
		
		ui : GameObject = Object.Instantiate(GameObject, Enums.LayerType.UI); ui.AddComponent(UIScript)
		
		background : GameObject = Object.Instantiate(GameObject, Enums.LayerType.BackGround, app.screen // 2)
		sp : Sprite = background.AddComponent(Sprite)
		sp.SetImage("Background.png")
		sp.AddAction('background', 0, 1, 1, Vector2(0, 0), Vector2(2400, 1800), '')
		
		self.player: GameObject = Object.Instantiate(GameObject, Enums.LayerType.Player, app.screen // 2)
		sc: LumberjackScript = self.player.AddComponent(LumberjackScript); sc.Init()
		
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