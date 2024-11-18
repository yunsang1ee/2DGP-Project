from pico2d import *

from framework.Application import app
from Scene.mainScene import MainScene


def main():
    open_canvas()
    app.Init(get_canvas_width(), get_canvas_height())
    app.CreateScene('mainScene', MainScene())
    app.LoadScene('mainScene')

    while True:
        app.Run()
    app.Release()

    pass

if __name__ == "__main__":
    main()