#!/usr/bin/env python3
# Author: Emmanuel Odeke <odeke@ualberta.ca>

import re
import sys

pyVersion = sys.hexversion/(1<<24)
if pyVersion < 3:
    byteFyer = bytes
else:
    byteFyer = lambda a: bytes(a, 'utf-8')

try:
    from router import acquireIndex, stepRange # Local module
except ImportError:
    from .router import acquireIndex, stepRange # Local module

intRegCompile = re.compile('^-?\d+\.?\d+', re.UNICODE)

class RouterManager:
    def __init__(self, hashBase, serverAddrList):
        if not hasattr(hashBase, '__divmod__'):
            raise Exception('HashBase must be a number')
        if not isinstance(serverAddrList, list):
            raise Exception('ServerAddrList must be a list')

        self.__hashBase = hashBase or 1
        self.__srvAddrList = serverAddrList

        self.__rangeTable = stepRange(self.__hashBase, len(self.__srvAddrList))
        self.__routingMap = dict(
            (self.__rangeTable[i], self.__srvAddrList[i]) for i in range(len(self.__rangeTable))
        )

    def getRoute(self, qHash):
        if hasattr(qHash, '__divmod__') or (qHash and intRegCompile.search(qHash)):
            qVal = int(qHash)
            return self.__routingMap.get(self.__resolveIndex(qVal), None)

    def getRoutingAddresses(self):
        return list(self.__routingMap.values())

    def __resolveIndex(self, index):
        qIndex = acquireIndex(self.__rangeTable, index % self.__hashBase)
        return self.__rangeTable[qIndex]

def main():
    rMgr = RouterManager(20, [
        '192.168.1.108', '192.168.1.110', '192.168.1.83', '192.168.1.64', '192.168.1.88'
    ])

    strList = [
        'http://yahoo.com', 'http://google.ca', 'http://cnn.com', 'http://time.com',
        'http://twitter.com', 'http://www.ualberta.ca'
    ]
    for item in strList:
        h = item.__hash__()
        print(item, rMgr.getRoute(h), h)

if __name__ == '__main__':
    main()
