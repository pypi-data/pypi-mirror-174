import pynput

from .gui_api_server import GuiApiServer
from .. import services
from ..cfg import Cfg


# --------------------
## holds functions to interact with tkinter and the server
class GuiApiTinker:
    # --------------------
    ## constructor
    def __init__(self):
        ## the top level root window for the GUI
        self._window = None
        ## the top level menu
        self._menu = None
        ## the current screen content
        self._screen = None

        services.guiapi = self
        services.server = GuiApiServer()

    # --------------------
    ## initialize. Configure and start the server
    #
    # @param ip_address   (optional) the socket address for the server
    # @param ip_port      (optional) the socket port for the server
    # @param logger       (optional) reference to a logger object
    # @param verbose      (optional) flag indicating if verbose logging is required
    # @param callback     (optional) reference to callback function for unknown incoming commands
    # @return None
    def init(self, ip_address=None, ip_port=None, logger=None, verbose=None, callback=None):
        services.cfg = Cfg()
        if logger is not None:
            services.logger = logger
        if verbose is not None:
            services.cfg.verbose = verbose
        if ip_address is not None:
            services.cfg.ip_address = ip_address
        if ip_port is not None:
            services.cfg.ip_port = ip_port
        if callback is not None:
            services.cfg.callback = callback

        services.server.init()
        self._window = None
        self._menu = None
        self._screen = None

    # --------------------
    ## set the TK root window
    #
    # @param window   the TK root window
    # @return None
    def set_window(self, window):
        self._window = window

    # --------------------
    ## set the top level menu
    #
    # @param menu  the top level menu
    # @return None
    def set_menu(self, menu):
        self._menu = menu

    # --------------------
    ## in the given widget, set an internal name to be used for screen dump purposes
    #
    # @param widget  the widget to set the name in
    # @param name    the name to use
    # @return None
    def set_name(self, widget, name):
        setattr(widget, 'guiapi_name', name)

    # --------------------
    ## generate a left mouse button click at the given screen coordinates
    #
    # @param x   the x value in screen coordinates
    # @param y   the y value in screen coordinates
    # @return None
    def click_left(self, x, y):
        services.logger.info(f'click_left: {x} {y}')
        m = pynput.mouse.Controller()
        prev_posn = m.position
        m.position = (x, y)
        m.click(pynput.mouse.Button.left, 1)
        # restore previous mouse position
        m.position = prev_posn

    # --------------------
    ## get a screen dump in JSON format of the currently displayed screen(s)
    #
    # @return screen content in JSON format
    def get_screen(self):
        services.logger.info('get_screen')
        self._screen = self._report_window(self._window)

        # services.logger.info(f'screen:\n{json.dumps(self._screen, indent=4)}')
        services.logger.info('get_screen done')
        return self._screen

    # --------------------
    ## get screen content for the given window in JSON format
    #
    # @param w  the window to get the screen content for
    # @return screen content in JSON format
    def _report_window(self, w):
        n = {
            'class': w.winfo_class(),
            'name': getattr(w, 'guiapi_name', 'unknown'),
            'title': w.title(),
            'geometry': w.geometry(),
        }
        self._get_coordinates(w, n)

        n['children'] = []
        for frame in w.winfo_children():
            child = {}
            self._report_child(frame, child)
            n['children'].append(child)

        return n

    # --------------------
    ## get screen content for the given frame in JSON format
    #
    # @param f  the frame to get the screen content for
    # @param n  the node/widget to get the screen content for
    # @return screen content in JSON format
    def _report_child(self, f, n):
        n['class'] = f.winfo_class()
        n['name'] = getattr(f, 'guiapi_name', 'unknown')

        # menus are handled differently
        if f.winfo_class() in ['Menu']:
            n['menu'] = []
            for index in range(0, f.index('end') + 1):
                if f.type(index) in ['command', 'cascade']:
                    menuitem = {
                        'index': index,
                        'type': f.type(index),
                        'label': f.entrycget(index, 'label'),
                        'state': f.entrycget(index, 'state'),
                    }
                    n['menu'].append(menuitem)
        else:
            # text on the screen and the current enable/disable state
            if f.winfo_class() in ['Label', 'Button']:
                n['value'] = f.cget('text')
                n['state'] = f.cget('state')
            else:
                n['value'] = '<unknown>'
                n['state'] = '<unknown>'

        self._get_coordinates(f, n)

        n['children'] = []
        for c in f.winfo_children():
            child = {}
            self._report_child(c, child)
            n['children'].append(child)

    # --------------------
    ## get coordinates for the given widget and add it to the current node
    #
    # @param f  the frame/widget to get the screen content for
    # @param n  the node to add the coordinates to
    # @return None
    def _get_coordinates(self, f, n):
        x1 = f.winfo_rootx()
        y1 = f.winfo_rooty()
        x2 = x1 + f.winfo_width()
        y2 = y1 + f.winfo_height()
        n['coordinates'] = {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
        }

    # --------------------
    ## invoke a menu item with the given menu path
    #
    # @param menu_path   a list of menu indicies to locate the menu item
    # @return ack/nak
    def menu_invoke(self, cmd):
        rsp = {
            'rsp': cmd['cmd'],
            'value': 'ack',
        }

        item = self._menu
        ok = False
        services.logger.info(f'DBG guiapi {cmd["menu_path"]}')
        for index in cmd['menu_path']:
            services.logger.info(f'DBG guiapi item:{item.index("end")}')
            if index <= item.index("end") and index == cmd['menu_path'][-1]:
                services.logger.info(f'DBG guiapi invoke {index} {cmd["menu_path"][-1]}')
                # this index is the last one in the menu_path so invoke it
                item.invoke(index)
                ok = True
                break

            # check the children
            services.logger.info(f'DBG guiapi getting children')
            children = item.winfo_children()
            if len(children) >= 1:
                item = item.winfo_children()[0]
            else:
                break

        if not ok:
            rsp['value'] = 'nak'
            rsp['reason'] = 'menuitem not found'
        services.logger.info(f'DBG guiapi exiting: {rsp}')

        return rsp
