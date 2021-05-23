import os
from PIL import Image
from remake import east_pred
# cmdr = os.system("chdir")

file_name = '90.jpg'

# im_fn_list = '..//..//test_data//' + file_name
#
#
# im = Image.open(im_fn_list).convert('RGB')
#
# print(im)

east_pred(file_name)
