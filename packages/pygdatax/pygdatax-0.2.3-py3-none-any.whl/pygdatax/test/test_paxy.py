import unittest
unittest.TestLoader.sortTestMethodsUsing = None
from pygdatax import cansas
from pygdatax.instruments import sans
import nexusformat.nexus as nx

import os


class TestPaxyTreatment(unittest.TestCase):

    def setUp(self) -> None:
        self.directory = os.path.abspath('../../../example_data/PAXY')
        fileList = os.listdir(self.directory)
        self.file32List = []
        for file in fileList:
            if file.endswith('.32'):
                self.file32List.append(file)
        self.standards = dict()
        self.standards['FD'] = ['XY3200', 'XY3208', 'XY3216', 'XY3226']
        self.standards['B4C'] = [['XY3206', 'XY3200'], ['XY3214', 'XY3208'], ['XY3223', 'XY3216'], ['XY3233', 'XY3226']]
        self.standards['EC'] = [['XY3207', 'XY3203'], ['XY3215', 'XY3211'], ['XY3224', 'XY3219'], ['XY3234', 'XY3229']]
        self.standards['H2O'] = [[None, None], [None, None], ['XY3225', 'XY3220'], ['XY3235', 'XY3230']]
        self.sample = dict()
        self.sample['NE_PS30k_HG'] = [['XY3204', 'XY3201'],
                                      ['XY3212', 'XY3209'],
                                      ['XY3221', 'XY3217'],
                                      ['XY3231', 'XY3227']]
        self.mask_file = ['mask_TPQ.edf', 'mask_PQ.edf', 'mask_MQ.edf', 'mask_GQ.edf']
        self.norm_file = ['norm_TPQ.nxs', 'norm_PQ.nxs', 'norm_MQ.nxs', 'norm_GQ.nxs']
        self.sub_file = ['sous_TPQ.nxs', 'sous_PQ.nxs', 'sous_MQ.nxs', 'sous_GQ.nxs']

    def test_a_paxy2nxsas(self):
        for file in os.listdir(self.directory):
            if file.endswith('.nxs'):
                os.remove(os.path.join(self.directory, file))
        for key in self.sample:
            for i in range(len(self.sample[key])):
                scatt = self.sample[key][i][0] + '.32'
                trans = self.sample[key][i][1] + '.32'
                cansas.paxy2nxsas(os.path.join(self.directory, scatt))
                cansas.paxy2nxsas(os.path.join(self.directory, trans))
        for key in self.standards:
            for files in self.standards[key]:
                if type(files) == list:
                    for f in files:
                        if f is not None:
                            cansas.paxy2nxsas(os.path.join(self.directory, f + '.32'))
                else:
                    if files is not None:
                        cansas.paxy2nxsas(os.path.join(self.directory, files + '.32'))



    def test_b_transmission(self):
        for key in self.standards:
            if key != 'FD':
                for i in range(len(self.standards[key])):
                    scatt = self.standards[key][i][0]
                    trans = self.standards[key][i][1]

                    if scatt and trans:
                        scatt_file_path = os.path.join(self.directory, scatt + '.nxs')
                        trans_file_path = os.path.join(self.directory, self.standards[key][i][1] + '.nxs')
                        fd_file = os.path.join(self.directory, self.standards['FD'][i] + '.nxs')
                        sans.set_transmission(scatt_file_path, trans_file=trans_file_path,
                                              direct_beam_file=fd_file,
                                              roi=[59, 59, 69, 69])
                        x0, y0 = sans.find_direct_beam(fd_file, roi=[59, 59, 69, 69])
                        sans.set_beam_center(scatt_file_path, x0=x0, y0=y0, detector_number=0)

        for key in self.sample:
            for i in range(len(self.sample[key])):
                scatt = self.sample[key][i][0]
                trans = self.sample[key][i][1]
                fd = self.standards['FD'][i]
                scatt_file_path = os.path.join(self.directory, scatt + '.nxs')
                trans_file_path = os.path.join(self.directory, trans + '.nxs')
                fd_file = os.path.join(self.directory, fd + '.nxs')
                x0, y0 = sans.find_direct_beam(fd_file, roi=[59, 59, 69, 69])
                sans.set_beam_center(scatt_file_path, x0=x0, y0=y0, detector_number=0)
                sans.set_transmission(scatt_file_path, trans_file=trans_file_path,
                                      direct_beam_file=fd_file,
                                      roi=[59, 59, 69, 69])

    def test_c_make_sub_package(self):

        package_name = self.sub_file
        for i in range(4):
            dark = os.path.join(self.directory, self.standards['B4C'][i][0]+'.nxs')
            ec = os.path.join(self.directory, self.standards['EC'][i][0]+'.nxs')
            root_ec = nx.nxload(ec, mode='r')
            x0 = root_ec.entry0.instrument.detector0.beam_center_x.nxdata
            y0 = root_ec.entry0.instrument.detector0.beam_center_y.nxdata
            if self.mask_file[i]:
                mask_path = os.path.join(self.directory, self.mask_file[i])
            else:
                mask_path = None
            sans.make_reduction_package(os.path.join(self.directory, package_name[i]),
                                        dark_file=dark,
                                        empty_beam_file=None,
                                        empty_cell_file=ec,
                                        x0=x0,
                                        y0=y0,
                                        mask_files=mask_path
                                        )

    def test_d_make_norm_package(self):
        # mask_list = [None, None, None, os.path.join(self.directory, 'mask_GQ.edf')]
        package_name = self.norm_file
        for i in range(4):
            dark = os.path.join(self.directory, self.standards['B4C'][i][0] + '.nxs')
            ec = os.path.join(self.directory, self.standards['EC'][i][0] + '.nxs')
            if self.standards['H2O'][i][0]:
                h2o = os.path.join(self.directory, self.standards['H2O'][i][0] + '.nxs')
                root_ec = nx.nxload(ec, mode='r')
                x0 = root_ec.entry0.instrument.detector0.beam_center_x.nxdata
                y0 = root_ec.entry0.instrument.detector0.beam_center_y.nxdata
                if self.mask_file[i]:
                    mask_path = os.path.join(self.directory, self.mask_file[i])
                else:
                    mask_path = None
                sans.make_reduction_package(os.path.join(self.directory, package_name[i]),
                                            dark_file=dark,
                                            empty_beam_file=None,
                                            empty_cell_file=ec,
                                            water_file=h2o,
                                            x0=x0,
                                            y0=y0,
                                            mask_files=mask_path
                                            )

    def test_e_reduction2D(self):
        for key in self.sample:
            for i in range(len(self.sample[key])):
                norm_file = [os.path.join(self.directory, i) for i in self.norm_file]
                sub_file = os.path.join(self.directory, self.sub_file[i])
                scat_file = os.path.join(self.directory, self.sample[key][i][0] + '.nxs')
                if os.path.exists(str(norm_file)):
                    sans.reduction2D(scat_file, sub_file=sub_file, norm_file=norm_file)
                else:
                    sans.reduction2D(scat_file, sub_file=sub_file, norm_file=os.path.join(self.directory, 'norm_MQ.nxs'))
        # set center and transmission
        # sans.set_transmission(scat_file, trans_file=trans_file,
        #                       direct_beam_file=fd_file,
        #                       roi=[59, 59, 69, 69])
        # x0, y0 = sans.find_direct_beam(fd_file, roi=[59, 59, 69, 69])
        # sans.set_beam_center(scat_file, x0=x0, y0=y0, detector_number=0)

    def test_f_azimutal(self):
        for key in self.sample:
            for i in range(len(self.sample[key])):
                scat_file = os.path.join(self.directory, self.sample[key][i][0] + '.nxs')
                sans.azimutal_integration(scat_file)

    def test_g_normalization_factor(self):
        norm_factor = [300, 20 , 1 , 0.8]
        for key in self.sample:
            for i in range(len(self.sample[key])):
                sans.normalization_factor(os.path.join(self.directory, self.sample[key][i][0]+'.nxs'),
                                          factor=norm_factor[i])

    def test_h_cuts(self):
        xmin = [0.002, 0.015, 0.03, 0.1]
        xmax = [0.017, 0.04, 0.08 , 0.4]
        for key in self.sample:
            for i in range(len(self.sample[key])):
                scat_file = os.path.join(self.directory, self.sample[key][i][0] + '.nxs')
                sans.cut(scat_file,xmin=xmin[i], xmax=xmax[i], detector_number=0)


    def test_i_concat(self):
        for key in self.sample:
            fileList = []
            for i in range(len(self.sample[key])):
                scat_file = os.path.join(self.directory, self.sample[key][i][0] + '.nxs')
                fileList.append(scat_file)
            output_file = os.path.join(self.directory, key + '_concat.nxs')
            sans.concat(output_file, *fileList)

if __name__ == '__main__':
    unittest.TestLoader.sortTestMethodsUsing = None
    # suite = unittest.TestSuite()
    # unittest.runner.TextTestRunner.run(TestPaxyTreatment.test_paxy2nxsas)
    # suite.addTest(TestPaxyTreatment('test_paxy2nxsas'))
    # suite.addTest(TestPaxyTreatment('test_transmission'))
    # suite.addTest(TestPaxyTreatment('test_make_reduction_package'))
    # suite.addTest(TestPaxyTreatment('test_reduction2D'))
    # runner = unittest.TextTestRunner(failfast=True)
    # runner.run(suite())
    unittest.main()
