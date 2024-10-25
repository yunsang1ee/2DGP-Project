from pico2d import *

from Application import app
from Scene import Scene


def main():

    open_canvas()
    app.Init(get_canvas_width(), get_canvas_height())
    app.CreateScene('mainScene', Scene())
    app.LoadScene('mainScene')

    while True:
        app.Run()
    app.Release()
if __name__ == "__main__":
    main()