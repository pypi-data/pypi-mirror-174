import numpy as np
import os
import concurrent.futures as cf
import cv2

# Function for saving individual images in .ppm format
def save_img(img, path):
    cv2.imwrite(path, img)
    # Renaming the '.pgm' images to '.ppm' to follow the format coming fron the camera
    new_path = path[0:-2] + 'p' + path[-2+1:]
    os.rename(path, new_path)

def export_data_cube(data_cube, folder_name, normalize_to_cube = True):
    """
    ########## HSTI_export ##########
    This function takes an HSTI numpy array and exports it as individual .ppm
    images to a folder given by folder_name.
    """
    if os.path.isdir(os.getcwd() + '/' + folder_name) == False:
        os.mkdir(os.getcwd() + '/' + folder_name)
        os.mkdir(os.getcwd() + '/' + folder_name + '/images')
        os.mkdir(os.getcwd() + '/' + folder_name + '/images/capture')
    path = os.getcwd() + '/' + folder_name + '/images/capture'
    data_cube = np.rot90(data_cube, 3)
    img_size = [data_cube.shape[0], data_cube.shape[1]]
    NoB = data_cube.shape[2]

    if normalize_to_cube:
        data_cube = (65535.9*(data_cube - np.min(data_cube))/(np.max(data_cube) - np.min(data_cube))).astype(np.uint16)

# setting up for multi processing
    img_lst, path_lst = [], []
    for i in range(NoB):
        img_lst.append(data_cube[:,:,i])
        step = i*10
        path_lst.append(f'{path}/step{step}.pgm')

# Multiprocessing step
    with cf.ProcessPoolExecutor() as executor:
        results = executor.map(save_img, img_lst, path_lst)
