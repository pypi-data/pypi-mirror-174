import sys

import os
import collections
import logging
import functools

import h5py
import silx.io.nxdata
from silx.gui import qt
from silx.gui import icons
import silx.gui.hdf5
from silx.app.view.ApplicationContext import ApplicationContext
from silx.app.view.CustomNxdataWidget import CustomNxdataWidget
from silx.app.view.CustomNxdataWidget import CustomNxDataToolBar
from silx.app.view import utils
from silx.gui.utils import projecturl
from silx.app.view.DataPanel import DataPanel
from silx.gui.data.DataViews import DataView, _normalizeData, _normalizeComplex


_logger = logging.getLogger(__name__)

# DataViewer modes
EMPTY_MODE = 0
PLOT1D_MODE = 10
RECORD_PLOT_MODE = 15
IMAGE_MODE = 20
PLOT2D_MODE = 21
COMPLEX_IMAGE_MODE = 22
PLOT3D_MODE = 30
RAW_MODE = 40
RAW_ARRAY_MODE = 41
RAW_RECORD_MODE = 42
RAW_SCALAR_MODE = 43
RAW_HEXA_MODE = 44
STACK_MODE = 50
HDF5_MODE = 60
NXDATA_MODE = 70
NXDATA_INVALID_MODE = 71
NXDATA_SCALAR_MODE = 72
NXDATA_CURVE_MODE = 73
NXDATA_XYVSCATTER_MODE = 74
NXDATA_IMAGE_MODE = 75
NXDATA_STACK_MODE = 76
NXDATA_VOLUME_MODE = 77
NXDATA_VOLUME_AS_STACK_MODE = 78

class PlotView(DataView):
    """View displaying data using a 1d plot"""

    def __init__(self, parent):
        super(PlotView, self).__init__(
            parent=parent,
            modeId=PLOT1D_MODE,
            label="Curve",
            icon=icons.getQIcon("view-1d"))
        self.__resetZoomNextTime = True

    def createWidget(self, parent):
        from silx.gui import plot
        return plot.Plot1D(parent=parent)

    def clear(self):
        self.getWidget().clear()
        self.__resetZoomNextTime = True

    def normalizeData(self, data):
        data = DataView.normalizeData(self, data)
        data = _normalizeComplex(data)
        return data

    def setData(self, data):
        data = self.normalizeData(data)
        plotWidget = self.getWidget()
        nxd = get_default(data)
        legend = os.path.split(data.file.filename)[1] + data.name
        plotWidget.addCurve(legend=legend,
                            x=nxd.axes[0],
                            y=nxd.signal,
                            resetzoom=self.__resetZoomNextTime)
        plotWidget.setActiveCurve(legend)
        self.__resetZoomNextTime = True

    def setDataSelection(self, selection):
        self.getWidget().setGraphTitle(self.titleForSelection(selection))

    def axesNames(self, data, info):
        return ["y"]

    def getDataPriority(self, data, info):
        if info.size <= 0:
            return DataView.UNSUPPORTED
        if data is None or not info.isArray or not info.isNumeric:
            return DataView.UNSUPPORTED
        if info.dim < 1:
            return DataView.UNSUPPORTED
        if info.interpretation == "spectrum":
            return 1000
        if info.dim == 2 and info.shape[0] == 1:
            return 210
        if info.dim == 1:
            return 100
        else:
            return 10

if __name__ == '__main__':
    import numpy as np
    import nexusformat.nexus as nx
    from silx.io.nxdata import is_valid_nxdata, get_default
    from silx.gui.data import DataViews
    from silx.gui.plot import Plot1D
    app = qt.QApplication([])
    from silx.gui.data import DataViewer
    # dp = DataViewer.DataViewer()
    x = np.linspace(0,1,100)
    y = 2*x
    # # dp.setData(x)
    # # dp.setData(y)
    #
    #
    file1 = '/home/achennev/Documents/collab lay theng/2020-02-18-LT/SiP2_pos1.nxs'
    file2 = '/home/achennev/Documents/collab lay theng/2020-02-18-LT/SiP2_pos2.nxs'
    # for file in [file1, file2]:
    #     with h5py.File(file, mode='r') as root:
    #         data = root['reflectivity/data']
    #         # print(data)
    #         print(get_default(root))
    #         print(is_valid_nxdata(data))
    #         dp.setData(get_default(root))
    # dp.show()
    dv = PlotView(None)
    for file in [file1, file2]:
        with h5py.File(file, mode='r') as root:
            data = root['reflectivity/data']
            dv.setData(data)
            # dv.setData(data['Q'])
    dv.getWidget().show()

    result = app.exec_()
    app.deleteLater()
    sys.exit(result)
