import sys, argparse, threading
from random import randint, seed, choice
from src.argparser import *

parser = ArgumentParser(
    width=100, description='''IPGen, a simple tool to create random IPv4 and IPv6 lists, with speed and customizability in mind''',
    epilog='''Copyright (c) 2022 Nexus/Nexuzzzz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
''', 
    argument_default=argparse.SUPPRESS, 
    allow_abbrev=False
)

# add arguments
parser.add_argument('-a',       '--amount',          action='store',      dest='amount',        metavar='amount',           type=int,  help='Amount of IP\'s to generate', default=500)
parser.add_argument('-t',       '--threads',         action='store',      dest='threads',       metavar='amount',           type=int,  help='Amount of threads to use', default=100)
parser.add_argument('-s',       '--seed',            action='store',      dest='seed',          metavar='seed',             type=str or int or float or bytes or bytearray,  help='Seed to use when initializing the Random module', default=None)
parser.add_argument('-o',       '--output',          action='store',      dest='output',        metavar='file',             type=str,  help='Output file to write results to', default='output.txt')
parser.add_argument('-b',       '--buffer',          action='store',      dest='buffer',        metavar='file buffer',      type=int,  help='Buffer size to use when writing IP\'s to output file', default=16*1024*1024)
parser.add_argument('-q',       '--quiet',           action='store_true', dest='quiet',                                                help='Silence the output', default=False)
parser.add_argument('-v',       '--verbose',         action='store_true', dest='verbose',                                              help='Show extra output', default=False)
parser.add_argument('-d',       '--duplicates',      action='store_true', dest='allow_dupes',                                          help='Allow duplicates', default=False)
parser.add_argument('-l',       '--lock',            action='store_true', dest='use_lock',                                             help='Use a thread lock when modifying variables. Can decrease performance.', default=False)
parser.add_argument('-4',       '--ipv4',            action='store_true', dest='gen_ipv4',                                             help='Generate IPv4 addresses', default=False)
parser.add_argument('-6',       '--ipv6',            action='store_true', dest='gen_ipv6',                                             help='Generate IPv6 addresses', default=False)
args = vars(parser.parse_args()) # parse the arguments

if len(sys.argv)== 1: # no arguments passed, show help menu
    sys.exit(f'Syntax: python3 {sys.argv[0]} -a amount\nUse "--help" to see all other arguments.')

# initialize the Random module
seed(args['seed'])

lock = threading.Lock() # lock for accessing objects
ips = [] # ip list
i = 0 # counter

def pprint(msg) -> None:
    '''
    pprint(message) -> None

    Helper function to display messages

    :returns None: Nothing
    '''

    if not args['quiet']:
        print(f'[IPGEN] {msg}')

def make_ipv4() -> str:
    '''
    make_ipv4() -> str

    Creates a random IPv4 address

    :returns str: The IP address
    '''

    return '.'.join([str(randint(1,255)) for _ in range(4)])

def make_ipv6() -> str:
    '''
    make_ipv6() -> str

    Creates a random IPv6 address

    :returns str: The IP address
    '''
    return ':'.join('{:x}'.format(randint(0, 2**16 - 1)) for _ in range(8))

def generator(threadid) -> None:
    '''
    generator(thread id) -> None

    Worker function which generates the IP address, and adds it to the list

    :param threadid str: Worker ID
    :returns None: Nothing
    '''

    global i

    while 1: 
        if i == args['amount']:
            break

        if args['use_lock']: lock.acquire()
        i+=1 # append one
        if args['use_lock']: lock.release()

        ip = ''
        if args['gen_ipv4'] and args['gen_ipv6']: ip = choice([make_ipv4(), make_ipv6()]) # if the user wants both IP v4 and v6, pick a random one
        elif args['gen_ipv4']: ip = make_ipv4() # generate a random IPv4 address
        elif args['gen_ipv6']: ip = make_ipv6() # generate a random IPv6 address
        else: ip = make_ipv4() # if no option has been specified, just make a random IPv4 address

        if not ip:
            pprint(f'[THREAD-{threadid}] Failed to make IP-{str(i)}')
            return # exit the function

        pprint(f'[THREAD-{threadid}] Generated IP-{str(i)}: {ip}')

        if args['allow_dupes']: # don't bother checking for duplicates
            if args['use_lock']: lock.acquire()
            ips.append(ip) # append IP to list
            if args['use_lock']: lock.release()

        else:
            if not ip in ips: # if the IP is NOT in the list already
                if args['use_lock']: lock.acquire()
                ips.append(ip)
                if args['use_lock']: lock.release()


    if args['verbose']:
        pprint(f'[THREAD-{threadid}] Finished.')

if __name__ == '__main__':
    pprint(f'Creating threads')

    threadbox = []
    for _id in range(0, args['threads']):
        _id+=1 # append one

        kaboom = threading.Thread(target=generator, args=(str(_id),))
        threadbox.append(kaboom)

        if args['verbose']:
            pprint(f'Thread-{str(_id)} started')

        kaboom.start() # start thread

    pprint(f'Waiting for threads to finish...')
    for thread in threadbox: # wait for all threads to finish their bizznizz
        thread.join()

    pprint(f'All threads finished, writing generated IP\'s to "{args["output"]}"')
    with open(args['output'], 'w+', buffering=args['buffer']) as fd: # and finally, write all generated ips to a file
        [fd.write(f'{ip}\n') for ip in ips]
    
    pprint(f'Done, seed used: {"None, so seed is unknown." if not args["seed"] else args["seed"]}')
