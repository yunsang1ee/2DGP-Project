from framework.Common import Enums
from framework.Common.Timer import timer
from framework.Component.Script import Script
from framework.Component.Sprite import Sprite
from game.Script.LumberjackScript import LumberjackScript


class UIScript(Script):
	def __init__(self):
		super().__init__()
		pass
	
	def Update(self):
		pass
	
	def LateUpdate(self):
		pass
	
	def Render(self):
		from framework.Application import app
		scene = app.activeScene
		playerSc : LumberjackScript = scene.player.GetComponent(Enums.ComponentType.Script)
		app.activeScene.font40.draw(app.screen.x // 2, app.screen.y - 72, f'RunTime: {int(timer.runTime)}', (0, 0, 255))
		app.activeScene.font40.draw(20, app.screen.y - 72, f'HP: {int(playerSc.health)}', (255, 0, 0))
		app.activeScene.font40.draw(20, app.screen.y - 144, f'HUN: {int(playerSc.hungry)}', (253, 126, 20))
		app.activeScene.font40.draw(20, app.screen.y - 216, f'Tomato: {int(playerSc.tomatoCount)}', (220, 50, 69))
		app.activeScene.font40.draw(20, app.screen.y - 288, f'Medikit: {int(playerSc.medikitCount)}', (255, 193, 7))
		app.activeScene.font40.draw(20, app.screen.y - 360, f'Energy: {int(playerSc.energyCount)}', (0, 123, 255))
		app.activeScene.font40.draw(20, app.screen.y - 432, f'Timber: {int(playerSc.timberCount)}', (123, 63, 0))
		
		sc : LumberjackScript = app.activeScene.player.GetComponent(Enums.ComponentType.Script)
		sp : Sprite = app.activeScene.player.GetComponent(Enums.ComponentType.Sprite)
		from framework.Common.InputManager import inputManager
		if (sc.generateReached
				and sc.energyCount >= 5
				and sp.name == 'Lumberjack'
				and inputManager.GetKey('e')
		):
			from framework.Application import app
			from framework.Application import mainCamera
			from framework.Component.Transform import Transform
			tr : Transform = app.activeScene.player.GetComponent(Enums.ComponentType.Transform)
			pos = mainCamera.CalculatePosition(tr.GetPosition())
			app.activeScene.font20.draw(pos.x - 20, pos.y + 40
			                            , f'{sc.evolutionTimer.x:.1f}/{sc.evolutionTimer.y:.1f}', (255, 255, 0))
		pass
	
	def OnCollisionEnter(self, other: 'Collider'):
		pass
	
	def OnCollisionStay(self, other: 'Collider'):
		pass
	
	def OnCollisionExit(self, other: 'Collider'):
		pass
	
	