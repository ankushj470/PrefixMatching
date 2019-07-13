'''
Created on 13/07/2019

@author: Ankush Soni
@summary: FileProcessor class to process the input file
'''

import json
import os
class FileProcessor():
    """
    @summary: This class is responsible for file processing methods.
    """
    def __init__(self):
        pass

    def read_in_chunks(self,fp,size=10):
        """
        @summary: This is the generator method to read the specified chunk of data from file
        @param fp: File Pointer to read the file
        @param size: Chunk size to be read
        @return: Chunk of given size from the file
        """
        while True:
            chunk = fp.read(size)
            if not chunk:
                break
            yield chunk

    def create_outfile(self,testcase_dir,data):
        """
        @summary: This method creates the output file and insert the json data if it doesn't exist
        @param testcase_dir: testcase directory where file needs to be created
        @param data: data to be inserted in file
        @return: False if file already exists else True
        """
        if os.path.exists(os.path.abspath(testcase_dir + "/output.json")):
            return False
        out_fp = open(testcase_dir + "/output.json", "w")
        json.dump(data, out_fp)
        out_fp.close()
        return True

    def update_outfile(self,testcase_dir,data):
        """
        @summary: This method adds the data in the output file
        @param testcase_dir: testcase directory where output file exists
        @param data: data to be appended in file
        @return:
        """
        read_fp = open(testcase_dir + "/output.json", "r")
        file_data = json.load(read_fp)
        file_data.update(data)
        read_fp.close()

        write_fp = open(testcase_dir + "/output.json", 'w')
        json.dump(file_data,write_fp)
        write_fp.close()
        return 1


