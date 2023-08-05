"""
File: ml.py 
-------------- 
Contains useful functions that I may import while programming 
machine learning projects.  
""" 

from matplotlib import pyplot as plt
from PIL import Image
import requests
import torch 
import numpy as np 
from glob import glob
import random
import torchvision.transforms as T


def plot_png(file_path, color):
	"""
	Plots a png file (or jpeg really) using matplotlib. Color is a bool value. 
	If true, image will be displayed in color. Else, it will be displayed in 
	greyscale.
	"""
	image = Image.open(file_path)
	if color == True:
		plt.imshow(image, interpolation='nearest')
		plt.show()
	else:
		plt.imshow(image, interpolation='nearest', cmap='Greys_r')
		plt.show()


def plot_np_img(image_array, color):
	"""
    (Here for longevity purposes... use plot instead)
	Plots a numpy array using matplotlib. Color is a bool value. If true, 
	image will be displayed in color. Else, it will be displayed in 
	greyscale.

    input: image_array must be of shape (1, H, W) or (H, W) for greyscale
    and (3, H, W) for color. 
	"""
	if color == True:
		plt.imshow(image_array, interpolation='nearest')
		plt.show()
	else:
		plt.imshow(image_array, interpolation='nearest', cmap='Greys_r')
		plt.show()


def plot(image_array, color=True):
    """
    Plots a numpy array using matplotlib. Color is a bool value which
    is true by default. If passed in as False, image will be displayed in 
    greyscale. 

    input: image_array must be of shape (1, H, W) or (H, W, 1) or (H, W) for greyscale
    and (3, H, W) or (H, W, 3) for color. 
    """

    # move to numpy is not already in numpy array format 
    image_array = np.array(image_array)
    image_array = np.squeeze(image_array)

    if color == True:
        if image_array.shape[0] == 3:
            image_array = np.moveaxis(image_array, 0, -1)
        plt.imshow(image_array, interpolation='nearest')
        plt.show()
    else:
        plt.imshow(image_array, interpolation='nearest', cmap='Greys_r')
        plt.show()


def image_dir_to_data(dirpath, extension):
    """
    Takes in a directory containing images
    and returns a list of numpy arrays representing
    those images. 
    Args:
        - dirpath: path to directory 
        - extension: image extension type (e.g. png) (string)
    """
    data_subset = []
    sub_set = glob(dirpath + '/*.' + extension)
    for elem in sub_set:
        image = Image.open(elem)
        image_array = np.array(image)
        data_subset.append(image_array)
    return data_subset  


def image_dir_to_data_norm(dirpath, extension):
    """
    (Same as image_dir_to_data but with max value 
    (255) normalization). 
    Takes in a directory containing images
    and returns a list of numpy arrays representing
    those images. 
    Args:
        - dirpath: path to directory 
        - extension: image extension type (e.g. png) (string)
    """
    data_subset = []
    sub_set = glob(dirpath + '/*.' + extension)
    for elem in sub_set:
        image = Image.open(elem)
        image_array = np.array(image)
        image_array = image_array.astype(float)
        image_array = image_array/255.0
        data_subset.append(image_array)
    return data_subset    


def gen_label_pair(data_samples, label):
	"""
	Takes in a list of data samples (i.e. images, x)
	and a corresponding label and returns a list of tuples
	where each tuple is an (x, y) pair. 
	"""
	d_set = []
	for elem in data_samples:
	    sample_pair = (elem, label)
	    d_set.append(sample_pair)
	return d_set 


def gen_distro(master_list):
    """
    Takes in a list of lists who each contain
    (x, y) tuple samples for that class and returns 
    a randomly concatenated version. 
    """
    generated_distro = []
    for class_list in master_list:
        generated_distro = generated_distro + class_list
    random.shuffle(generated_distro)
    return generated_distro


def get_img(url='https://stanford.edu/~rsikand/assets/images/seal.png', resize=True, size=(128, 128)):
    """
    Returns a sample numpy image to play with. 
    Arguments:
    -----------
    - url: Can pass in custom url if you want a different image. 
    Defaults to a baby seal!  
    - resize: by default, all images are resized to 128x128. If you'd
    like to keep the default size, specify False. 
    - size: size to resize to. Default is 128x128. 
    """

    image = np.array(Image.open(requests.get(url, stream=True).raw))


    if resize:
        if len(image.shape) == 3:
            image = np.array(T.Resize(size=size)(torch.movedim(torch.tensor(image), -1, 0)))
        else:
            image = np.array(T.Resize(size=size)(torch.tensor(image)))
    else:
        if len(image.shape) == 3:
            if image.shape[0] != 3 and image.shape[2] == 3:
                image = np.moveaxis(image, -1, 0)
            elif image.shape[0] != 1 and image.shape[2] == 1:
                image = np.moveaxis(image, -1, 0)
            else:
                image = image
        else:
            image = image

    return image


def img_dataset_from_dir(dir_path):
    """
    Given a directory containing folders
    representing classes of images, this
    functions builds a valid numpy
    dataset distribution. 
    Input (dir_path) structure: 
    dir_path/class_1, class_n/1.png 
    Note: 'dir_path' must be the raw
    dir name (no trailing dash) 
    Output: [(x,y), ..., (x,y)]
    """

    dir_path = dir_path + "/*/"
    class_list = glob(dir_path, recursive = True)
    
    master_list = []
    idx = 0
    for class_ in class_list:
        curr_class = image_dir_to_data_norm(class_, "png")
        new_arrays = []
        for elem in curr_class:
            if len(elem.shape) == 2:
                elem = np.expand_dims(elem, axis=0)
            assert len(elem.shape) == 3
            if elem.shape[0] != 3 and elem.shape[2] == 3:
                elem = np.moveaxis(elem, -1, 0)
            elif elem.shape[0] != 1 and elem.shape[2] == 1:
                elem = np.moveaxis(elem, -1, 0)
            new_arrays.append(elem)

        labeled_list = gen_label_pair(new_arrays, idx)
        master_list.append(labeled_list)
        idx += 1

    return gen_distro(master_list)


def print_model_size(net):
    """
    Function that calculates PyTorch model size
    and prints it out in mb, bytes, and num params.  
    """
    # taken from 
    # https://stackoverflow.com/questions/49201236/check-the-total-number-of-parameters-in-a-pytorch-model
    total_params = sum(p.numel() for p in net.parameters())
    
    # taken from 
    # https://discuss.pytorch.org/t/finding-model-size/130275/2 
    param_size = 0
    for param in net.parameters():
        param_size += param.nelement() * param.element_size()
    buffer_size = 0
    for buffer in net.buffers():
        buffer_size += buffer.nelement() * buffer.element_size()

    size_all_mb = (param_size + buffer_size) / 1024**2
    
    print("Total number of parameters: ", total_params)
    print("model size (bytes): ", (param_size + buffer_size))
    print('model size (mb): {:.3f}MB'.format(size_all_mb))


class MeanMetric:
  """
  Scalar metric designed to use on a per-epoch basis 
  and updated on per-batch basis. For getting average across
  the epoch. 
  """

  def __init__(self):
    self.vals = []

  def update(self, new_val):
    self.vals.append(new_val)

  def reset(self):
    self.vals = []

  def get(self):
    mean_value = sum(self.vals)/len(self.vals)
    return mean_value
    
