# -*- coding: utf-8 -*-

from sys import exit
from struct import unpack
from os import path, makedirs
from zlib import decompress

class RAFLib:
    def __init__(self, path_raf, path_raf_data):
        try:
            self.raf = open(path_raf, "rb")
            self.raf_data = open(path_raf_data, "rb")
        except IOError, error:
            print error
            exit()
        self.le_data = lambda data: unpack("<I", data)[0]  # Interpret readed data in little-endian order
        # RAF Check
        self.magic_number = self.le_data(self.raf.read(4))
        if self.magic_number != 0x18be0ef0:
            print("[Error]%s is not a Riot Archive File(RAF)." % self.raf.name)
            exit()
        else:
            self.version = self.le_data(self.raf.read(4))  # File version
            self.manager_index = self.le_data(self.raf.read(4))  # Internal use number
            self.file_list_offset = self.le_data(self.raf.read(4))  # Offset where's stored file info
            self.path_list_offset = self.le_data(self.raf.read(4))  # Offset whre's stored path info
            print "[Info]%s is as Riot Archive File(RAF) %s." % (self.raf.name, self.version)

    def __get_file_entries(self):
        print "[Info]File List Offset starting at: %s. Storing..." % (hex(self.file_list_offset))
        number_of_entries = self.le_data(self.raf.read(4))
        # List of [file_path_hash, data_offset, data_size, path_list_index]
        file_entries_list = [[self.le_data(self.raf.read(4)) for file_entry in range(4)] for file_entries in range(number_of_entries)]
        return file_entries_list

    def __get_path_list_entries(self):
        print "{Info]Path List Offset starting at: %s. Storing..." % (hex(self.path_list_offset))
        path_list_size = self.le_data(self.raf.read(4))  # Total size of the path list (bytes)
        path_list_count = self.le_data(self.raf.read(4))  # Number of entries in path list
        # List of [path_offset, path_length]
        path_list_entries = [[self.le_data(self.raf.read(4)) for file_entry in range(2)] for file_entries in range(path_list_count)]
        return path_list_entries

    def unpack_content(self):
        file_entries = sorted(self.__get_file_entries(), key=lambda index: index[3]) #  Sort the file entries by path_index
        path_list_entries = self.__get_path_list_entries()
        print "[Info]Generating %s files." % len(path_list_entries)
        path_list = [self.raf.read(size) for relative_offset, size in path_list_entries] # Creating a list of paths to unpack files
        if len(path_list) == len(file_entries):
            for entry in range(len(path_list)):
                print "[Info]Generating: %s" % path.abspath(path_list[entry])
                the_path, filename = path.split(path_list[entry])
                #print path.split(path_list[1])
                if not the_path=="" and not path.exists(the_path): makedirs(the_path)  # Create directory if it doesn't exist
                actual_file = open(path_list[entry][0:-1], "w+")  # Create related file in path
                self.raf_data.seek(file_entries[entry][1], 0)  # Go to correct data_offset in raf.dat
                raf_data = self.raf_data.read(file_entries[entry][2]) # Read the data_size in raf.dat
                try: actual_file.write(decompress(raf_data))  # Trying to decompress using zlib and write in correct file
                except: actual_file.write(raf_data)  # If can't decompress write as is
        else:
            print "[Error]An error has ocurred..."
            sys.exit()
        self.raf.close()
        self.raf_data.close()