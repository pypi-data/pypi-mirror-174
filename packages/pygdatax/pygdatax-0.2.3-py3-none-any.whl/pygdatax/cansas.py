import nexusformat.nexus as nx
from nexusformat.nexus.tree import NeXusError
import fabio
import numpy as np
import struct
import re
from pygdatax import nxlib


def createEmptyNXsas(spectro_name='generic_sans', detector_number=1):
    """
    Create
    Args:
        spectro_name:
        detector_number:

    Returns:

    """
    root = nx.NXroot()
    root.attrs['default'] = 'entry0'
    root.attrs['NX_class'] = b'NXroot'
    entry = nx.NXentry()
    # entry.attrs['default'] = 'data'
    entry.attrs['version'] = '1.1'
    entry.title = nx.NXfield(value='')
    entry.run = nx.NXfield(value=0)
    entry.definition = nx.NXfield(definition='NXcanSAS')
    # entry.date=nx.NXfield(date=)

    # building instrument
    instrument = nx.NXinstrument(description=spectro_name, name=spectro_name, attrs={'canSAS_class': 'SASinstrument'})
    # intrument/aperture
    aperture = nx.NXaperture(shape='rectangular',  # rectangular or cicular
                             # (for circular, x and y should be equal to the diameter)
                             x_gap=nx.NXfield(None, attrs={'units': 'mm'}),
                             y_gap=nx.NXfield(None, attrs={'units': 'mm'}))
    # collimation
    collimator = nx.NXcollimator(length=nx.NXfield(None, units='mm'),
                                 distance=nx.NXfield(None, units='mm')
                                 )
    # instrument/detector
    for i in range(detector_number):
        detector = nx.NXdetector(data=None,
                                 distance=nx.NXfield(None, attrs={'units': 'mm'}),
                                 x_position=nx.NXfield(None, attrs={'units': 'mm'}),
                                 y_position=nx.NXfield(None, attrs={'units': 'mm'}),
                                 beam_center_x=nx.NXfield(None, attrs={'units': 'pixel'}),
                                 beam_center_y=nx.NXfield(None, attrs={'units': 'pixel'}),
                                 x_pixel_size=nx.NXfield(None, attrs={'units': 'mm'}),
                                 y_pixel_size=nx.NXfield(None, attrs={'units': 'mm'}),
                                 description='',
                                 pixel_mask=None,
                                 name='detector'+str(i),
                                 dead_time=nx.NXfield(0.0, attrs={'units': 's'}),
                                 countrate_correction_applied=False
                                 )
        entry.insert(nx.NXdata(attrs={'interpretation': b"image",
                                      'signal': "data"}), name='data'+str(i))
        instrument.insert(detector)

    # instrument/source
    source = nx.NXsource(type='', probe='', description='',
                         shape='rectangular',  # rectangular or cicular
                         # (for circular, x and y should be equal to the diameter)
                         incident_wavelength=nx.NXfield(None, attrs={'units': 'angstrom'}),
                         incident_wavelength_spread=nx.NXfield(None, attrs={'units': '%'}),
                         beam_size_x=nx.NXfield(None, attrs={'units': 'mm'}),
                         beam_size_y=nx.NXfield(None, attrs={'units': 'mm'})
                         )
    # insturment monitor (not present in canSAS but I think it is very important to have it for normalization procedure)
    monitor = nx.NXmonitor(integral=None,
                           mode='timer',  # 'timer' or 'monitor'
                           count_time=nx.NXfield(None, attrs={'units': 's'}),
                           preset = None)

    entry.instrument = instrument
    entry.instrument.insert(aperture)
    entry.instrument.insert(collimator)
    entry.instrument.insert(source)
    entry.insert(monitor, name='monitor')

    sample = nx.NXsample(thickness=nx.NXfield(1.0, attrs={'units': 'mm'}),
                         transmission=nx.NXfield(1.0),
                         x_position=nx.NXfield(0.0, attrs={'units': 'mm'}),
                         y_position=nx.NXfield(0.0, attrs={'units': 'mm'}),
                         # rotation axis parallel to the incident beam
                         roll=nx.NXfield(None, attrs={'units': 'deg'}),
                         # horizontal vertical axis perpendicular to the incident beam
                         pitch=nx.NXfield(None, attrs={'units': 'deg'}),
                         # vertical rotation axis
                         yaw=nx.NXfield(None, attrs={'units': 'deg'}),
                         temperature=nx.NXfield(None, attrs={'units': '°C'}),
                         name=''
                         )
    entry.insert(sample)
    root.entry0 = entry
    return root


def sansllb2nxsas(nexusfile):
    pass


def edf2nxsas(filename):
    fileObj = fabio.open(filename)
    header = fileObj.header
    root = createEmptyNXsas(spectro_name='Xeuss')
    # run
    # title = 2020 - 12 - 30 - AC_flux_0_67489.edf;
    title = header['title']
    num = title.split('_')[-1]
    root.entry0.run = int(num.split('.')[0])
    root.entry0.title = title
    # aperture
    y_gap = float(header['s2bot']) + float(header['s2top'])
    x_gap = float(header['s2hr']) + float(header['s2hl'])
    root.entry0.instrument.aperture.x_gap.nxdata = x_gap
    root.entry0.instrument.aperture.y_gap.nxdata = y_gap
    # collimator
    root.entry0.instrument.collimator.length.nxdata = 1200
    root.entry0.instrument.collimator.distance.nxdata = 200 # approximative and depends on configuration
    # detector
    det = root.entry0.instrument.detector0
    det.distance.nxdata = float(header['SampleDistance']) * 1000
    det.x_position.nxdata = float(header['detx'])
    det.y_position.nxdata = float(header['detz'])
    det.x_pixel_size.nxdata = float(header['PSize_1']) * 1000
    det.y_pixel_size.nxdata = float(header['PSize_2']) * 1000
    det.beam_center_x.nxdata = float(header['Center_1'])
    det.beam_center_y.nxdata = float(header['Center_2'])
    det.dead_time.nxdata = 0.0
    det.countrate_correction_applied = True
    det.data = nx.NXfield(fileObj.data)
    det.description = "Pilatus 1M"
    # instrument/monitor
    moni = root.entry0.instrument.monitor
    moni.mode = 'timer'
    moni.count_time.nxdata = float(header['count_time'])
    # Since there is no monitor on the xeuss, we take the measurement of the flux (transEmpty_beam) and multiply it by
    # the acquisition time assuming no source fluctuation
    moni.integral.nxdata = float(header['pilai1'])*float(header['count_time'])
    # instrument/source
    source = root.entry0.instrument.source
    sizeX = float(header['s1hr']) + float(header['s1hl'])
    sizeY = float(header['s1bot']) + float(header['s1top'])
    source.beam_size_x.nxdata = sizeX
    source.beam_size_y.nxdata = sizeY
    source.probe = 'x-ray'
    source.type = 'Fixed Tube X-ray'
    source.description = 'Genix 3D'
    source.incident_wavelength.nxdata = float(header['WaveLength'])*1.0e10
    source.incident_wavelength_spread = 0.0
    # sample
    sample = root.entry0.sample
    sample.name = header['Comment']
    sample.thickness.nxdata = 1.5
    sample.x_position.nxdata = float(header['x'])
    sample.y_position.nxdata = float(header['z'])
    sample.pitch.nxdata = float(header['om'])
    sample.yaw.nxdata = float(header['phi'])
    sample.roll.nxdata = 0.0
    sample.temperature.nxdata = float(header['Temperature'])
    # link data field to detector data
    if 'data0' in root.entry0:
        del root['entry0/data0']
        root.entry0.data0 = nx.NXdata(attrs={'interpretation': b"image",
                                            'signal': "data"})
    root.entry0.data0.makelink(root.entry0.instrument.detector0.data)
    root.entry0.attrs['default'] = 'data0'
    # save nexus file with the same name as the edf file and the same folder but with .nxs extension
    new_name = filename.split('.')[0]
    new_name += '.nxs'
    try:
        root.save(new_name, mode='w')
        root.close()
    except NeXusError:
        print('error')
        if os.path.exists(new_name):
            print('already here')
            os.remove(new_name)
            root.save(new_name, mode='w')
            root.unlock()
        else:
            print('something else')

    return root


# def xy2nxcansas(filename):
#     with open(filename, 'rb') as fid:
#         #        The first 256 characters contains information on the sample
#         hd = fid.read(256)
#         #       read binary data (32 bit int : 'I')
#         binarySize = struct.calcsize(128 * 128 * 'I')
#         fid.seek(256)
#         binData = fid.read(binarySize)
#         #        read last rows
#         tl = fid.read()
#     hd = hd.decode(encoding='latin-1')
#     numData = struct.unpack(128 * 128 * 'I', binData)
#     m = np.asarray(numData, dtype=np.int32)
#     m.shape = (128, 128)
#     #    m=np.flip(m,1)
#     tl = tl.decode(encoding='latin-1')
#     tl = tl.splitlines()
#     tl.pop(0)
#     #    convert tail as dictionnary veq
#     comp = re.compile(r"\s* = \s*")
#     veq = {}
#     for line in tl:
#         [key, value] = comp.split(line)
#         try:
#             fValue = float(value)
#         except ValueError:
#             fValue = value
#         veq[key] = fValue
#
#     et = {}
#     et['type'] = 'XY'
#     et['x'] = 'PIXEL'
#     et['y'] = 'PIXEL'
#     et['z'] = 'N'
#     #    store header data in et dictionnary
#     et['spectro'] = 'PA' + hd[:2]
#     et['numero'] = int(hd[2:6])
#     et['commentaire'] = hd[6:12] + '-' + hd[12:24]
#     et['date'] = hd[38:48] + '-' + hd[48:56]
#     et['temps'] = float(hd[24:30])
#     et['moniteur'] = int(hd[30:38])
#     et['diviseur'] = 1
#     et['imax'] = int(hd[56:61])
#     et['vitesse_selecteur'] = float(hd[61:66])
#     et['distance'] = float(hd[68:73])
#     #    from tail
#     et['ep'] = veq['Thickness Sample']
#     et['tr'] = veq['Transmission']
#     et['wavelength'] = veq['Lambda (lecture)']
#     et['dlsurl'] = veq['Delta-Lambda/Lambda'] / 235.48
#     et['d3'] = veq['Diaphragmes 0m']
#     et['d2'] = veq['Diaphragmes 2m']
#     et['d1'] = veq['Diaphragmes 5m']
#     et['dc'] = veq['D Coll(m)']
#     et['eff'] = veq['Efficacite Detecteur']
#     et['t0'] = veq['Temps Mort micro-seconde']
#     et['x0'] = veq['X0']
#     et['y0'] = veq['Y0']
#     et['dr'] = veq['Resolution']
#     et['MueDetecteur'] = et['eff'] * et['wavelength']
#     et['r0'] = veq['Diametre_beam']
#     et['rm'] = np.inf
#     et['veq'] = veq
#     #    For resolution calculation
#     et['r2'] = et['d3'] / 2
#     if et['dc'] < 3000:
#         et['r1'] = et['d2'] / 2
#     else:
#         et['r1'] = et['d1'] / 2
#     #        additional field on pinguoin data
#     if 'TrSum' in veq:
#         et['TrSum'] = veq['TrSum']
#     #    Legend type
#     leg = {'x': 'x (pixel)', 'y': 'y (pixel)', 'z': 'n'}
#
#     d = {'m': m, 'et': et, 'leg': leg}
#     root = createEmptyNXcansas(spectro_name='Xeuss')
#     # run
#     # title = 2020 - 12 - 30 - AC_flux_0_67489.edf;
#     title = header['title']
#     num = title.split('_')[-1]
#     root.entry0.run = int(num.split('.')[0])
#     # collimator
#     root.entry0.instrument.collimator.length.nxdata = veq['D Coll(m)']
#     root.entry0.instrument.collimator.distance.nxdata = 0  # approximative and depends on configuration
#     # aperture
#     d3 = veq['Diaphragmes 0m']
#     d2 = veq['Diaphragmes 2m']
#     d1 = veq['Diaphragmes 5m']
#     root.entry0.instrument.shape = 'circular'
#     root.entry0.instrument.aperture.x_gap.nxdata = d3
#     root.entry0.instrument.aperture.y_gap.nxdata = d3
#     # detector
#     det = root.entry0.instrument.detector0
#     det.distance.nxdata = float(hd[68:73])
#     # det.x_position.nxdata = float(header['detx'])
#     # det.y_position.nxdata = float(header['detz'])
#     det.x_pixel_size.nxdata = veq['Resolution']
#     det.y_pixel_size.nxdata = veq['Resolution']
#     det.beam_center_x.nxdata = veq['X0']
#     det.beam_center_y.nxdata = veq['Y0']
#     det.data = nx.NXfield(m)
#     det.pixel_mask = np.zeros_like(m)
#     # instrument/monitor
#     moni = root.entry0.instrument.monitor
#     moni.mode = 'timer'
#     moni.count_time.nxdata = float(hd[24:30])
#     moni.integral.nxdata = int(hd[30:38])
#     # instrument/source
#     source = root.entry0.instrument.source
#     source.shape = 'circular'
#     source.probe = 'neutron'
#     source.type = 'Reactor Neutron Source'
#     source.description = 'Orphée'
#     source.incident_wavelength = veq['Lambda (lecture)']
#     source.incident_wavelength_spread = veq['Delta-Lambda/Lambda'] / 235.48
#     # select the good collimating diaphragm according to collimation distance
#     if veq['D Coll(m)'] < 3000:
#         source.beam_size_x.nxdata = d2
#         source.beam_size_y.nxdata = d2
#     else:
#         source.beam_size_x.nxdata = d1
#         source.beam_size_y.nxdata = d1
#     # sample
#     sample = root.entry0.sample
#     sample.sample_name = header['Comment']
#     sample.thickness.nxdata = 1.5
#     sample.x_position.nxdata = float(header['x'])
#     sample.y_position.nxdata = float(header['z'])
#     sample.pitch.nxdata = float(header['om'])
#     sample.yaw.nxdata = float(header['phi'])
#     sample.roll.nxdata = 0.0
#     sample.temperature.nxdata = float(header['Temperature'])
#     # link data field to detector data
#     if 'data' in root.entry0:
#         del root['entry0/data']
#         root.entry0.data = nx.NXdata(attrs={'interpretation': b"image",
#                                             'signal': "data"})
#     root.entry0.data.makelink(root.entry0.instrument.detector0.data)
#     root.entry0.attrs['default'] = 'data'
#     # save nexus file with the same name as the edf file and the same folder but with .nxs extension
#     new_name = filename.split('.')[0]
#     new_name += '.nxs'
#     try:
#         root.save(new_name, mode='w')
#         root.close()
#     except NeXusError:
#         print('error')
#         if os.path.exists(new_name):
#             print('already here')
#             os.remove(new_name)
#             root.save(new_name, mode='w')
#             root.unlock()
#         else:
#             print('something else')
#     #
#     return root


# TODO: finish that
def sansone2nxsas(filename):
    root_ini = nx.nxload(filename)
    entry = root_ini.entry1
    root = createEmptyNXsas(spectro_name='SANS-I')
    os.path.basename(filename)
    root.entry0.title = entry.sample.name[0]
    root.entry0.run = os.path.basename(filename).split('.')[0]
    # aperture
    root.entry0.instrument.aperture.shape = 'circular'
    # TODO : put the rigth collimation geometry
    root.entry0.instrument.aperture.x_gap.nxdata = 10
    root.entry0.instrument.aperture.y_gap.nxdata = 10
    # collimator
    root.entry0.instrument.collimator.length.nxdata = entry.SANS.collimator.length.nxdata[0]*1000  # in mm
    root.entry0.instrument.collimator.distance.nxdata = 0  # We assume no shift between last slit and the sample
    # detector
    det = root.entry0.instrument.detector0
    det.beam_center_x.nxdata = entry.SANS.detector.beam_center_x.nxdata[0]
    det.beam_center_y.nxdata = entry.SANS.detector.beam_center_y.nxdata[0]
    det.data = entry.SANS.detector.counts.nxdata
    det.description = "3He PSD"
    det.distance.nxdata = entry.SANS.detector.x_position.nxdata[0]
    det.x_position.nxdata = entry.SANS.detector.y_position.nxdata[0]
    det.y_position.nxdata = 0.0
    det.x_pixel_size.nxdata = 7.5
    det.y_pixel_size.nxdata = 7.5
    # monitor
    # TODO : choose the write monitor. According to Joachim, this is the last one with non zero value butfor viai e
    moni = root.entry0.instrument.monitor
    moni.count_time.nxdata = entry.SANS.detector.counting_time[0]
    moni.integral.nxdata = entry.SANS.detector.preset[0]
    # moni.integral.nxdata = entry.SANS.monitor_7.counts[0]
    moni.mode = entry.SANS.detector.count_mode[0]
    # source
    source = root.entry0.instrument.source
    source.shape = 'circular'
    # TODO: put the right collimation apertures
    source.beam_size_x.nxdata = 10.0  # arbitrary
    source.beam_size_y.nxdata = 10.0  # arbitrary
    source.description = 'SINQ'
    source.incident_wavelength.nxdata = entry.SANS['Dornier-VS/lambda'][0]/10 # conversion in Angstrom
    # TODO: check velocity selctor wavelength spread. I fix it to 11.6% as for PAXY
    source.incident_wavelength.nxdata = entry.SANS['Dornier-VS/lambda'][0] / 10
    source.incident_wavelength_spread.nxdata = 0.116
    # sample
    sample = root.entry0.sample
    sample.name = entry.sample.name[0]
    sample.thickness.nxdata = 1.0
    sample.transmission = 1.0
    # TODO: check postion and angle of sample
    sample.x_position.nxdata = entry.sample.x_position[0]
    sample.y_position.nxdata = entry.sample.y_position[0]
    # data field
    # link data field to detector data
    if 'data0' in root.entry0:
        del root['entry0/data0']
        root.entry0.data0 = nx.NXdata(attrs={'interpretation': b"image",
                                            'signal': "data"})
    root.entry0.data0.makelink(root.entry0.instrument.detector0.data)
    root.entry0.attrs['default'] = 'data0'
    root_ini.close()
    new_name = filename.split('.')[0]
    new_name += '.nxs'
    try:
        root.save(new_name, mode='w')
        root.close()
    except NeXusError:
        print('error')
        if os.path.exists(new_name):
            print('already here')
            os.remove(new_name)
            root.save(new_name, mode='w')
            root.unlock()
        else:
            print('something else')
    return root


def paxy2nxsas(filename):
    with open(filename, 'rb') as fid:
        #        The first 256 characters contains information on the sample
        hd = fid.read(256)
        #       read binary data (32 bit int : 'I')
        binarySize = struct.calcsize(128 * 128 * 'I')
        fid.seek(256)
        binData = fid.read(binarySize)
        #        read last rows
        tl = fid.read()
    hd = hd.decode(encoding='latin-1')
    numData = struct.unpack(128 * 128 * 'I', binData)
    m = np.asarray(numData, dtype=np.int32)
    m.shape = (128, 128)
    #    m=np.flip(m,1)
    tl = tl.decode(encoding='latin-1')
    tl = tl.splitlines()
    tl.pop(0)
    #    convert tail as dictionnary veq
    comp = re.compile(r"\s* = \s*")
    veq = {}
    for line in tl:
        [key, value] = comp.split(line)
        try:
            fValue = float(value)
        except ValueError:
            fValue = value
        veq[key] = fValue
    et = {}
    et['spectro'] = 'PA' + hd[:2]
    et['numero'] = int(hd[2:6])
    et['commentaire'] = hd[6:12] + '-' + hd[12:24]
    et['date'] = hd[38:48] + '-' + hd[48:56]
    et['temps'] = float(hd[24:30])
    et['moniteur'] = int(hd[30:38])
    et['diviseur'] = 1
    et['imax'] = int(hd[56:61])
    et['vitesse_selecteur'] = float(hd[61:66])
    et['distance'] = float(hd[68:73])
    #    from tail
    et['ep'] = veq['Thickness Sample']
    et['tr'] = veq['Transmission']
    et['wavelength'] = veq['Lambda (lecture)']
    et['dlsurl'] = veq['Delta-Lambda/Lambda'] / 235.48
    et['d3'] = veq['Diaphragmes 0m']
    et['d2'] = veq['Diaphragmes 2m']
    et['d1'] = veq['Diaphragmes 5m']
    et['dc'] = veq['D Coll(m)']
    et['eff'] = veq['Efficacite Detecteur']
    et['t0'] = veq['Temps Mort micro-seconde']
    et['x0'] = veq['X0']
    et['y0'] = veq['Y0']
    et['dr'] = veq['Resolution']
    et['MueDetecteur'] = et['eff'] * et['wavelength']
    et['r0'] = veq['Diametre_beam']
    et['rm'] = np.inf
    et['veq'] = veq
    #    For resolution calculation
    if et['dc'] < 3000:
        et['din'] = et['d2']
    else:
        et['din'] = et['d1']
#     d = {'m': m, 'et': et, 'leg': leg}
    root = createEmptyNXsas(spectro_name=et['spectro'])
    root.entry0.title = et['commentaire']
    root.entry0.run = int(et['numero'])
    # aperture
    root.entry0.instrument.aperture.x_gap.nxdata = et['d3']
    root.entry0.instrument.aperture.y_gap.nxdata = et['d3']
    root.entry0.instrument.aperture.shape = 'circular'
    # collimator
    root.entry0.instrument.collimator.length = et['dc']
    root.entry0.instrument.collimator.distance = 0
    # detectector
    det = root.entry0.instrument.detector0
    det.distance.nxdata = et['distance']
    det.x_position.nxdata = None
    det.y_position.nxdata = None
    det.x_pixel_size.nxdata = et['dr']
    det.y_pixel_size.nxdata = et['dr']
    det.beam_center_x.nxdata = et['x0']
    det.beam_center_y.nxdata = et['y0']
    det.data = nx.NXfield(m)
    det.description = "3He PSD"
    det.dead_time = et['t0']*1e-6
    # instrument/monitor
    moni = root.entry0.monitor
    moni.mode = 'timer' # cannot guess the mode within xy.32 files
    moni.count_time.nxdata = et['temps']
    moni.integral.nxdata = et['moniteur']
    # instrument/source
    source = root.entry0.instrument.source
    source.beam_size_x.nxdata = et['din']
    source.beam_size_y.nxdata = et['din']
    source.shape = 'circular'
    source.probe = 'neutron'
    source.type = 'Reactor Neutron Source'
    source.description = 'Orphee'
    source.incident_wavelength.nxdata = et['wavelength']
    source.incident_wavelength_spread = et['dlsurl']
    # sample
    sample = root.entry0.sample
    sample.name = et['commentaire']
    sample.thickness.nxdata = et['ep']
    sample.x_position.nxdata = None
    sample.y_position.nxdata = None
    sample.pitch.nxdata = None
    sample.yaw.nxdata = None
    sample.roll.nxdata = None
    #data
    if 'data0' in root.entry0:
        del root['entry0/data0']
        root.entry0.data0 = nx.NXdata(attrs={'interpretation': b"image",
                                             'signal': "data"})
    root.entry0.data0.makelink(root.entry0.instrument.detector0.data)
    root.entry0.attrs['default'] = 'data0'
    new_name = filename.split('.')[0]
    new_name += '.nxs'
    try:
        root.save(new_name, mode='w')
        root.close()
    except NeXusError:
        print('error')
        if os.path.exists(new_name):
            print('already here')
            os.remove(new_name)
            root.save(new_name, mode='w')
            root.unlock()
            root.close()
        else:
            print('something else')
    return


if __name__ == '__main__':
    import os
    edfFile = '/home/achennev/Documents/xeuss/2020-12-30-AC_flux/2020-12-30-AC_flux_0_67489.edf'
    edf2nxsas(edfFile)
    sans1file = '/home/achennev/Documents/PA20-PSI/example_data_files_from_SANS-1/sans2020n026648.hdf'
    sansone2nxsas(sans1file)
    root = createEmptyNXsas(spectro_name='sans_llb', detector_number=3)
    try:
        fname = '/home/achennev/Documents/PA20-PSI/sansLLB_AC_nxcansas.nxs'
        root.save(fname)
        root.close()
    except NeXusError:
        print('error')
        if os.path.exists(fname):
            print('already here')
            os.remove(fname)
            root.save(fname, mode='w')
            root.unlock()
        else:
            print('something else')

    root.close()
    paxy2nxsas('../../example_data/PAXY/XY31200.32')

    # root = createEmptyNXcansas(spectro_name='xeuss', detector_number=1)
    # new_name = '/home/achennev/Documents/test_cansas.nxs'
    # try:
    #     root.save(new_name, mode='w')
    #     root.close()
    # except NeXusError:
    #     print('error')
    #     if os.path.exists(new_name):
    #         print('already here')
    #         os.remove(new_name)
    #         root.save(new_name, mode='w')
    #         root.unlock()
    #     else:
    #         print('something else')