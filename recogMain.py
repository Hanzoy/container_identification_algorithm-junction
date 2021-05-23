import sys
import os
import cv2
import string
import other.guolv22
from time import *
import model.EAST.eval as eval
from numba import cuda
import tensorflow as tf
import shutil
# from model.OCR.init import init_detector, init_recognizer


tf.app.flags.DEFINE_string('test_data_path', 'test_data', '') # 检测图片地址
tf.app.flags.DEFINE_string('gpu_list', '0', '')
tf.app.flags.DEFINE_string('checkpoint_path', 'model//EAST//model', '')
tf.app.flags.DEFINE_string('output_dir', 'model//EAST//out', '')
tf.app.flags.DEFINE_bool('no_write_images', False, 'do not write images')

if __name__ == '__main__':
    time1 = time()
    shutil.rmtree('model//EAST//out')
    # 递归删除目录下所有文件
    os.mkdir('model//EAST//out')

    # test_path = str(sys.argv[1])
    # tf.app.flags.DEFINE_string('test_data_path', test_path, '')
    time_eval = time()
    # east输出
    eval.main()

    print("eval耗时：" + str(time() - time_eval))
    # ocr
    east_out_path = 'model//EAST//out'
    cuda.select_device(0)
    cuda.close()

    time_ocr = time()
    # time_dec = time()

    from model.OCR.init import init_detector, init_recognizer

    detector = init_detector(r'model/OCR/model//model\craft_mlt_25k.pth', 'cuda')

    # print("detector耗时：" + str(time() - time_dec))
    # time_reg = time()

    character = '0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk' \
                'lmnopqrstuvwxyzÀÁÂÃÄÅÆÇÈÉÊËÍÎÑÒÓÔÕÖØÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿąęĮįıŁłŒœŠšųŽž'
    separator_list = {}
    dict_list = {'en': 'D:\\集装箱\\集装箱\\model\\OCR\\dict\\en_char.txt'}
    model_path = r'model/OCR/model//model\latin.pth'
    recognizer, converter = init_recognizer(1, 512, 512, character, separator_list, dict_list, model_path, 'cuda')

    # print("recognizer耗时：" + str(time() - time_reg))

    import model.OCR.ocr as ocr
    # my_ocr = ocr.Ocr() # 调用OCR
    my_ocr = ocr.Ocr(detector_model=detector, recognizer_model=recognizer, converter_model=converter)  # 调用OCR

    # eval.main()

    print("ocr耗时：" + str(time() - time_ocr))

    picture_list = os.listdir(east_out_path)
    # img_test = cv2.imread(east_out_path+'//'+picture_list[0]) # 读取图片

    # print("test结果如下"+str(my_ocr.get_result(img_test)))
    result = "" # 输出

    for a in picture_list: # 对每张图片进行ocr识别
        if a.endswith('.jpg') or a.endswith('.png'):
            # print(a)
            filter_result = a + '\n' + str(
                my_ocr.get_result(east_out_path + '//' + a, allowlist='ABCDEFGHIJKLMNOPQRSTWVUXYZ0123456789',
                                  canvas_size=2000)) + '\n'
            result = result + filter_result
            # print(a)
            print(filter_result)

    # for index,a in enumerate(picture_list):

    # for i in range(len(picture_list)):
    #     num = os.path.basename(picture_list[0]).split()
    #     a = str(i+1)+os.path.basename(picture_list[0])[1:]
    #     if a.endswith('.jpg') or a.endswith('.png'):
    #         filter_result = a+'\n'+str(my_ocr.get_result(east_out_path+'//'+a,allowlist='ABCDEFGHIJKLMNOPQRSTWVUXYZ0123456789',canvas_size=2000))+'\n'
    #         result = result + filter_result
    #         print(a)
    #         print(filter_result)
    fh = open('other/result_nofilter.txt', 'w', encoding='utf-8')
    fh.write(str(result))
    order_dict = {}
    fh.close()

    other.guolv22.chuMain()
    # inner print filtered result

    print("耗时间：" + str(time() - time1))