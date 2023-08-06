import unittest
from pygdatax.instruments import sans
import nexusformat.nexus as nx


class TestDetectorNumber(unittest.TestCase):

    def test_xeuss(self):
        file = '/home/achennev/Documents/xeuss/2020-12-30-AC_flux/2020-12-30-AC_flux_0_67489.nxs'
        root = nx.nxload(file)
        self.assertEqual(sans.get_detector_number(root), 1)
        dic = sans.get_default_reduction_parameters(root)
        print('\n XEUSS default paramerters')
        print(dic)

    def test_sansone(self):
        file = '/home/achennev/Documents/PA20-PSI/example_data_files_from_SANS-1/sans2020n026648.nxs'
        root = nx.nxload(file)
        self.assertEqual(sans.get_detector_number(root), 1)
        dic = sans.get_default_reduction_parameters(root)
        print('\n SANSONE default paramerters')
        print(dic)

    def test_sansllb(self):
        pass
    #     # sansLLB
    #     file = '/home/achennev/Documents/PA20-PSI/sans-llb_markV2.hdf'
    #     root = nx.nxload(file)
    #     self.assertEqual(sans.get_detector_number(root), 3)
        # # xeuss



if __name__ == '__main__':
    unittest.main()
