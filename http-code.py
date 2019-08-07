#!/usr/bin/python
# -*-Python-script-*-
#
#/**
# * Title    : http request status code
# * Auther   : by Alex, Lee
# * Created  : 06-11-2015
# * Modified : 06-18-2015
# * E-mail   : cine0831@gmail.com
#**/

import os
import sys
import socket
import time
import threading
import httplib
import optparse
import time
import datetime

start = time.time()

lock = threading.Lock()

def myThread(url,fds, argv):
    try:
        if argv.proto == 'http':
            httpconn = httplib.HTTPConnection(url, argv.port, timeout = 1)

        if argv.proto == 'https':
            httpconn = httplib.HTTPSConnection(url, argv.port, timeout = 1)

        httpconn.connect()
        httpconn.request(argv.method, argv.uri)
        reqstat = httpconn.getresponse()

        lock.acquire()
        output = "%4s %s %3s %3s %s%s" % (reqstat.status, reqstat.reason, '', '', url, '\n')
        print output,
        lock.release()
        httpconn.close()
    except (httplib.HTTPException, socket.error) as ex:
        lock.acquire()
        output = " Error          %s %20s%s" % (url, ex, '\n')
        print output,
        lock.release()

    fds.writelines(output)
    time.sleep(0)

    return


def parsing(argv):
    proto = ['http','https']
    method = ['GET','POST']

    cmd = optparse.OptionParser()
    cmd.usage = """
    %prog -l [filename] -p [port] -P [http | https] -m [GET | POST] -u [uri]
    """

    cmd.add_option('-l', action='store', type='string', dest='filename', help='file of server lists')
    cmd.add_option('-p', action='store', type='string', dest='port', help='destination port')
    cmd.add_option('-P', action='store', type='string', dest='proto', help='http or https')
    cmd.add_option('-m', action='store', type='string',dest='method', help='http method GET / POST')
    cmd.add_option('-u', action='store', type='string', dest='uri', default='/index.html', help='request uri | ex) /index.html'
)
    cmd.add_option('-v', action='store_true', dest='verbose', help='show version and exit')

    (options, args) = cmd.parse_args(argv)

    if len(args) == 1:
        cmd.print_help()
        sys.exit()

    if options.verbose == 1:
        print 'HTTP Code checker ver 0.2'
        sys.exit()

    if options.proto not in proto:
        cmd.print_help()
        sys.exit()

    if options.method not in method:
        cmd.print_help()
        sys.exit()

    return options


def run(argv):
    try:
        fd = open (argv.filename)
        fd_log = open ('result_log.txt', 'w')

        threads = []

        for line in fd:
            url = line.strip('\n')

            th = threading.Thread(target=myThread,args=(url,fd_log,argv))
            th.start()
            threads.append(th)

        for th in threads:
            th.join()

        fd_log.close
        fd.close

    except (IOError):
        print 'Can not open file'
    except (IndexError):
        print 'Index Error'


def main():
    opt = parsing(sys.argv[1:])
    run(opt)


if __name__ == "__main__":
    main()

print "Elapsed time: %s" % (time.time() - start)
