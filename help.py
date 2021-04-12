import os


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



if __name__ == '__main__':
    print(getfile('path', 'to', 'file'))