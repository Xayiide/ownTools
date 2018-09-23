#!/usr/bin/env python3
# Help from:
# https://stackoverflow.com/questions/31348836/multiprocessing-acting-up-in-python-3


import sys, os
from multiprocessing import Pool
from zipfile import ZipFile

def init(protectedzip):
    """
    Every process will do this when created.
    This will allow them to keep their own ZipFile object.
    """
    global zfile
    zfile = ZipFile(open(protectedzip, 'rb'))

def check(password):
    """
    Tries the password and if it matches, the archive
    is unzipped.
    """
    assert password
    try:
        zfile.extractall(pwd=password.encode('utf-8'))
        return password
    except Exception as e:
        if e.args[0] != 'Bad password for file':
            raise RuntimeError(password)

def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: ./zipCracker.py <zipfile> <dictionary>\n")

    zipf = sys.argv[1]
    dict = sys.argv[2]

    with open(dict) as passFile, \
         Pool(processes=os.cpu_count()-1, initializer=init, initargs=[zipf]) as pool:
         # Open the dictionary file and create a Pool with the total number of CPUs-1
         # (number of CPUs-1 to avoid unresponsiveness)
         # This pool will contain processes that will call init(zipf) when created
        passwords = (line.strip('\n') for line in passFile) # strip the trailing \n
        passwords = filter(None, passwords) # erase empty passwords

        """
        The iterable is "passwords". It's chunked into chunks of 100 items each.
        It calls function "check" for every item in the iterable, and every process
        receives a chunk to process.
        check(password) will return the password if it opens the zipfile
        If it doesn't find a matching password, a message is printed
        """
        for password in pool.imap_unordered(check, passwords, chunksize=100):
            if password is not None:
                print("[+] Password found: " + password)
                print("[+] Extracting zip...")
                break
        else:
            sys.exit('Unable to find password')

if __name__ == '__main__':
    main()
