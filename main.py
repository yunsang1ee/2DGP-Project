from pico2d import *

from Application import app

def main():
    open_canvas()
    app.Init()

    while True:
        app.Run()
    app.Release()

if __name__ == "__main__":
    main()