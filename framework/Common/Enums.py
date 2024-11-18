import enum

class LayerType(enum.Enum):
    Non = 0
    BackGround = enum.auto()
    Obstacle = enum.auto()
    Tree = enum.auto()
    Player = enum.auto()
    Enemy = enum.auto()
    Supplies = enum.auto()
    Camera = enum.auto()
    End = enum.auto()
    pass

class ColliderType(enum.Enum):
    Non = 0
    Box2D = enum.auto()
    Circle = enum.auto()
    End = enum.auto()
    pass

class ComponentType(enum.Enum):
    Transform = 0
    Collider = enum.auto()
    Script = enum.auto()
    Sprite = enum.auto()
    Animation = enum.auto()
    Camera = enum.auto()
    End = enum.auto()
    pass