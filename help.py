'''
has functions to help speed up the work

'''

import os
import pickle as pl


def getfile(*arg):
    '''
If file lives in .../MtgFi/a/b/c.txt, just write:

getfile("a","b","c.txt")

this returns the path: .../MtgFi/a/b/c.txt


On Windows, both give you the same result:


getfile(r"\a\b\c.txt")
getfile("a","b","c.txt")

    '''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    paths = [dir_path]
    for arguments in arg:
        paths.append(arguments)
    return(os.sep.join(paths))


def pickle(data, path):
    '''
pickle(data, 'path/to/pickled/file')


    '''

    with open(path, 'wb') as file_handler:
        pl.dump(data,file_handler)


def unpickle(path):
    '''
unpickle('path/to/pickled/file')

    '''
    with open(path, 'rb') as file_handler:
        return pl.load(file_handler)

if __name__ == '__main__':
    #print(getfile('path', 'to', 'file'))
    pickle(2,getfile('test','fine.txt'))
    print(3*unpickle(getfile('test', 'fine.txt')))