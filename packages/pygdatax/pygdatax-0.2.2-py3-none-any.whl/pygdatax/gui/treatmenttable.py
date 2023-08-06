from silx.gui import qt
from silx.gui.widgets.TableWidget import TableWidget, TableView
import os
from pygdatax.gui import FileBrowserWidget, DirectoryBrowserWidget, DataView
from pygdatax.instruments.sans import make_reduction_package, treat_normalization_package


class SpectraTable(TableWidget):
    show_data_clicked = qt.pyqtSignal(str)

    def __init__(self, parent=None, extenstion='.nxs'):
        super(SpectraTable, self).__init__(parent=parent, cut=True, paste=True)
        self.directory = None
        self.extension = extenstion
        self.setRowCount(3)
        self.setColumnCount(3)
        action = qt.QAction(self)
        action.setText('show data')
        action.triggered.connect(self.show_data)
        self.addAction(action)
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(['scatt', 'trans', 'trans_empty', 'tr value'])
        # self.setHorizontalHeaderLabels(['scatt', 'trans', 'tr value'])
        # self.setVerticalHeaderLabels(['empty beam', 'Cd/B4C', 'empty cell'])

    def set_directory(self, path):
        if os.path.exists(path) and os.path.isdir(path):
            self.directory = path

    def set_extension(self, ext):
        if '.' == ext[0]:
            self.extension = ext

    def show_data(self):
        if self.directory:
            if self._text_last_cell_clicked:
                self.show_data_clicked.emit(os.path.join(self.directory, self._text_last_cell_clicked))


class NormalizationTable(SpectraTable):

    def __init__(self, parent=None):
        super(NormalizationTable, self).__init__(parent=parent)
        self.setRowCount(4)
        self.setVerticalHeaderLabels(['water', 'Cd/B4C', 'empty cell' , 'empty beam'])

    # TODO: finish this function in order to feed the makerductionpackage fucntion
    def get_files(self):
        for i in range(self.rowCount()):
            for j in self.columnCount():
                pass


    # TODO: code the set_transmission function of the normalization table
    def set_transmission(self, trList):
        pass



class SubstractionTable(SpectraTable):

    def __init__(self, parent=None):
        super(SubstractionTable, self).__init__(parent=parent)
        self.setRowCount(3)
        self.setVerticalHeaderLabels(['empty beam', 'Cd/B4C', 'empty cell'])


class SampleTable(SpectraTable):

    def __init__(self):
        super(SampleTable, self).__init__()
        self.setRowCount(1)
        # self.setColumnCount()

# TODO: finish this
class ReductionParametersWidget(qt.QWidget):
    """
    Tab widget allowing to store reduction parameters such as the beam center, the mask file and the binning.
    The nummber of tabs corresponds to the number of detector
    """

    def __init__(self, parent=None):
        super(ReductionParametersWidget, self).__init__(parent=parent)
        self.x0LineEdit = qt.QLineEdit(parent=self)
        self.x0LineEdit.setValidator(qt.QDoubleValidator())
        self.y0LineEdit = qt.QLineEdit(parent=self)
        self.y0LineEdit.setValidator(qt.QDoubleValidator())
        # self.binsLineEdit = qt.QLineEdit(parent=self)
        # self.binsLineEdit.setValidator(qt.QIntValidator())
        self.maskLineEdit = FileBrowserWidget(label='mask file:', directory="", extensions="All files (*.*)", parent=self)
        layout = qt.QFormLayout()
        layout.addRow('x0 (pixels) : ', self.x0LineEdit)
        layout.addRow('y0 (pixels) :', self.y0LineEdit)
        # layout.addRow('bins :', self.binsLineEdit)
        vlayout = qt.QVBoxLayout()
        vlayout.addLayout(layout)
        vlayout.addWidget(self.maskLineEdit)
        self.setLayout(vlayout)

    def get_parameters(self):
        """
        Return a dictinnonary with reduction parameters (beam center, binning, mask file)
        :return:
        """
        d = {}
        x0 = self.x0LineEdit.text()
        if x0 != '':
            d['x0'] = float(x0)
        else:
            d['x0'] = None

        y0 = self.y0LineEdit.text()
        if y0 != '':
            d['y0'] = float(x0)
        else:
            d['y0'] = None

        # bins = self.binsLineEdit.text()
        # if bins != '':
        #     d['bins'] = float(x0)
        # else:
        #     d['bins'] = None
        mask_file = self.maskLineEdit.get_file()
        if os.path.exists(mask_file):
            d['mask_file'] = mask_file
        else:
            d['mask_file'] = None
        return d


class ReductionParametersTabWidget(qt.QTabWidget):
    
    def __init__(self, nDet=1, parent=None):
        super(ReductionParametersTabWidget, self).__init__(parent=parent)
        for i in range(nDet):
            self.addTab(ReductionParametersWidget(parent=self), 'detector' + str(i))

    def get_parameters(self):
        d_all = {}
        nDet = self.count()
        d_all['x0'] = []
        d_all['y0'] = []
        d_all['mask_files'] = []
        for i in range(nDet):
            widget = self.widget(i)
            d = widget.get_parameters()
            d_all['x0'].append(d['x0'])
            d_all['y0'].append(d['y0'])
            d_all['mask_files'].append(d['mask_file'])
        print(d_all)
        return d_all


class ReductionPackageWidget(qt.QWidget):

    def __init__(self, parent=None, nDet=1, directory=None):
        super(ReductionPackageWidget, self).__init__(parent=parent)
        self.parameterTabWidget = ReductionParametersTabWidget(nDet=nDet)
        self.table = NormalizationTable(parent=self)
        self.directoryBrowser = DirectoryBrowserWidget(label='data directory:', parent=self)
        # self.directoryButton = qt.QPushButton(parent=self)
        # self.directoryButton.setIcon(getQIcon('directory.ico'))
        self.packageFileLineEdit = qt.QLineEdit(parent=self)
        self.saveButton = qt.QPushButton('Save', parent=self)
        self.quitButton = qt.QPushButton('Quit', parent=self)
        # layout
        layout = qt.QVBoxLayout()
        layout.addWidget(self.directoryBrowser)
        layout.addWidget(self.parameterTabWidget)
        layout.addWidget(self.table)
        # filename of the package to be saved
        hlayout0 = qt.QHBoxLayout()
        hlayout0.addWidget(qt.QLabel('Package file:'))
        hlayout0.addWidget(self.packageFileLineEdit)
        layout.addLayout(hlayout0)
        # buttons
        hlayout = qt.QHBoxLayout()
        hlayout.addWidget(self.saveButton)
        hlayout.addWidget(self.quitButton)
        layout.addLayout(hlayout)
        self.setLayout(layout)

        # connect signals
        self.quitButton.clicked.connect(self.on_quit)
        self.saveButton.clicked.connect(self.on_save)
        self.directoryBrowser.directoryChanged.connect(self.on_directoryChanged)
        self.table.show_data_clicked.connect(self.on_showData)
        # init directory
        if directory and os.path.isdir(directory):
            self.directoryBrowser.set_directory(directory)

    def on_directoryChanged(self, path):
        self.table.set_directory(path)

    def on_showData(self, filepath):
        # we don't use it for the moment because the default viewer could be use to plot raw data
        pass

    def on_save(self):
        directory = self.directoryBrowser.get_directory()
        fname = self.packageFileLineEdit.text()
        param_dict = self.parameterTabWidget.get_parameters()
        print(param_dict)
        # TODO finish this

    def on_quit(self):
        self.close()


if __name__ == '__main__':
    import sys

    app = qt.QApplication([])
    folder = "/home/achennev/python/pygdatax/example_data/PAXY"
    w = ReductionPackageWidget(nDet=0, directory=folder)
    w.show()
    result = app.exec_()
    app.deleteLater()
    sys.exit(result)
