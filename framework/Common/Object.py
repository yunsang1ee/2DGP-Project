from pygame import Vector2

from framework.Common.Enums import LayerType
from framework.Component.Transform import Transform
from framework.GameObject.GameObject import GameObject
from framework.Application import app

def Instantiate(layer : LayerType, vec2 : Vector2 = None):
	newObject = GameObject()
	newObject.layer = layer
	
	if vec2 is not None:
		tr : Transform = newObject.AddComponent(Transform)
		tr.SetPosition(vec2)
		
	app.activeScene.AddObject(newObject)
	return newObject