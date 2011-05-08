#-*- coding: UTF-8 -*-   

######################################################################
# Purpose:  get and sort clipping in kindle notes: "My Clippings.txt"
# Useage:   python get_clippings.py --help
# Version:  Initial Version by Alex(bin.c.chen@gmail.com)
######################################################################


import os
import re
import sys
import getopt
import struct
import shutil
import csv
import codecs
from string import *
from pprint import pprint
DEBUG = 0

    
class clippings:
    def __init__(self, ):
        self.file = "My Clippings.txt"
        self.clipping = []
        self.clip_desc = \
            [   'BOOK_TITLE', 
                'CLIP_LOC', 
                'CLIP_TYPE', 
                'CLIP_TIME', 
                'CLIP_TEXT' 
            ]
            
    def read(self, ):
        try:
            data = open(self.file, "r").read()
            print "\n-- Get clipping in file %s ! --" %self.file
        except:
            print "NO FILE: %s" %self.file
            sys.exit(3)
        
        notes = data.split('==========')
        notes_num = len(notes)
        for note_index, note in enumerate(notes):
            lines = note.split('\n')
            index = 0
            for i, line in enumerate(lines):
                if len(strip(line)):
                    index = i
                    break
            
            if index+2 > len(lines)-1:
                if DEBUG: print 'Invalid clips %d/%d: (%s)'  \
                    %(note_index, notes_num-1, note)
                continue
                
            title = lines[index]
            info = lines[index+1]   
            text = ' '.join(lines[index+2:])
            
            clip_type = info.split()[1]
            if 'Loc' in info:
                clip_loc = info.split()[3]
            else:
                clip_loc = info.split()[4]
            clip_loc = int(clip_loc.split('-')[0])
            
            clip_time = info.split('|')[1][9:]
                
            self.clipping.append( [title, clip_loc, clip_type, clip_time, text] )  

    def sort_key(self, item):  
        return (item[0], item[2], item[1], item[3])  

    def write(self, ):

        self.clipping.sort(key=self.sort_key)
        
        result_file_name = os.path.splitext(self.file)[0] + '.csv'
        
        try:
            fobj = open(result_file_name,'wb')
            fobj.write(codecs.BOM_UTF8)
            w = csv.writer(fobj) 
        except IOError:
            print "\n!! Please close file %s firstly !!" %result_file_name
            sys.exit(4)

        try:
            w.writerow( self.clip_desc )
            for rec in self.clipping:
                w.writerow(rec)
        finally:
            fobj.close()
            print "-- Save result in file %s ! --" %result_file_name

    def get(self, f):  
        if f: self.file = f
        
        self.read()
        self.write()
        
        
    def help(self, ):
        help_str = """
        Usage: get_clipping.py [args]                                        
        options:                                                             
           -f <file>............... specify <file> to analyze
           -d, --debug ............ show debug infornation                   
           -h, --help ............. show this help
        """
        print help_str                           



if __name__ == "__main__":
    
    file = ''
        
    clip = clippings()
    
    try:                                
        opts, args = getopt.getopt(sys.argv[1:], "hdf:", ["help", "debug"])
    except getopt.GetoptError:          
        clip.help()
        sys.exit(2)
                         
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            clip.help()
            sys.exit()  
                           
        elif opt in ("-d", "--debug"):
            DEBUG = 1
                    
        elif opt in ('-f'):
            file = arg
    
    clip.get(file)


