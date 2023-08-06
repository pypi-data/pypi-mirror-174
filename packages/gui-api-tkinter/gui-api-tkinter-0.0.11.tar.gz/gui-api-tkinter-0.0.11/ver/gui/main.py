import sys

sys.path.append('.')  # noqa: E402
from ver.gui.app import App


# --------------------
## main line
def main():
    app = App()
    app.init()


# --------------------
if __name__ == '__main__':
    main()
