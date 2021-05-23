import torch
import torch.backends.cudnn as cudnn
from torch.autograd import Variable
from PIL import Image
from collections import OrderedDict

import cv2
import numpy as np
from .craft_utils import getDetBoxes, adjustResultCoordinates
from .imgproc import resize_aspect_ratio, normalizeMeanVariance
from .craft import CRAFT

from PIL import Image
import torch
import torch.backends.cudnn as cudnn
import torch.utils.data
import torch.nn.functional as F
import torchvision.transforms as transforms
import numpy as np
from collections import OrderedDict

from .model import Model
from .utils import CTCLabelConverter
import math


def copyStateDict(state_dict):
    if list(state_dict.keys())[0].startswith("module"):
        start_idx = 1
    else:
        start_idx = 0
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = ".".join(k.split(".")[start_idx:])
        new_state_dict[name] = v
    return new_state_dict


def init_detector(trained_model, device='cpu'):
    net = CRAFT()
    if device == 'cpu':
        net.load_state_dict(copyStateDict(torch.load(trained_model, map_location=device)))
    else:
        net.load_state_dict(copyStateDict(torch.load(trained_model, map_location=device)))
        net = torch.nn.DataParallel(net).to(device)
        cudnn.benchmark = False

    net.eval()
    return net


def init_recognizer(input_channel, output_channel, hidden_size, character, \
                        separator_list, dict_list, model_path, device='cpu'):

        converter = CTCLabelConverter(character, separator_list, dict_list)
        num_class = len(converter.character)
        model = Model(input_channel, output_channel, hidden_size, num_class)

        if device == 'cpu':
            state_dict = torch.load(model_path, map_location=device)
            new_state_dict = OrderedDict()
            for key, value in state_dict.items():
                new_key = key[7:]
                new_state_dict[new_key] = value
            model.load_state_dict(new_state_dict)
        else:
            import time
            # time_reg = time.time()

            model = torch.nn.DataParallel(model).to(device)
            model.load_state_dict(torch.load(model_path, map_location=device))

            # print("regor耗时：" + str(time.time() - time_reg))
        return model, converter