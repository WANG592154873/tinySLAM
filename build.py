#!/usr/bin/python
# coding:utf-8
from os import listdir, system
import os
import sys
goFile = []
for i in listdir('src'):
    if 'go' in i.split('.')[-1]:
        goFile.append(i)
os.chdir('src')
if len(sys.argv) == 1:
    print(u"默认使用本地编译，加上arm参数则使用arm-openwrt-linux-g++交叉编译")
    system('cd uart && ./build.sh')  # 编译静态库
    system('GOPATH=`pwd`/../ go build '+' '.join(goFile))
elif sys.argv[1] == 'arm':
    print(u"使用arm-openwrt-linux-g++交叉编译")
    system('''
cd uart && 
rm *.so &&
arm-openwrt-linux-g++ -c -fPIC READ_UART.cpp &&
arm-openwrt-linux-g++ -c -fPIC serial.cpp &&
arm-openwrt-linux-g++ -c -fPIC bridge.cpp &&
arm-openwrt-linux-ar -crs libctest.so READ_UART.o serial.o bridge.o &&
rm *.o
''')
    system('GOPATH=`pwd`/../ GOARCH=arm CGO_ENABLED=1 CXX="arm-openwrt-linux-g++" CC="arm-openwrt-linux-gcc" go build ' + ' '.join(goFile) +' ' + ' '.join(sys.argv[2:]))
system('mv main ../bin')
