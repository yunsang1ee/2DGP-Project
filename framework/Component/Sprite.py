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
		self.name : str = None
		self.image : Image = None
		self.curAction : str = None
		self.action : Dict[str, ImageInfo] = {}
		self.offset : Vector2 = Vector2(0, 0)
		pass
	
	def Update(self):
		pass
	
	def LateUpdate(self):
		info = self.action[self.curAction]
		if (not info.repeat) and info.isComplete: return
		if self.curAction is not None:
			delta = timer.GetDeltaTime()
			info.curFrame = info.curFrame + info.frameSpeed * delta
			if info.curFrame > info.frameCount:
				info.isComplete = True
				if info.repeat: info.curFrame %= info.frameCount
				else: info.curFrame -= 1
		pass
	
	def Render(self):
		tr: Transform = self.GetOwner().GetComponent(Enums.ComponentType.Transform)
		if self.curAction is not None:
			info = self.action[self.curAction]
			left = int(info.offset.x + (int(info.curFrame) % info.frameWidth) * (info.size.x + 1))
			bottom = int(info.offset.y - (int(info.curFrame) // info.frameWidth) * (info.size.y + 1))
			position = tr.GetPosition()
			from framework.Application import mainCamera
			if mainCamera:
				position = mainCamera.CalculatePosition(position)
			scale = tr.GetScale()
			# print(f'{left=}, {bottom=}')
			self.image.clip_composite_draw(left, bottom
			                               , int(info.size.x), int(info.size.y)
			                               , tr.GetRotation()
			                               , info.flip
			                               , position.x + self.offset.x, position.y + self.offset.y
			                               , int(info.size.x * scale.x), int(info.size.y * scale.y))
		pass
	
	def SetImage(self, path: str):
		self.name = path[0:path.find('.')]
		self.image = load_image("./resource/" + path)
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
	
	def SetActionSpeed(self,name : str = None, frameSpeed : int = 5):
		if name is None:
			self.action[self.curAction].frameSpeed = frameSpeed
		else:
			self.action[name].frameSpeed = frameSpeed
		pass
	
	def SetOffset(self, offset : Vector2):
		self.offset = offset
		pass
	
	def SetFlip(self, name : str, flip : str):
		self.action[name].flip = flip
		pass
	def SetAllFlip(self, flip : str):
		for info in self.action.values():
			info.flip = flip
		pass
	pass