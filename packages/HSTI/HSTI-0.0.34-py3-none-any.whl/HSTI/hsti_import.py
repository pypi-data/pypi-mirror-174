import cv2 as cv
import numpy as np
import os

def import_data_cube(path, verbose = False):
    """
    ########## import_data_cube ##########
This function imports the hyperspectral thermal datacube from the raw output (.ppm)
of the camera. The path that the function uses as input must be the one containing
the 'images' directory.
    """

    impath = path + '/images/capture/'

    try:
        number_of_image_files = sum([ '.ppm' in s for s in os.listdir(impath)])
        steps = np.arange(0,number_of_image_files*10,10)
        imgs = []
        for step in steps:
            imgs.append(np.rot90(cv.imread(f'{impath}step{step}.ppm',cv.IMREAD_ANYDEPTH)))
        imgs = np.array(imgs, dtype = 'float64')
        imgs = np.moveaxis(imgs, 0, 2)
        if verbose:
            print('Hyperspectral image shape:')
            print(imgs.shape)

    except:
        print('Path should be directory containing the \'images\' directory.')

    return imgs

    """
    ########## import_image_acquisition_settings ##########
    his function imports the image acquisition settings during the capturing event.
    The path that the function uses as input must be the one containing the
    'images' directory.
    """
def import_image_acquisition_settings(path, verbose = False):

    with open(f"{path}/output.txt", 'r') as file:
        lines = file.readlines()
        temperature_lst = []
        for line in lines:
            if (len(line.split()) == 13) or (len(line.split()) == 10):
                temperature_lst.append(int(line.split()[6])/1000)
        sens_T = np.mean(temperature_lst)
        if len(lines[-1].split()) == 13:
            GSK = int(lines[-1].split()[10])
            GFID = int(lines[-1].split()[11])
            Gain = float(lines[-1].split()[12])
        else:
            GSK = None
            GFID = None
            Gain = None

    if verbose:
        print(f'Sensor temperature: {sens_T}')
        print(f'GSK: {GSK}')
        print(f'GFID: {GFID}')
        print(f'Gain: {round(Gain,2)}')

    valdict = {
      'SENS_T': sens_T,
      'GSK': GSK,
      'GFID': GFID,
      'GAIN': Gain
    }

    return valdict
