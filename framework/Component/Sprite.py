from typing import Dict

from pico2d import *
from pygame import Vector2

from framework.Common import Enums
from framework.Common.Timer import timer
from framework.Component.Component import Component
from framework.Component.Transform import Transform

class ImageInfo:
	def __init__(self, frame : float, frameCount : int, frameWidth : int
	             , offset : Vector2, size : Vector2, flip : str, frameSpeed : int, repeat : bool):
		self.curFrame : float = frame
		self.frameCount : int = frameCount
		self.frameWidth : int = frameWidth
		self.offset : Vector2 = offset
		self.size : Vector2 = size
		self.flip : str = flip
		self.frameSpeed : int = frameSpeed
		self.repeat : bool = repeat
		self.isComplete : bool = False
		pass
	pass

class Sprite(Component):
	def __init__(self, ):
		super().__init__(Enums.ComponentType.Sprite)
		self.image : Image = None
		self.curAction : str = None
		self.action : Dict[str, ImageInfo] = {}
		pass
	
	def Update(self):
		pass
	
	def LateUpdate(self):
		if self.curAction is not None:
			info = self.action[self.curAction]
			info.curFrame = info.curFrame + info.frameSpeed * timer.GetDeltaTime()
			if info.curFrame > info.frameCount:
				info.isComplete = True
				info.curFrame %= info.frameCount
		pass
	
	def Render(self):
		tr: Transform = self.GetOwner().GetComponent(Enums.ComponentType.Transform)
		if self.curAction is not None:
			info = self.action[self.curAction]
			left = int(info.offset.x + (int(info.curFrame) % info.frameWidth) * (info.size.x + 1))
			bottom = int(info.offset.y - (int(info.curFrame) // info.frameWidth) * (info.size.y + 1))
			# print(f'{left=}, {bottom=}')
			self.image.clip_composite_draw(left, bottom
			                               , int(info.size.x), int(info.size.y)
			                               , tr.GetRotation()
			                               , info.flip
			                               , tr.GetPosition().x, tr.GetPosition().y
			                               , int(info.size.x), int(info.size.y))
		pass
	
	def SetImage(self, path: str):
		self.image = load_image("game/resource/" + path)
		pass
	
	def AddAction(self, name : str, frame : float, frameCount : int, frameWidth : int
	              , offset : Vector2, size : Vector2, flip : str, frameSpeed : int = 5, repeat : bool = True):
		self.curAction = name
		self.action[name] = ImageInfo(frame, frameCount, frameWidth
		                              , offset, size, flip, frameSpeed, repeat)
		pass
	def SetAction(self, name : str):
		self.curAction = name
		self.action[self.curAction].curFrame = 0
		self.action[self.curAction].isComplete = False
		pass
	
	def SetActionSpeed(self,name : str, frameSpeed : int):
		self.action[name].frameSpeed = frameSpeed
		pass
	
	def SetFlip(self, name : str, flip : str):
		self.action[name].flip = flip
		pass
	pass