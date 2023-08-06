import time

from .client import Client
from .. import services
from ..cfg import Cfg
from ..logger_null import LoggerNull


# --------------------
## test harness used to communicate with GuiApi Server
class GuiApiHarness:
    # --------------------
    ## constructor
    def __init__(self):
        ## holds reference to common configuration information
        self.cfg = None
        ## holds reference to logger object
        self.logger = None
        ## holds current screen content
        self._content = None
        ## holds reference to the socket client
        self._client = None

    # --------------------
    ## initialize
    #
    # @param logger   (optional) a reference to a logger object
    # @return None
    def init(self, logger=None):
        self.cfg = Cfg()
        services.cfg = self.cfg
        if logger is None:
            self.logger = LoggerNull()
        else:
            self.logger = logger
        services.logger = self.logger

        services.cfg.init()
        self._client = Client()

    # --------------------
    ## terminate
    #
    # @return None
    def term(self):
        if self._client is not None:
            self._client.term()
            self._client = None

    # --------------------
    ## connect to the GUI API server running inside the GUI
    #
    # @return False
    def connect(self):
        ok = False
        if self.is_connected():
            self.logger.info(f'connect(): already connected, ignoring')
        else:
            self._client.init()
            time.sleep(0.5)
            ok = True

        return ok

    # --------------------
    ## check if connected to the server
    #
    # @return True if connected, False otherwise
    def is_connected(self):
        if self._client is None:
            return False

        return self._client.is_connected()

    # --------------------
    ## send a command and wait for a response
    #
    # @param cmd  the command to send
    # @return the response
    def send_recv(self, cmd: dict) -> dict:
        return self._client.send_recv(cmd)

    # --------------------
    ## get the current screen contents in JSON format
    #
    # @return screen content in JSON format
    def get_screen(self) -> list:
        screen = self._client.get_screen()
        # currently can only handle 1 root window,
        # therefore content is a list of one item
        self._content = [screen]
        return self._content

    # --------------------
    ## the current screen contents in JSON format
    #
    # @return the current screen contents in JSON format
    @property
    def content(self) -> dict:
        return self._content

    # --------------------
    ## find the widget matching the path given in the search list
    #
    # @param search_path  a list of widget names
    # @return the widget item if found, None otherwise
    def search(self, search_path: list):
        if self._content is None:
            ack_nak = {
                'rsp': 'search',
                'value': 'nak',
                'reason': 'content is None'
            }
            return ack_nak

        if search_path is None:
            ack_nak = {
                'rsp': 'search',
                'value': 'nak',
                'reason': 'search path is None'
            }
            return ack_nak

        if not search_path:
            ack_nak = {
                'rsp': 'search',
                'value': 'nak',
                'reason': 'search path is empty'
            }
            return ack_nak

        item = self._search_content(self._content, search_path, 0)
        if item is None:
            ack_nak = {
                'rsp': 'search',
                'value': 'nak',
                'reason': 'search path is not found'
            }
            return ack_nak

        # it was found, no errors
        return item

    # --------------------
    ## recursive function to find the widget item that matches the search list
    #
    # @param content      the screen content to search
    # @param search_path  the list of widget names to search
    # @param index        the current entry in the search_list
    # @return the widget item if matches the last entry in search_list, None otherwise
    def _search_content(self, content, search_path, index=0):
        if content is None or \
                search_path is None or \
                len(search_path) == 0:
            return None

        # uncomment to debug
        # self.logger.info(f'DBG searching index={index} srch={search_path}')
        search_name = search_path[index]
        for item in content:
            if item['name'] == search_name:
                if index == len(search_path) - 1:
                    # uncomment to debug
                    # self.logger.info(f'DBG found it  index={index} node={item}')
                    return item

                # it matched, but not at the end of the search list, so check the children
                # uncomment to debug
                # self.logger.info(f'DBG children  index={index} srch={search_name} curr={item["name"]}')
                node = self._search_content(item['children'], search_path, index + 1)
                if node is not None:
                    return node

        # uncoment to debug
        # self.logger.info(f'DBG not_found index={index} {search_name}')
        return None

    # --------------------
    ## click left mouse button at given screen coordinates
    #
    # @param x   the x value in screen coordinates
    # @param y   the y value in screen coordinates
    # @return None
    def click_left_at(self, x: int, y: int):
        if not isinstance(x, int):
            ack_nak = {
                'rsp': 'click_left_at',
                'value': 'nak',
                'reason': 'click x-coordinate is not an integer'
            }
            return ack_nak

        if not isinstance(y, int):
            ack_nak = {
                'rsp': 'click_left_at',
                'value': 'nak',
                'reason': 'click y-coordinate is not an integer'
            }
            return ack_nak

        ack_nak = self._client.click_left(x, y)
        if 'reason' in ack_nak:
            ack_nak['rsp'] = 'click_left_at'
            return ack_nak

        ack_nak = {
            'rsp': 'click_left_at',
            'value': 'ack',
        }
        return ack_nak

    # --------------------
    ## click the left mouse button on the given widget item
    #
    # @param item  the widget item to click on
    # @return None
    def click_left_on(self, item: dict):
        if item is None:
            ack_nak = {
                'rsp': 'click_left_on',
                'value': 'nak',
                'reason': 'click item is None'
            }
            return ack_nak

        if 'coordinates' not in item:
            ack_nak = {
                'rsp': 'click_left_on',
                'value': 'nak',
                'reason': 'click item missing coordinates values'
            }
            return ack_nak

        x = int((item['coordinates']['x1'] + item['coordinates']['x2']) / 2)
        y = int((item['coordinates']['y1'] + item['coordinates']['y2']) / 2)
        ack_nak = self.click_left_at(x, y)
        if 'reason' in ack_nak:
            ack_nak['rsp'] = 'click_left_on'
            return ack_nak

        ack_nak = {
            'rsp': 'click_left_on',
            'value': 'ack',
        }
        return ack_nak

    # --------------------
    ## click the left mouse button on the widget at the given search list
    #
    # @param click_path  the path to the widget
    # @return None
    def click_left(self, click_path: list):
        if click_path is None:
            ack_nak = {
                'rsp': 'click_left',
                'value': 'nak',
                'reason': 'click path is None'
            }
            return ack_nak

        if not click_path:
            ack_nak = {
                'rsp': 'click_left',
                'value': 'nak',
                'reason': 'click path is empty'
            }
            return ack_nak

        item = self.search(click_path)
        if 'reason' in item:
            item['rsp'] = 'click_left'
            return item

        ack_nak = self.click_left_on(item)
        if 'reason' in ack_nak:
            item['rsp'] = 'click_left'
            return ack_nak

        ack_nak = {
            'rsp': 'click_left',
            'value': 'ack',
        }
        return ack_nak

    # --------------------
    ## select the menu item at the given menu path
    #
    # @param menu_path   the list of menu indicies to search
    # @return ack_nak response
    def menu_click(self, menu_path: list):
        if menu_path is None:
            ack_nak = {
                'rsp': 'menu_click',
                'value': 'nak',
                'reason': 'menu path is None'
            }
        elif not menu_path:
            ack_nak = {
                'rsp': 'menu_click',
                'value': 'nak',
                'reason': 'menu path is empty'
            }
        else:
            ack_nak = self._client.menu_click(menu_path)

        return ack_nak
