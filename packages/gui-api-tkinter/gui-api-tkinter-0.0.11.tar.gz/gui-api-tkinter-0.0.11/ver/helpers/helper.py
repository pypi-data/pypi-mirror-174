import time

from ver.helpers import services
from ver.helpers.cmd_runner import CmdRunner


# --------------------
class Helper:

    # --------------------
    def __init__(self):
        self.gui_process = None

        self.button1_path = ['window1', 'page1_frame', 'button_frame', 'button1']
        self.label1_path = ['window1', 'page1_frame', 'button_frame', 'label1']
        self.menu_clear_path = [2]

    # --------------------
    def start_process(self, args=''):
        services.logger.info('start_process')
        self.gui_process = CmdRunner()
        self.gui_process.start_task_bg('gui', f'python ver/gui/main.py {args}', working_dir='.')
        # TODO get coverage to work on background gui
        # self.gui_process.start_task_bg('gui',
        #                                f'coverage run --append --rcfile=setup.cfg ver/gui/main.py {args}',
        #                                working_dir='.')
        # show it off for a bit
        time.sleep(1)

    # --------------------
    def kill_process(self):
        services.logger.info('kill_process')
        self.gui_process.finish()

    # --------------------
    @property
    def label1_text(self):
        item = services.th.search(self.label1_path)
        return item['value']

    # --------------------
    def click_button1(self):
        services.th.click_left(self.button1_path)

    # --------------------
    def click_clear_menuitem(self):
        services.th.menu_click(self.menu_clear_path)
