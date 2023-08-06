import sys
import unittest

from pytest_ver import pth

sys.path.append('.')

from ver.helpers import services
from ver.helpers.helper import Helper
from ver.helpers.logger_mock import Logger
from gui_api_tkinter.lib.harness.gui_api_harness import GuiApiHarness  # noqa: E402


# -------------------
class TestTp002(unittest.TestCase):
    page1 = None
    logger = None
    helper = None
    th = None

    # --------------------
    @classmethod
    def setUpClass(cls):
        pth.init()

        services.th = GuiApiHarness()
        services.th.init()
        services.logger = Logger()
        services.helper = Helper()

    # -------------------
    def setUp(self):
        print('')

    # -------------------
    def tearDown(self):
        services.helper.kill_process()
        self.assertFalse(services.helper.gui_process.is_alive())

        # uncomment for debugging
        # print(f'DBG {services.logger.lines}')

    # --------------------
    @classmethod
    def tearDownClass(cls):
        services.th.term()
        pth.term()

    # --------------------
    # @pytest.mark.skip(reason='skip')
    def test_tp002(self):
        pth.proto.protocol('tp-002', 'no callback defined, check for nak')

        pth.proto.step('start gui')
        # don't define callback
        services.helper.start_process('--no-callback --logger stdout')
        pth.ver.verify_true(services.helper.gui_process.is_alive())
        pth.ver.verify_false(services.th.is_connected(), reqids='SRS-009')

        pth.proto.step('connect harness to GUI App server')
        services.th.connect()
        pth.ver.verify_true(services.th.is_connected(), reqids=['SRS-001', 'SRS-009'])

        pth.proto.step('send invalid "cmd02" command')
        cmd = {
            'cmd': 'cmd02',
            'param1': 'some parameter1',
            'param2': 'some parameter2',
        }
        rsp = services.th.send_recv(cmd)
        pth.ver.verify_equal(rsp['value'], 'nak', reqids='SRS-005')
        pth.ver.verify_equal(rsp['reason'], 'unknown command', reqids='SRS-005')

        pth.proto.step('disconnect from GUI API server')
        services.th.term()
        pth.ver.verify_false(services.th.is_connected(), reqids='SRS-003')
