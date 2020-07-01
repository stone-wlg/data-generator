#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import datetime 
import json
from random import *
from getEquation import getEquation
from randomDate import randomDate
from collections import defaultdict
from dateutil.parser import parse
import sys
    
class DataGenerator(object):
    def __init__(self,rowFormat, rcnt):
        super(DataGenerator, self).__init__()
        self.lastTocken=defaultdict(lambda: None)
        self.row=defaultdict(lambda: None)
        self.rcnt=rcnt
        self.rowFormat=rowFormat
    def getHeader(self):
        headerString=""
        isUsed=False
        for i in self.rowFormat.keys():
            headerString=headerString+i+","
            isUsed=True
        if isUsed:
            headerString=headerString[:-1]
        return headerString    
    def generate(self,isHeader=True):
        if isHeader:
            print(self.getHeader())
        for i in range(1,self.rcnt+1):
            print(self.getRow())    

    def getRow(self):
        rowString=""
        del self.row
        self.row=defaultdict(lambda: None)
        isUsed=False
        for k in self.rowFormat.keys():
            theVal=self.getValue( k ) 
            self.row[k]=theVal
            if type(theVal) is datetime.datetime:
                theVal=theVal.strftime("%y-%m-%d %H:%M:%S")
            elif type(theVal) is float:
                theVal=str(theVal)
            rowString=rowString+ theVal+ ","
            isUsed=True
        if isUsed:
            rowString=rowString[:-1]
        return rowString

    def getValue(self, key):
        gType=self.rowFormat[key][0]
        gMethod=self.rowFormat[key][1]
        gMin=self.rowFormat[key][2]
        gMax=self.rowFormat[key][3]
        gGap=gMax
        gPrecision=self.rowFormat[key][4]
            
        if gMethod=="s":
            gStart=self.rowFormat[key][2]
            if self.lastTocken[key]:
                # if start
                lastVal=self.lastTocken[key]
                if gType=="dt":
                    theVal=lastVal+datetime.timedelta(days=gGap)
                    self.lastTocken[key]=theVal
                else:
                    theVal=lastVal+gGap
            else:
                if gType=="dt":
                    theVal=parse(gStart)
                else:
                    theVal=gStart
                self.lastTocken[key]=theVal
        elif gMethod=="r":
            if gType=="dt":
                    theVal=randomDate(parse(gMin),parse(gMax) )
            elif gType=="f":
                    gMinf=gMin*(10**gPrecision)
                    gMaxf=gMax*(10**gPrecision)
                    theVal=randint(gMinf,gMaxf)/(10**gPrecision)
            elif gType=="i":
                    theVal=randint(gMin,gMax)
        elif gMethod=="c":
            gEquation=self.rowFormat[key][5]

            eString=getEquation(gEquation,"self.row")
            # print(eString)
            theVal=eval(eString)
            theVal=int(theVal*(10**gPrecision))/(10**gPrecision)
        return theVal

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--num-of-files', dest='num_of_files', default=100, help='num of files')
    parser.add_argument('--num-of-records', dest='num_of_records', default=10000, help='num of records')
    parser.add_argument('--schema-file', dest='schema_file', default='./schema.json', help='schema file')
    parser.add_argument('--output-dir', dest='output_dir', default='./output', help='output dir')
    return parser.parse_args()

def open_schema(schema_file):
    schema = open(schema_file).read()
    return json.loads(schema)

if __name__ == '__main__':
    args = parse_args()
    schema = open_schema(args.schema_file)
    print(schema)

    # g=DataGenerator(rowFormat,rowCnt)
    # g.generate()
