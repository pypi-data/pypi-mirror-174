import weakref
import pytest
from silx.gui.utils.testutils import TestCaseQt
from ..gui_xeuss import XeussMainWindow

class TestGuiXeuss(TestCaseQt):

    def testConstruct(self):
        widget = Viewer()
        self.qWaitForWindowExposed(widget)

    def testDestroy(self):
        widget = Viewer()
        ref = weakref.ref(widget)
        widget = None
        self.qWaitForDestroy(ref)

