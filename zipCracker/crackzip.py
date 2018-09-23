import zipfile
import optparse
from threading import Thread



def extractFile(zFile, password):
    try:
        zFile.extractall(pwd=password)
        print("[+] Found password: " + password + "\n")
    except Exception as e:
        print(e)


def main():
    parser = optparse.OptionParser("usage %prog " + \
            "-f <zipfile> -d <dictionary>")
    parser.add_option('-f', dest='zname', type='string',\
            help='specify zip file')
    parser.add_option('-d', dest='dname', type='string',\
            help='specify dictionary file')
    (options, args) = parser.parse_args()

    if (options.zname == None) or (options.dname == None):
        print(parser.usage)
        exit(1)
    else:
        zname = options.zname
        dname = options.dname



    zFile = zipfile.ZipFile(zname)
    with open(dname) as passFile:
        for line in passFile.readlines():
            password = line.strip('\n')
            t = Thread(target=extractFile, args=(zFile, password))
            t.start()

if __name__ == '__main__':
    main()
