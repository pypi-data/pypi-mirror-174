from fabio.app.convert import get_output_filename

from pygdatax import flib
from pygdatax import nxlib
import numpy as np
import os
import fabio
import nexusformat.nexus as nx
from typing import Union


def get_default_reduction_parameters(root):
    """
    Return the default parameters for azimutal integration stored within the NXroot object for the three detectors.
    These parameters are the beam center position and the default number of bins for each detector.
    The default bin nubre if defined as the diagonal length for the central detector and the number of tubes for the
    wide angle detectors.

    :param root:
    :type root: NXroot
    :return: parameters dictionnary e.g. {'x0':[x0_0, ..., x0_n],'y0':[y0_0, ..., y0_n],
        'bins':[bins_0, ..., bins_n]} n is the number of detectors
    :rtype: dict
    """
    x0 = []
    y0 = []
    bins = []
    entry = root[nxlib.get_last_entry_key(root)]
    for i in range(nxlib.get_detector_number(root)):
        x = entry.instrument['detector' + str(i) + '/beam_center_x'].nxdata
        y = entry.instrument['detector' + str(i) + '/beam_center_y'].nxdata
        xDim = entry.instrument['detector' + str(i) + '/data'].shape[1]
        yDim = entry.instrument['detector' + str(i) + '/data'].shape[0]
        bins.append(flib.get_default_bins(x, y, xDim, yDim))
        x0.append(x)
        y0.append(y)
    dic = {'x0': x0,
           'y0': y0,
           'bins': bins
           }
    return dic


def find_direct_beam(file: str, roi: list =None):
    """
    Find direct beam on central detector (detector0) on a given region of interest

    :param file: transmission file
    :type file: str
    :param roi: region of interest allowing to search direct beam [x1,Y1, X2, Y2] (bottom left and top right corners), default to None (full detector)
    :type roi: list, optional
    :return: coordinate of beam center (center of mass) [x0, y0]
    :rtype: [float, float]
    """
    root = nx.nxload(file)
    data = root.entry0.instrument.detector0.data.nxdata
    x0, y0 = flib.find_direct_beam(data, corners=roi)
    root.close()
    return [x0, y0]


@nxlib.treatment_function(new_entry=False)
def set_beam_center(root: nx.NXroot, x0: float = None, y0: float = None, detector_number: int = 0) -> None:
    """
    set the beam center of a given detector identified by its number.

    :param root: NXroot
    :type root: NXroot
    :param x0: horizontal beam center position (in pixels)
    :type x0 : float
    :param y0: vertical beam center position (in pixel)
    :type y0: float
    :param detector_number: detector identifier
    :type detector_number int
    :return: None
    """
    if x0:
        root.entry0.instrument['detector'+str(detector_number)].beam_center_x = x0
    if y0:
        root.entry0.instrument['detector' + str(detector_number)].beam_center_y = y0
    return


@nxlib.treatment_function(new_entry=False)
def set_transmission(root: nx.NXroot, trans_file: str = None, direct_beam_file: str = None,
                     roi: list = [None, None, None, None]) -> None:
    """
    Compute sample trasnmission and store it in the sample.transmission field. The computation is done over the roi.
    By default this roi is 20x20 pixel centered over the center given by the scattering file in detector0 field
    :param root: NXroot of the data file
    :type root: NXroot
    :param trans_file: nexus file for sample transmission
    :type trans_file: str
    :param direct_beam_file: direct beam nexus file corresponding
    :type direct_beam_file: str
    :param roi: Region of interest on central detector allow to compute transmission [X1,Y1, X2,Y2]
    :type roi: list
    :return:
    """


    # """
    #     compute sample trasnmission and store it in the sample.transmission field. The computation is done over the roi.
    #     By default this roi is 20x20 pixel centered over the center given by the scattering file in detector0 field
    #     Args:
    #         root: NXroot of the scattering file
    #         trans_file (str): transmited filepath
    #         direct_beam_file (str): direct beaml filepath
    #         roi (list): roi extent [X1,Y1, X2,Y2] on which is computed the transmission
    #
    #     Returns:
    #
    #     """
    entry = root.entry0
    if roi == 4 * [None]:
        x0 = entry['instrument/detector0/beam_center_x'].nxdata
        y0 = entry['instrument/detector0/beam_center_y'].nxdata
        roi = [int(x0 - 10), int(y0 - 10), int(x0 + 10), int(y0 + 10)]

    if trans_file is not None and direct_beam_file is not None:
        if os.path.exists(trans_file) and os.path.exists(direct_beam_file):
            direct_root = nx.nxload(direct_beam_file, mode='r')
            trans_root = nx.nxload(trans_file, mode='r')
            crop_direct = direct_root['entry0/instrument/detector0/data'].nxdata[roi[1]:roi[3], roi[0]:roi[2]]
            crop_direct = crop_direct.sum()
            crop_trans = trans_root['entry0/instrument/detector0/data'].nxdata[roi[1]:roi[3], roi[0]:roi[2]]
            crop_trans = crop_trans.sum()
            monitor_trans = trans_root['entry0/monitor/integral'].nxdata
            monitor_direct = direct_root['entry0/monitor/integral'].nxdata
            t = crop_trans / crop_direct * monitor_direct / monitor_trans

            entry['sample/transmission'] = t
        else:
            return
    else:
        print('No transmission file or direct beam file povided')
        return


@nxlib.treatment_function(output_file=True)
def make_reduction_package(output_file: str,
                           dark_file: str = None, empty_cell_file: str = None, empty_beam_file: str = None,
                           water_file: str = None,
                           mask_files: Union[str, list]= None,
                           x0: Union[float, list] = None,
                           y0: Union[float, list] = None
                           ):
    """

    :param output_file: nexus file output for the reduction package
    :type output_file: str
    :param dark_file: dark nexus file path
    :type dark_file: str
    :param empty_cell_file: empty cell nexus file path
    :type empty_cell_file: str
    :param empty_beam_file: empty beam nexus file path
    :type empty_beam_file: str
    :param water_file: water nexus file for normalization package
    :type water_file: str
    :param mask_files: mask file path or list of mask file for each deteector [mask_0, mask_1, ...]
    :type mask_files: Union[float, list]
    :param x0: beam center in pixel or list of beam centers for each detector [x0_0, X0_1, ...].
    :param y0:
    """
    # put parameter as a list
    if type(x0) != list:
        x0 = [x0]
    if type(y0) != list:
        y0 = [y0]
    if type(mask_files) != list:
        mask_files = [mask_files]

    root = nx.NXroot()
    root.save(output_file, mode='w')
    nDet = 0
    if dark_file is not None:
        dark_root = nx.nxload(dark_file, mode='r')
        nDet = nxlib.get_detector_number(dark_root)
        nxlib.copy_entry(root, dark_root, 'dark', 'entry0')
        dark_root.close()
        def_params = get_default_reduction_parameters(dark_root)

    if empty_cell_file is not None:
        ec_root = nx.nxload(empty_cell_file, mode='r')
        nDet = nxlib.get_detector_number(ec_root)
        nxlib.copy_entry(root, ec_root, 'empty cell', 'entry0')
        ec_root.close()
        def_params = get_default_reduction_parameters(ec_root)

    if empty_beam_file is not None:
        db_root = nx.nxload(empty_beam_file, mode='r')
        nDet = nxlib.get_detector_number(db_root)
        nxlib.copy_entry(root, dark_root, 'empty beam', 'entry0')
        db_root.close()
        def_params = get_default_reduction_parameters(db_root)

    if water_file is not None:
        water_root = nx.nxload(water_file, mode='r')
        nDet = nxlib.get_detector_number(water_root)
        nxlib.copy_entry(root, water_root, 'water', 'entry0')
        water_root.close()
        def_params = get_default_reduction_parameters(water_root)

    params_entry = nx.NXgroup()
    root.insert(params_entry, name='parameters')
    # check that lists have the same length
    if not all(len(i) == nDet for i in [x0, y0, mask_files]):
        raise ValueError('not all list have the same length as the number of detector')

    for i in range(nDet):
        detector = nx.NXgroup()
        params_entry.insert(detector, name='detector'+str(i))
        if mask_files[i] is not None:
            mask_data = fabio.open(mask_files[i]).data
        else:
            mask_data = None
        detector.insert(nx.NXfield(mask_data), name='mask')

        if x0[i] is None:
            detector.insert(nx.NXfield(def_params['x0'][i]), name='beam_center_x')
        else:
            detector.insert(nx.NXfield(x0[i]), name='beam_center_x')
        if y0[i] is None:
            detector.insert(nx.NXfield(def_params['y0'][i]), name='beam_center_y')
        else:
            detector.insert(nx.NXfield(y0[i]), name='beam_center_y')
    root.close()


# TODO : compute resolution
@nxlib.treatment_function(new_entry=True)
def reduction2D(root: nx.NXroot, sub_file: str = None, norm_file: str = None,
                thickness: float = None, transmission: float = None, distance: list = None) -> object:
    # """
    # Subtract and normalize the sans 2D spectra according to Brûlet, A., Lairez, D., Lapp, A., & Cotton, J. P. (2007). Improvement of data treatment in small-angle neutron scattering. Journal of Applied Crystallography, 40(1), 165-177.
    # The resulting spectra is a 2D spectra
    # Args:
    #     root:
    #     sub_file (str): substraction package file
    #     norm_file (str): normalization package file
    #     thickness (float): sample thickness
    #     transmission (float): sample transmisssion
    #     distance (list): list of detector distances
    #
    # Returns:
    #
    # """
    entry = root[nxlib.get_last_entry_key(root)]
    nDet = nxlib.get_detector_number(root)
    if type(distance) != list:
        distance = [distance]
    if len(distance) != nDet:
        raise ValueError('Distances should have the same lenght as the number of detector (%i here))' % nDet)

    def delta(u, a):
        if u == 1:
            v = 1
        else:
            v = (1 - x ** a) / (-a * np.log(x))
        return v

    def tr_theta(t, angle):
        if t == 1:
            t_th = 1
        else:
            t_th = t * (t ** (1 - 1 / np.cos(angle)) - 1) / (np.log(t) * (1 - 1 / np.cos(angle)))
        return t_th

    if transmission is None:
        transmission = entry.sample.transmission.nxdata
        # if transmission == 0:
        #     entry.sample.transmission = 1.0
    else:
        entry.sample.transmission = transmission
    if thickness is None:
        thickness = entry.sample.thickness.nxdata
    else:
        entry.sample.thickness = thickness

    for i in range(nxlib.get_detector_number(root)):
        distance_key = 'instrument/detector' + str(i) + '/distance'
        if distance[i] is None:
            distance[i] = entry[distance_key].nxdata
        else:
            entry[distance_key].nxdata = distance[i]

        i_sample = root['entry0/data'+str(i)]
        i_sample.nxerrors = nx.NXfield(np.sqrt(np.abs(i_sample.data.nxdata)))
        monitor_sample = root['entry0/monitor/integral'].nxdata
        time_sample = root['entry0/monitor/count_time'].nxdata
        shape = i_sample.nxsignal.nxdata.shape

        # uncack the substraction package file
        default_params = get_default_reduction_parameters(root)
        if sub_file is not None:
            sub_root = nx.nxload(sub_file, mode='rw')
            if 'dark' in sub_root:
                i_dark = sub_root['dark/data'+str(i)]
                # i_dark.nxerrors = np.zeros(shape)
                i_dark.nxerrors = nx.NXfield(np.sqrt(np.abs(i_dark.data.nxdata)))
                # monitor_dark = sub_root['dark/monitor3/integral'].nxdata
                time_dark = sub_root['dark/monitor/count_time'].nxdata
            else:
                i_dark = nx.NXdata(nx.NXfield(np.zeros(shape), name='i_dark'))
                i_dark.nxerrors = np.zeros(shape)
                # monitor_dark = 1
                time_dark = 1
            if 'empty cell' in sub_root:
                i_ec = sub_root['empty cell/data'+str(i)]
                i_ec.nxerrors = nx.NXfield(np.sqrt(np.abs(i_ec.nxsignal.nxdata)))
                monitor_ec = sub_root['empty cell/monitor/integral'].nxdata
                time_ec = sub_root['empty cell/monitor/count_time'].nxdata
                trans_ec = sub_root['empty cell/sample/transmission'].nxdata
            else:
                i_ec = nx.NXdata(nx.NXfield(np.zeros(shape), name='i_ec'))
                i_ec.nxerrors = np.zeros(shape)
                monitor_ec = 1
                time_ec = 1
                trans_ec = 1
            if 'empty beam' in sub_root:
                i_eb = sub_root['empty beam/data'+str(i)]
                i_eb.nxerrors = nx.NXfield(np.sqrt(np.abs(i_eb.data.nxdata)))
                monitor_eb = sub_root['empty beam/monitor/integral'].nxdata
                time_eb = sub_root['empty beam/instrument/monitor/count_time'].nxdata
            else:
                i_eb = nx.NXdata(nx.NXfield(np.zeros(shape), name='i_eb'))
                i_eb.nxerrors = np.zeros(shape)
                monitor_eb = 1
                time_eb = 1

            # centers for regroupement
            if 'beam_center_x' in sub_root['parameters/detector'+str(i)]:
                x0 = sub_root['parameters/detector'+str(i)+'/beam_center_x'].nxdata
                entry['instrument/detector'+str(i)+'/beam_center_x'] = x0
            else:
                x0 = default_params['x0']
            if 'beam_center_y' in sub_root['parameters/detector'+str(i)]:
                y0 = sub_root['parameters/detector'+str(i)+'/beam_center_y'].nxdata
                entry['instrument/detector' + str(i) + '/beam_center_y'] = y0
            else:
                y0 = default_params['y0']
            # mask
            if 'mask' in sub_root['parameters/detector'+str(i)]:
                sub_mask = sub_root['parameters/detector'+str(i)+'/mask'].nxdata
            else:
                sub_mask = np.zeros(shape)
        else:
            i_dark = nx.NXdata(nx.NXfield(np.zeros(shape), name='i_dark'))
            i_dark.nxerrors = np.zeros(shape)
            # monitor_dark = 1
            time_dark = 1
            i_ec = nx.NXdata(nx.NXfield(np.zeros(shape), name='i_ec'))
            i_ec.nxerrors = np.zeros(shape)
            monitor_ec = 1
            time_ec = 1
            trans_ec = 1
            i_eb = nx.NXdata(nx.NXfield(np.zeros(shape), name='i_eb'))
            i_eb.nxerrors = np.zeros(shape)
            monitor_eb = 1
            time_eb = 1
            x0 = default_params['x0']
            y0 = default_params['y0']
            sub_mask = np.zeros(shape)

        x_pixel_size = entry['instrument/detector' + str(i) + '/x_pixel_size'].nxdata
        y_pixel_size = entry['instrument/detector' + str(i) + '/y_pixel_size'].nxdata
        solid_angle = x_pixel_size * y_pixel_size / (distance[i] ** 2)
        y, x = np.indices(shape, dtype='float')
        y = (y - y0) * y_pixel_size
        x = (x - x0) * x_pixel_size
        r = np.sqrt(x ** 2 + y ** 2)
        theta = np.arctan(r / distance[i])
        chi = np.angle(x + 1j*y)

        if monitor_eb == 1:  # no empty beam
            fb = nx.NXdata(nx.NXfield(np.zeros(shape), name='i_eb'))
            fb.nxerrors = np.zeros(shape)
        else:
            fb = i_eb - i_dark*time_eb/time_dark
            fb /= monitor_eb
        trans_ec = trans_ec ** 0.5
        if monitor_ec == 1 and time_ec == 1 and trans_ec == 1:  # no empty cell given
            z_fec = nx.NXdata(nx.NXfield(np.zeros_like(i_sample.nxsignal), name='z_fec'))
            z_fec.nxerrors = np.zeros_like(i_sample.nxsignal)
        else:
            z_fec = (i_ec - i_dark*time_ec/time_dark) / monitor_ec - fb * np.power(trans_ec, 2 / np.cos(theta))
            z_fec /= trans_ec ** (1 / np.cos(theta)) * (trans_ec + tr_theta(trans_ec, theta))

        # substarct the contributions
        fs = (i_sample - i_dark*time_sample/time_dark) / monitor_sample
        fs -= fb * trans_ec ** (2 / np.cos(theta)) * transmission ** (1 / np.cos(theta))
        fs -= z_fec * tr_theta(trans_ec, theta) * ((transmission * trans_ec) ** (1 / np.cos(theta)) +
                                                   trans_ec * transmission)
        fs /= tr_theta(transmission, theta) * trans_ec * trans_ec ** (1 / np.cos(theta)) * 0.1 * thickness
        fs /= solid_angle
        fs /= np.cos(theta) ** 3
        # normalization by water
        norm_mask = np.zeros(shape)
        if norm_file:
            if os.path.exists(norm_file):
                norm_root = nx.nxload(norm_file, mode='a')
                if 'water_substracted' in norm_root.keys():
                    i_water = norm_root['water_substracted/data'+str(i)]
                else:
                    norm_root.close()
                    treat_normalization_package(norm_file)
                    norm_root = nx.nxload(norm_file, mode='r')
                    i_water = norm_root['water_substracted/data' + str(i)]
                fs /= i_water
                if 'mask' in norm_root['parameters/detector' + str(i)]:
                    norm_mask = norm_root['parameters/detector' + str(i) + '/mask'].nxdata
            else:
                print('normalization file not found')
        # compute Q, Qx anq Qy
        wavelength = entry['instrument/source/incident_wavelength'].nxdata
        q_grid = 4*np.pi*np.sin(theta/2)/wavelength
        qx_grid = q_grid * np.cos(chi)
        qy_grid = q_grid * np.sin(chi)
        qx_binned = np.histogram_bin_edges(qx_grid, bins=shape[1])
        qx_binned = (qx_binned[:-1] + qx_binned[1:]) / 2
        qy_binned = np.histogram_bin_edges(qy_grid, bins=shape[0])
        qy_binned = (qy_binned[:-1] + qy_binned[1:]) / 2

        # handle mask if norm normalization and substraction mask are differeent, they are merged
        mask_sum = np.logical_or(norm_mask, sub_mask)
        entry['instrument/detector' + str(i) + '/pixel_mask'] = mask_sum
        entry['instrument/detector' + str(i) + '/pixel_mask_applied'] = False

        data = nx.NXdata()
        # data.nxsignal = nx.NXfield(np.ma.masked_array(fs.nxsignal.nxdata, mask=mask_sum)
        #                            , name='I', attrs={'units': r'cm$^{-1}$'})
        data.nxsignal = nx.NXfield(fs.nxsignal.nxdata,
                                   name='I', attrs={'units': r'cm$^{-1}$'})
        # data.nxerrors = np.ma.masked_array(fs.nxerrors.nxdata, mask=mask_sum)
        data.nxerrors = fs.nxerrors.nxdata
        data.nxaxes = [nx.NXfield(qy_binned, name='Qy', attrs={'units': r'$A^{-1}$'}),
                       nx.NXfield(qx_binned, name='Qx', attrs={'units': r'$A^{-1}$'})
                       ]

        del entry['data' + str(i)]
        # entry['data' + str(i)] = fs
        entry['data' + str(i)] = data
        # entry['data'+ str(i)].attrs['units'] = r'cm^{-1}'
    return


@nxlib.treatment_function(new_entry=True)
def azimutal_integration(root: nx.NXroot, bins: int = None) -> None:
    last_key = nxlib.get_last_entry_key(root)
    entry = root[last_key]
    nDet = nxlib.get_detector_number(root)
    # format bins list in order to remove as much bugs as possible bugs due to bad typing
    if type(bins) != list:
        bins = [bins]
    while len(bins) < nDet:
        bins.append(None)
    if len(bins) > nDet:
        bins = bins[:nDet]

    for i in range(nDet):
        x0 = entry['instrument/detector'+str(i)+'/beam_center_x'].nxdata
        y0 = entry['instrument/detector'+str(i)+'/beam_center_y'].nxdata
        x_pixel_size = entry['instrument/detector'+str(i)+'/x_pixel_size']
        y_pixel_size = entry['instrument/detector'+str(i)+'/y_pixel_size']
        m = entry['data'+str(i)].nxsignal.nxdata
        mask_data = entry['instrument/detector'+str(i)+'/pixel_mask'].nxdata
        signal_key = entry['data' + str(i)].signal
        if 'signal_key' + '_errors' in entry['data'+str(i)]:
            error = entry['data'+str(0)].nxerrors.nxdata
        else:
            error = None
        if bins[i] is None:
            bins[i] = get_default_reduction_parameters(root)['bins'][i]
        # get signal units
        sig_unit = ''
        if 'units' in entry['data' + str(i)].nxsignal.attrs:
            sig_unit = entry['data' + str(i)].nxsignal.attrs['units']

        del entry['data' + str(i)]
        r, intensity, sigma, dr = flib.regiso(m, mask_data, x0, y0, x_pixel_size, y_pixel_size,
                                              bins[i], error=error)
        wavelength = entry['instrument/source/incident_wavelength'].nxdata
        distance = entry['instrument/detector' + str(i) + '/distance'].nxdata
        theta = np.arctan(r/distance)
        q = 4 * np.pi / wavelength * np.sin(theta / 2)
        entry['data'+str(i)] = nx.NXdata()
        # new_entry.data.I = nx.NXfield(i, units='counts')  # uncertainties='I_errors'
        entry['data'+str(i)].nxsignal = nx.NXfield(intensity, name=signal_key, attrs={'interpretation': 'spectrum',
                                                                                    'units': sig_unit})
        entry['data'+str(i)].nxerrors = sigma
        entry['data'+str(i)].nxaxes = nx.NXfield(q, name='Q', attrs={'units': '1/A'})
        # entry['data'+str(i)].r_errors = nx.NXfield(dr, attrs={'units': 'mm'})
    # new_entry.data.nxerrors = sigma
    # new_entry.process = nx.NXprocess(program='azimutal integration',
    #                                  sequence_index=1,
    #                                  date=str(datetime.datetime.today()))
    return


def treat_normalization_package(norm_file: str) -> None:
    """
    Substract the water file stored within the normalization packaged file

    :param norm_file: filepath of the nexus normalization file
    :type norm_file: str
    """
    def delta(u, a):
        if u == 1:
            v = 1
        else:
            v = (1 - x ** a) / (-a * np.log(x))
        return v

    def tr_theta(t, angle):
        if t == 1:
            t_th = 1
        else:
            t_th = t * (t ** (1 - 1 / np.cos(angle)) - 1) / (np.log(t) * (1 - 1 / np.cos(angle)))
        return t_th
    if not os.path.exists(norm_file):
        print('normalization file not found')
        return
    norm_root = nx.nxload(norm_file, mode='rw')
    if 'water' not in norm_root.keys():
        print('no water file in the normalisation package')
        return
    if 'water_substracted' not in norm_root.keys():
        new_entry = norm_root['water'].copy()
        norm_root['water_substracted'] = new_entry

    water_entry = norm_root['water_substracted']
    transmission = water_entry.sample.transmission.nxdata

    for i in range(nxlib.get_detector_number(norm_root)):
        distance_key = 'instrument/detector' + str(i) + '/distance'
        distance = water_entry[distance_key].nxdata
        i_water = water_entry['data'+str(i)]
        i_water.nxerrors = nx.NXfield(np.sqrt(np.abs(i_water.data.nxdata)))
        monitor_sample = water_entry['monitor/integral'].nxdata
        time_sample = water_entry['monitor/count_time'].nxdata
        shape = i_water.nxsignal.nxdata.shape

        # uncack the substraction package file
        if 'dark' in norm_root:
            i_dark = norm_root['dark/data'+str(i)]
            # i_dark.nxerrors = np.zeros(shape)
            i_dark.nxerrors = nx.NXfield(np.sqrt(np.abs(i_dark.data.nxdata)))
            # monitor_dark = sub_root['dark/monitor3/integral'].nxdata
            time_dark = norm_root['dark/monitor/count_time'].nxdata
        else:
            i_dark = nx.NXdata(nx.NXfield(np.zeros(shape), name='i_dark'))
            i_dark.nxerrors = np.zeros(shape)
            # monitor_dark = 1
            time_dark = 1
        if 'empty cell' in norm_root:
            i_ec = norm_root['empty cell/data'+str(i)]
            i_ec.nxerrors = nx.NXfield(np.sqrt(np.abs(i_ec.nxsignal.nxdata)))
            monitor_ec = norm_root['empty cell/monitor/integral'].nxdata
            time_ec = norm_root['empty cell/monitor/count_time'].nxdata
            trans_ec = norm_root['empty cell/sample/transmission'].nxdata
        else:
            i_ec = nx.NXdata(nx.NXfield(np.zeros(shape), name='i_ec'))
            i_ec.nxerrors = np.zeros(shape)
            monitor_ec = 1
            time_ec = 1
            trans_ec = 1
        if 'empty beam' in norm_root:
            i_eb = norm_root['empty beam/data'+str(i)]
            i_eb.nxerrors = nx.NXfield(np.sqrt(np.abs(i_eb.data.nxdata)))
            monitor_eb = norm_root['empty beam/monitor/integral'].nxdata
            time_eb = norm_root['empty beam/monitor/count_time'].nxdata
        else:
            i_eb = nx.NXdata(nx.NXfield(np.zeros(shape), name='i_eb'))
            i_eb.nxerrors = np.zeros(shape)
            monitor_eb = 1
            time_eb = 1

        # centers for regroupement
        if 'beam_center_x' in norm_root['parameters/detector'+str(i)]:
            x0 = norm_root['parameters/detector'+str(i)+'/beam_center_x'].nxdata
            water_entry['instrument/detector'+str(i)+'/beam_center_x'] = x0
        else:
            x0 = water_entry['instrument/detector'+str(i)+'/beam_center_x'].nxdata
        if 'beam_center_y' in norm_root['parameters/detector'+str(i)]:
            y0 = norm_root['parameters/detector'+str(i)+'/beam_center_y'].nxdata
            water_entry['instrument/detector' + str(i) + '/beam_center_y'] = y0
        else:
            y0 = water_entry['instrument/detector' + str(i) + '/beam_center_y']
        x_pixel_size = water_entry['instrument/detector' + str(i) + '/x_pixel_size'].nxdata
        y_pixel_size = water_entry['instrument/detector' + str(i) + '/y_pixel_size'].nxdata
        y, x = np.indices(shape, dtype='float')
        y = (y - y0)*y_pixel_size
        x = (x - x0)*x_pixel_size
        r = np.sqrt(x ** 2 + y ** 2)
        theta = np.arctan(r / distance)
        solid_angle = x_pixel_size * y_pixel_size / (distance ** 2)
        if monitor_eb == 1:  # no empty beam
            fb = nx.NXdata(nx.NXfield(np.zeros(shape), name='i_eb'))
            fb.nxerrors = np.zeros(shape)
        else:
            fb = i_eb - i_dark*time_eb/time_dark
            fb /= monitor_eb
        trans_ec = trans_ec ** 0.5
        if monitor_ec == 1 and time_ec == 1 and trans_ec == 1:  # no empty cell given
            z_fec = nx.NXdata(nx.NXfield(np.zeros_like(i_water.nxsignal), name='z_fec'))
            z_fec.nxerrors = np.zeros_like(i_water.nxsignal)
        else:
            z_fec = (i_ec - i_dark*time_ec/time_dark) / monitor_ec - fb * np.power(trans_ec, 2 / np.cos(theta))
            z_fec /= trans_ec ** (1 / np.cos(theta)) * (trans_ec + tr_theta(trans_ec, theta))

        # substarct the contributions
        fs = (i_water - i_dark*time_sample/time_dark) / monitor_sample
        fs -= fb * trans_ec ** (2 / np.cos(theta)) * transmission ** (1 / np.cos(theta))
        fs -= z_fec * tr_theta(trans_ec, theta) * ((transmission * trans_ec) ** (1 / np.cos(theta)) +
                                                   trans_ec * transmission)
        fs /= tr_theta(transmission, theta) * trans_ec * trans_ec ** (1 / np.cos(theta)) * 0.1
        fs /= solid_angle
        fs /= np.cos(theta) ** 3
        del water_entry['data'+str(i)]
        water_entry['data'+str(i)] = fs
        # q_scale(root.file_name, distance=distance, new_entry=False)
        norm_root.close()
    return


@nxlib.treatment_function(new_entry=True)
def normalization_factor(root: nx.NXroot, factor: float = None) -> None:
    """
    Apply a multiplcation factor to the current data
    :param root: NXroot data
    :type root: NXroot
    :param factor: multiplication factor applied to each detector. Any missing factor within the list is assumed to be 1.
    :type factor: Union[list,float]
    :return:
    """
    nDet = nxlib.get_detector_number(root)
    if type(factor) != list:
        factor = [factor]
    while len(factor) < nDet:
        factor.append(1.0)
    if len(factor) > nDet:
        factor = factor[:nDet]
    last_key = nxlib.get_last_entry_key(root)
    entry = root[last_key]

    for i in range(nDet):
        entry['data' + str(i)].nxsignal *= factor[i]
        entry['data' + str(i)].nxerrors *= factor[i]
    return


@nxlib.treatment_function(new_entry=True)
def cut(root: nx.NXroot, xmin: float = None, xmax: float = None, detector_number: int = 0) -> None:
    """
    Cut 1D scattering spectra between xmin and xmax on a given detector
    :param root: data file NXroot
    :param xmin: lower bound
    :type xmin: float
    :param xmax: upper bound
    :type xmax: float
    :param detector_number: detector number of identifiaction (default is 0, corresponding to centra detector)
    :type detector_number: int, optional
    :return:
    """
    last_key = nxlib.get_last_entry_key(root)
    entry = root[last_key]
    data = entry['data' + str(detector_number)]
    if np.ndim(data.nxsignal.nxdata) == 1:
        x = data.nxaxes[0].nxdata
        if xmin is None:
            xmin = np.min(x)
        if xmax is None:
            xmax = np.max(x)
        index1 = np.argwhere(x >= xmin)
        index2 = np.argwhere(x <= xmax)
        index = np.intersect1d(index1, index2)
        data_cut = data[np.min(index):np.max(index)]
        # data_cut.nxsignal = data.nxsignal[index]
        # data_cut.nxaxes = data.nxaxes[0][index]
        # if data.signal + '_errors' in data:
        #     i_errors = data[data.signal + '_errors'].nxdata[index]
        #     data_cut.nxerrors = i_errors
        #
        # if data.axes[0] + '_errors' in data:
        #     x_errors_key = data.axes[0] + '_errors'
        #     data_cut.insert(data[x_errors_key][index], name=x_errors_key)

        del entry['data' + str(detector_number)]
        entry['data' + str(detector_number)] = data_cut
        return


# TODO : finish this
@nxlib.treatment_function(output_file=True, new_entry=False)
def concat(concat_file, *args):
    """
    Concatenate 1D data files
    :param concat_file: file path of the generated concatenated file
    :param args: data file paths to be concatenated
    :return:
    """
    if len(args) <= 1:
        raise ValueError("More than one file is needed to be concatenated")
    root = nx.nxload(args[0], mode='r')
    new_root = nx.nxload(concat_file, mode='w')
    last_entry_key = nxlib.get_last_entry_key(root)
    nxlib.copy_entry(new_root, root, 'entry0', last_entry_key)
    data_key = nxlib.get_nxdata_key(root, last_entry_key)
    root.close()
    for key in data_key:
        nxdataList = []
        del new_root['entry0/' + key]
        for file in args:
            root = nx.nxload(file, mode='r')
            last_entry_key = nxlib.get_last_entry_key(root)
            nxdataList.append(root[last_entry_key + '/' + key])
            root.close()
        nxdata_conc = nxlib.concatnxdata(nxdataList)
        new_root['entry0/' + key] = nxdata_conc
        new_root.close()
    return
