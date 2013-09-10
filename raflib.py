# -*- coding: utf-8 -*-

import sys
import struct

class RAFLib:
    def __init__(self, path_raf, path_raf_data):
        try:
            self.raf = open(path_raf, "rb")
            self.raf_data = open(path_raf_data, "rb")
        except IOError, error:
            print error
            sys.exit()
        # Interpret readed data in little-endian order
        self.le_data = lambda data: struct.unpack("<I", data)[0]
        # RAF Check
        self.magic_number = self.le_data(self.raf.read(4))
        if self.magic_number != 0x18be0ef0:
            print("[Error]%s is not a Riot Archive File(RAF)." % self.raf.name)
            sys.exit()
        else:
            # Getting general information
            self.version = self.le_data(self.raf.read(4))
            self.manager_index = self.le_data(self.raf.read(4))
            self.file_list_offset = self.le_data(self.raf.read(4))  # Offset where's stored file info
            self.path_list_offset = self.le_data(self.raf.read(4))  # Offset whre's stored path info
            print "[Info]%s is as Riot Archive File %s." % (self.raf.name, self.version)

    def __get_file_entries(self):
        print "[Info]File List Offset starting at: %s. Storing..." % (hex(self.file_list_offset))
        # Working with the file entries
        file_list_entries = []
        number_of_entries = self.le_data(self.raf.read(4))
        for file_entry in range(number_of_entries):
            file_path_hash = self.le_data(self.raf.read(4))
            data_offset = self.le_data(self.raf.read(4))  # Offset of the file in raf.dat
            data_size = self.le_data(self.raf.read(4))  # Size of the file in raf.dat
            path_list_index = self.le_data(self.raf.read(4))
            # A list of tuples where each tuple is a file entry
            file_list_entries.append((file_path_hash, data_offset, data_size, path_list_index))
        return file_list_entries

    def __get_path_list_entries(self):
        print "{Info]Path List Offset starting at: %s. Storing..." % (hex(self.path_list_offset))
        # Working with the path list entries
        path_list_entries = []
        path_list_size = self.le_data(self.raf.read(4))  # Total size of the path list (bytes)
        path_list_count = self.le_data(self.raf.read(4))  # Number of entries in path list
        for path_entry in range(path_list_count):
            path_offset = self.le_data(self.raf.read(4))  # Number of bytes from the start of path list to start of the string
            path_length = self.le_data(self.raf.read(4))  # Size of the path string
            path_list_entries.append((path_offset, path_length))
        return path_list_entries

    def __get_paths_and_files(self):
        pass

    def unpack_content(self):
        file_entries = self.__get_file_entries()
        path_list_entries = self.__get_path_list_entries()
        print path_list_entries

        # code

        self.raf.close()
        self.raf_data.close()

if __name__ == "__main__":
    raf_tool = RAFLib("Archive_203379600.raf", "Archive_203379600.raf.dat")
    raf_tool.unpack_content()