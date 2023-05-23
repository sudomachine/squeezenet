from torchvision import transforms
from PIL import Image

import torch, os

toTensor = transforms.ToTensor()

def loadImage(path, size=[], normalized=False, tensor_dim='3d'):
    '''
    get 
    image path file; 
    size of returned image: height and width as list;
    flag that means divide each pixel by 255 (if true);
    dimension of tensor is 3d if you want get it without batch dim (otherwise 4d)

    return pillow image and torch tensor of this image
    '''

    image = Image.open(path)

    if size != []:
        image = image.resize(size)

    tensor = toTensor(image)

    if not normalized:
        tensor = torch.mul(tensor, 255)

    if tensor_dim == '4d':
        tensor.unsqueeze_(0)

    return image, tensor

def loadImagesByCategories(images_dir, size=[], normalized=False):
    '''
    get 
    images directory with other categories directories; 
    size of returned image: height and width as list;
    flag that means divide each pixel by 255 (if true);
    
    return two dictionaries (images dict and tensors dict)
    1 dict: {"cat 1": [img1, ..., imgN1], ..., "cat m": [img1, ..., imgNM], ...}
    2 dict: {"cat 1": [tensor1, ..., tensorN1], ..., "cat m": [tensor1, ..., tensorNM], ...}
    '''

    images = dict()
    tensors = dict()

    for cat_dir in os.listdir(images_dir):
        
        images_list = []
        tensors_list = []

        for image_file in os.listdir(images_dir + cat_dir):

            full_img_path = images_dir + cat_dir + '/' + image_file

            image, tensor = loadImage(full_img_path, size, normalized)
            images_list.append(image)
            tensors_list.append(tensor)

        images[cat_dir] = images_list
        tensors[cat_dir] = torch.stack(tensors_list)

    return images, tensors

def loadImages(images_dir, size=[], normalized=False, shuffle=False):
    '''
    get 
    images directory with other categories directories; 
    size of returned image: height and width as list;
    flag that means divide each pixel by 255 (if true);
    flag thet means mixed images

    return 
    pillow images list;
    torch tensor with shape [batch, channel, height, width];
    categories list;
    categories names list
    '''

    images = []
    tensors = []
    categories = []
    category_id = 0
    cat_names = []

    for cat_dir in os.listdir(images_dir):

        cat_names.append(cat_dir)

        for image_file in os.listdir(images_dir + cat_dir):

            full_img_path = images_dir + cat_dir + '/' + image_file

            image, tensor = loadImage(full_img_path, size, normalized)

            images.append(image)
            tensors.append(tensor)
            categories.append(category_id)

    if (shuffle):
        pass

    tensors = torch.stack(tensors)


    return images, tensors, categories, cat_names



def splitDataset(tensors, images=None, training_set_percent=75):
    '''
    get batch of several input tensors;
    same batch of several input images;
    percent of training set (remaining percent is for test and valid sets (50/50)),
    for example 75-train, 12,5-test, 12,5-valid

    return 
    '''
