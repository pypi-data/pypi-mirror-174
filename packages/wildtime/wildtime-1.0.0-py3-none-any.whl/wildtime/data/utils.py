import os
import pickle
from enum import Enum

import gdown
import numpy as np
import torch
from torch import nn
from torchvision.transforms import transforms
from transformers import DistilBertTokenizer


# from data.MIMIC.get_stay_dict import get_stay_dict
# from data.MIMIC.preprocess import preprocess_MIMIC

class Mode(Enum):
    TRAIN = 0
    TEST_ID = 1
    TEST_OOD = 2

    def __eq__(self, another):
        # return hasattr(another, 'data') and self.data == another.data
        return True

    def __hash__(self):
        # return hash(self.data)
        return hash(0)
def initialize_distilbert_transform(max_token_length):
    """Adapted from the Wilds library, available at: https://github.com/p-lambda/wilds"""
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    def transform(text):
        tokens = tokenizer(
            text,
            padding='max_length',
            truncation=True,
            max_length=max_token_length,
            return_tensors='pt')
        x = torch.stack((tokens['input_ids'], tokens['attention_mask']), dim=2)
        x = torch.squeeze(x, dim=0) # First shape dim is always 1
        return x
    return transform

class GaussianBlur(object):
    """blur a single image on CPU"""
    def __init__(self, kernel_size):
        radias = kernel_size // 2
        kernel_size = radias * 2 + 1
        self.blur_h = nn.Conv2d(3, 3, kernel_size=(kernel_size, 1),
                                stride=1, padding=0, bias=False, groups=3)
        self.blur_v = nn.Conv2d(3, 3, kernel_size=(1, kernel_size),
                                stride=1, padding=0, bias=False, groups=3)
        self.k = kernel_size
        self.r = radias

        self.blur = nn.Sequential(
            nn.ReflectionPad2d(radias),
            self.blur_h,
            self.blur_v
        )

        self.pil_to_tensor = transforms.ToTensor()
        self.tensor_to_pil = transforms.ToPILImage()

    def __call__(self, img):
        img = self.pil_to_tensor(img).unsqueeze(0)

        sigma = np.random.uniform(0.1, 2.0)
        x = np.arange(-self.r, self.r + 1)
        x = np.exp(-np.power(x, 2) / (2 * sigma * sigma))
        x = x / x.sum()
        x = torch.from_numpy(x).view(1, -1).repeat(3, 1)

        self.blur_h.weight.data.copy_(x.view(3, 1, self.k, 1))
        self.blur_v.weight.data.copy_(x.view(3, 1, 1, self.k))

        with torch.no_grad():
            img = self.blur(img)
            img = img.squeeze()

        img = self.tensor_to_pil(img)

        return img

def get_simclr_pipeline_transform(size, s=1):
    """Return a set of data augmentation transformations as described in the SimCLR paper."""
    color_jitter = transforms.ColorJitter(0.8 * s, 0.8 * s, 0.8 * s, 0.2 * s)
    data_transforms = transforms.Compose([transforms.RandomResizedCrop(size=size),
                                              transforms.RandomHorizontalFlip(),
                                              transforms.RandomApply([color_jitter], p=0.8),
                                              transforms.RandomGrayscale(p=0.2),
                                              GaussianBlur(kernel_size=int(0.1 * size)),
                                              transforms.ToTensor()])
    return data_transforms

class ContrastiveLearningViewGenerator(object):
    """Take two random crops of one image as the query and key."""

    def __init__(self, base_transform, n_views=2):
        self.base_transform = base_transform
        self.n_views = n_views

    def __call__(self, x):
        return [self.base_transform(x) for i in range(self.n_views)]

def download_gdrive(url, save_path, is_folder):
    """ Download the preprocessed data from Google Drive. """
    if not is_folder:
        gdown.download(url=url, output=save_path, quiet=False)
    else:
        gdown.download_folder(url=url, output=save_path, quiet=False)


def download_arxiv(data_dir):
    download_gdrive(
        url='https://drive.google.com/u/0/uc?id=1H5xzHHgXl8GOMonkb6ojye-Y2yIp436V&export=download',
        save_path=os.path.join(data_dir, 'arxiv.pkl'),
        is_folder=False
    )


def download_drug(data_dir):
    download_gdrive(
        url='https://drive.google.com/drive/folders/1796kUMCTs8r0dnQjBiLt7YTm6ZtZAd3f?usp=sharing',
        save_path=os.path.join(data_dir, 'Drug-BA'),
        is_folder=True
    )
    download_gdrive(
        url='https://drive.google.com/u/0/uc?id=179g3KTOG2mBTZzF6lxG6iodNp8xmdxpg&export=download',
        save_path=os.path.join(data_dir, 'drug_preprocessed.pkl'),
        is_folder=False
    )


def download_fmow(data_dir):
    download_gdrive(
        url='https://drive.google.com/u/0/uc?id=1s_xtf2M5EC7vIFhNv_OulxZkNvrVwIm3&export=download',
        save_path=os.path.join(data_dir, 'fmow.pkl'),
        is_folder=False
    )


def download_huffpost(data_dir):
    download_gdrive(
        url='https://drive.google.com/u/0/uc?id=1jKqbfPx69EPK_fjgU9RLuExToUg7rwIY&export=download',
        save_path=os.path.join(data_dir, 'huffpost.pkl'),
        is_folder=False
    )


# def download_mimic(args, data_dir):
#     if not os.path.exists('./Data/mimic_stay_dict.pkl'):
#         get_stay_dict(data_dir)
#     data = pickle.load(open('./Data/mimic_stay_dict.pkl', 'rb'))
#     preprocess_MIMIC(data, 'readmission', args)
#     preprocess_MIMIC(data, 'mortality', args)


def download_precipitation(data_dir):
    download_gdrive(
        url='https://drive.google.com/u/0/uc?id=19BnZT3VxYEtNIEj0fN76UcGG2GP2JP65&export=download',
        save_path=os.path.join(data_dir, 'weather.pkl'),
        is_folder=False
    )


def download_yearbook(data_dir):
    download_gdrive(
        url='https://drive.google.com/u/0/uc?id=1mPpxoX2y2oijOvW1ymiHEYd7oMu2vVRb&export=download',
        save_path=os.path.join(data_dir, 'yearbook.pkl'),
        is_folder=False
    )


def download_detection(data_dir, dataset_name):
    if os.path.isfile(data_dir):
        raise RuntimeError('the save path should be a dir')
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    if os.path.isfile(os.path.join(data_dir, dataset_name)):
        pass
    else:
        if 'arxiv' in dataset_name:
            download_arxiv(data_dir)
        elif 'drug' in dataset_name:
            download_drug(data_dir)
        elif 'fmow' in dataset_name:
            download_fmow(data_dir)
        elif 'huffpost' in dataset_name:
            download_huffpost(data_dir)
        elif 'precipitation' in dataset_name:
            download_precipitation(data_dir)
        elif 'yearbook' in dataset_name:
            download_yearbook(data_dir)
        else:
            raise RuntimeError('wrong dataset name')
