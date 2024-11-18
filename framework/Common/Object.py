from pygame import Vector2

from framework.Common.Enums import LayerType
from framework.Component.Transform import Transform
from framework.GameObject.GameObject import GameObject
from framework.Application import app

def Instantiate(layer : LayerType, position : Vector2 = None, rotation : float = None) -> GameObject:
	newObject = GameObject()
	newObject.layer = layer
	
	if position is not None:
		tr : Transform = newObject.AddComponent(Transform)
		tr.SetPosition(position)
		
		if rotation is not None:
			tr.SetRotation(rotation)
		
	app.activeScene.AddObject(newObject)
	return newObject

def Destroy(object : GameObject):
	object.state = GameObject.State.Dead