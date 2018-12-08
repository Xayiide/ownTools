import optparse
import subprocess
import queue
import time
import ipaddress
from threading import *

# updated

# Define the lock for the threads to share the screen
#printLock = Lock()

# Define the thread Queue
address_queue = queue.Queue() # Queue of addresses that haven't been pinged yet

# Define the max amount of threads to run
MAX_PINGERS = 4

# Define the timeout (in miliseconds)
TIMEOUT = 300

def testUp(address):
    isUp   = False
    count  = 0
    while (not isUp and count < 4):
        ping = subprocess.call(['fping', '-c', '1', '-t', str(TIMEOUT), address], \
                    stdout=subprocess.DEVNULL, \
                    stderr=subprocess.DEVNULL)
        if ping == 0:
            isUp = True
        else:
            count += 1
    return isUp

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
            exitStatus = testUp(address)
            if exitStatus:
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
        print("Example: %prog -n 192.168.50.0/24")
        exit(1)
    if thr != None:
        MAX_PINGERS = thr
    if tmo != None:
        TIMEOUT = tmo

    net = ipaddress.IPv4Network(net)


    for ip in list(net.hosts()):
        address_queue.put(str(ip))


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
