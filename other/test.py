if __name__ == '__main__':
    test = open('result_nofilter.txt','r+')
    print(test.readlines(1))
    test = open('result_nofilter.txt', 'r+')
    print(len(test.readlines()))
