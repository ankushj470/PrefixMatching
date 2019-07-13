'''
Created on 13/07/2019

@author: Ankush Soni
@summary: InputProcessor class to process the input
'''

import heapq
import os
import json
from config import config
from file_processor import FileProcessor
from exception_util import RequestParseException

class InputProcessor():
    """
    @summary: This class is responsible for processing the input
    """

    def __init__(self):
        self.result_list =[]
        heapq.heapify(self.result_list)
        self.counter = 0

    def process_input(self,f_name,query):
        """
        @summary: This method process the input file using FileProcessor class and returns the output
        @param f_name:file name to be processed
        @param query:query to be searched
        @return: Dictionary with query as the key and list of top found elems as the value
        """
        fp_obj = FileProcessor()
        data_leftover = ""

        with open(f_name) as fp:
            for chunk in fp_obj.read_in_chunks(fp, config.CHUNK_SIZE):
                curr_list,data_leftover = self.convert_to_list((data_leftover + chunk).strip('[]'))
                self.prefix_match(curr_list,query)

        return self.convert_to_dict(self.result_list,query)

    def query_already_exists(self,dir_name,query):
        """
        @summary: This method checks if the query has searched in the past and returns the output if exists
        @param dir_name:Output file directory
        @param query:query to be searched
        @return: Dictionary with query as the key and list of top found elems as the value or 0 if doesn't exists
        """
        file_path = dir_name + "/output.json"
        if os.path.exists(os.path.abspath(file_path)):
            out_fp = open(file_path, "r")
            data = json.load(out_fp)
            if query in data.keys():
                print "Found in Output File"
                return {query:data[query]}

        return 0



    def convert_to_dict(self,input_list,query):
        """
        @summary: This method converts the list of tuples into dictionary
        @param input_list:list of tuples to be converted
        @param query:query to be the key of dictionary
        @return: Dictionary with query as the key and list of top found elems as the value
        """
        result_dict = {query:[]}
        for elem in sorted(input_list, key=lambda x: x[0], reverse=True):
            result_dict[query].append(elem[1])

        return result_dict


    def convert_to_list(self,s):
        """
        @summary: This method converts the string into list of tuples
        @param s: string to be converted
        @return: list of tuples
        """
        try:
            if '(' in s and  ')' in s:
                start_index = s.index('(')
                end_index = s.rindex(')')
                curr_str = s[start_index:end_index+1]
                data_leftover = s[end_index+1:]

            else:
                curr_str = ''
                data_leftover = s


        except:
            raise RequestParseException

        curr_list = eval('[' + curr_str + ']') if curr_str else []
        return curr_list,data_leftover


    def prefix_match(self,curr_list,query):
        """
        @summary: This method maintains the heap of top elements whos Name starts with the query
        @param curr_list: List of tuples containing names and scores
        @param query:query to be matched with
        @return: updates the heap
        """
        for tup in curr_list:
            for word in tup[config.NAME_INDEX].split('_'):
                if word.startswith(query):
                    elem = tup[::-1]
                    if self.counter< config.COUNT:
                        heapq.heappush(self.result_list,elem)
                        self.counter+=1

                    else:
                        heapq.heappushpop(self.result_list,elem)


