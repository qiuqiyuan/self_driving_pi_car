import argparse
import pickle
import os
from scipy import misc
import numpy as np
from util import command2int


def folder2array(folder_path,
                 pickle_path,
                 width,
                 height,
                 channels,
                 verbose):
    """
    Function to transform all images from the folder folder_name
    into a tuple of np arrays.

    :param folder_path: path to folder containing images
    :type folder_path: str
    :param pickle_path: path to pickle containing the labels
    :type pickle_path: str
    :param width: image width
    :type width: int
    :param height: image height
    :type height: int
    :param channels: image channels
    :type channels: int

    :rtype: (np.array,np.array)
    """
    all_images = []
    all_labels = []
    flat_shape = width * height * channels
    with open(pickle_path, "rb") as f:
        label_dict = pickle.load(f)
    if verbose:
        print("Trying to convert images from {} \n".format(folder_path))
    for filename in os.listdir(folder_path):
        key = filename[:- 4]
        label = command2int[label_dict[key]]
        image_path = os.path.join(folder_path, filename)
        image = change_type_to_uint8(misc.imread(image_path))
        image = image.reshape(flat_shape)
        all_images.append(image)
        all_labels.append(label)
    all_labels = change_type_to_uint8(np.array(all_labels))
    all_images = np.array(all_images)
    return all_images, all_labels


def change_type_to_uint8(image):
    """
    Change type to uint8 Unsigned integer (0 to 255)

    :param image: image as an np.array
    :type image: np.array
    :rtype: np.array
    """
    image = image.astype('uint8')
    return image


def create_data_set_as_np_array(folder_path,
                                data_name="data",
                                label_name="labels",
                                width=160,
                                height=90,
                                channels=3,
                                verbose=True):
    """
    Giving one path to a folder of folders of images,
    this function transform all images in two arrays
    one 'data_name' with all the flatted images
    and other 'label_name' with all the respective labels

    :param folder_path: path to folder containing folders of images
                        and pickles
    :type folder_path: str
    :param data_name: name of the data array to be saved
    :type data_name: str
    :param label_name: name of the labels array to be saved
    :type label_name: str
    :param width: image width
    :type width: int
    :param height: image height
    :type heights: int
    :param channels: image channels
    :type channels: int
    :param verbose: param to print path information
    :type verbose: boolean
    """
    assert os.path.exists(folder_path)
    all_images = []
    all_labels = []
    for folder in os.listdir(folder_path):
        folder = os.path.join(folder_path, folder)
        if os.path.isdir(folder):
            pickle_path = folder + "_pickle"
            images, labels = folder2array(folder,
                                          pickle_path,
                                          width,
                                          height,
                                          channels,
                                          verbose)
            all_images.append(images)
            all_labels.append(labels)
    all_images = np.concatenate(all_images, axis=0)
    all_labels = np.concatenate(all_labels, axis=0)
    all_labels = all_labels.reshape((all_labels.shape[0], 1))
    np.save(data_name, all_images)
    np.save(label_name, all_labels)


def main():
    """
    Script to transform one folder containing folders of images
    and pickles to a tuple of np.arrays
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('img_folder_path',
                        type=str, help='path to image folder')
    parser.add_argument('data_path',
                        type=str, help='path to data to be saved')
    parser.add_argument('labels_path',
                        type=str, help='path to labels to be saved')
    parser.add_argument("-w",
                        "--image_width",
                        type=int,
                        default=160,
                        help="width number (default=160)")
    parser.add_argument("-H",
                        "--image_height",
                        type=int,
                        default=90,
                        help="height number (default=90)")
    parser.add_argument("-c",
                        "--image_channels",
                        type=int,
                        default=3,
                        help="number of channels (default=3)")
    user_args = parser.parse_args()
    create_data_set_as_np_array(user_args.img_folder_path,
                                user_args.data_path,
                                user_args.labels_path,
                                user_args.image_width,
                                user_args.image_height,
                                user_args.image_channels)


if __name__ == '__main__':
    main()
