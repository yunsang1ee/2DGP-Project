from pico2d import *

from framework.Application import app

def main():
    from Scene.mainScene import MainScene
    open_canvas(1200, 900)
    
    app.Init(get_canvas_width(), get_canvas_height())
    app.CreateScene('mainScene', MainScene())
    app.LoadScene('mainScene')
    
    while app.running:
        app.Run()
    app.Release()

    pass

if __name__ == "__main__":
    main()