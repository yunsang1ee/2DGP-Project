from framework.Common import Enums
from framework.Component.Script import Script
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
		playerSc = scene.player.GetComponent(Enums.ComponentType.Script)
		app.activeScene.font72.draw(20, app.screen.y - 72, f'HP: {int(playerSc.health)}', (255, 0, 0))
		app.activeScene.font72.draw(20, app.screen.y - 144, f'HUN: {int(playerSc.hungry)}', (255, 50, 10))
		pass
	
	def OnCollisionEnter(self, other: 'Collider'):
		pass
	
	def OnCollisionStay(self, other: 'Collider'):
		pass
	
	def OnCollisionExit(self, other: 'Collider'):
		pass
	
	