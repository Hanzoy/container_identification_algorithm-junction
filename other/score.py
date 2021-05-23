import os
if __name__ == '__main__':
    anno_file = open('annotation.txt','r+')
    resutl_file = open('result.txt','r+')
    anno_dict = {}
    right = 0
    for content in anno_file:
        anno_dict[content.split('\n')[0].split(' ',1)[0]] = content.split('\n')[0].split(' ',1)[1]

    for content in resutl_file:
        if(content.split('\n')[0].split(' ',1)[0]!=''):
            if(anno_dict[content.split('\n')[0].split(' ',1)[0]] == content.split('\n')[0].split(' ',1)[1]):
                print(content.split('\n')[0].split(' ', 1)[0])
                print(content.split('\n')[0].split(' ', 1)[1])
                right = right+1

    print('percent:{:.3%}',format(right/4000))