import optparse
import subprocess
import queue
import time
from threading import *


# Define the lock for the threads to share the screen
#printLock = Lock()

# Define the thread Queue
pingers_queue = queue.Queue() # Max amount of threads in the Queue is 8 (as 8 is the # of cores my cpu has)
address_queue = queue.Queue() # Queue of addresses that haven't been pinged yet

# Define the max amount of threads to run
MAX_PINGERS = 4

# Define the timeout (in miliseconds)
TIMEOUT = 300


def IPscan(toPingQueue):
    """
    Pings to IPs on the ping Queue.
    Uncomment the printLock lines to see how a lock works (slows down A LOT the scan)
    """
    global TIMEOUT

    try:
#       printLock.acquire()
        while True:
            address = toPingQueue.get_nowait() # Get an address to ping
            exitStatus = subprocess.call(['fping', '-c', '1', '-t', str(TIMEOUT), address], \
                    stdout=subprocess.DEVNULL, \
                    stderr=subprocess.DEVNULL)
            if exitStatus == 0:
                print("[+]", address, "up")
#           else:
#               print("[-]", address, "seems down")

    except queue.Empty:
        pass
#       printLock.acquire()
#       print("[-] No more addresses to ping.") # Prints out once for every thread

    
#   finally:
#       printLock.release()

def main():
    global MAX_PINGERS
    global TIMEOUT

    parser = optparse.OptionParser('Usage: %prog -n <network> -t <threads> ' + \
            '-w <timeout>')
    parser.add_option('-n', dest='network', type='string', help='specify target network')
    parser.add_option('-t', dest='threads', type='int', help='specify number of threads [default: 4]')
    parser.add_option('-w', dest='timeout', type='int', help='specify the timeout (ms) [default: 300]')

    (options, args) = parser.parse_args()


    net = options.network
    thr = options.threads
    tmo = options.timeout
    if net == None:
        print(parser.usage)
        print("Example: %prog -n 192.168.50")
        exit(1)
    if thr != None:
        MAX_PINGERS = thr
    if tmo != None:
        TIMEOUT = tmo

    for host in range(1, 255):
        address_queue.put(net + "." + str(host))


    pingers = [Thread(target=IPscan, args=(address_queue,)) for _ in range(MAX_PINGERS)]

    start_time = time.time()
    for pinger in pingers:
        pinger.start()
    
    for pinger in pingers:
        pinger.join()

    finish_time = time.time()
    print("Duration of the scan:", finish_time - start_time)


if __name__ == '__main__':
    main()
    
