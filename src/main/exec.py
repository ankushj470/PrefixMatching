'''
Created on 13/07/2019

@author: Ankush Soni
dkfldksflds
@summary: This file is the execution file which processes the testcases and returns the output
'''

from input_processor import InputProcessor
from file_processor import FileProcessor
from config import config


if __name__ == '__main__':
    #List of testcases to be run
    testcases = ['testcase1/testcase1.txt','testcase2/testcase2.txt','testcase3/testcase3.txt']

    #This loop will run all the testcases and save the output as a json object in the output.json file and print the result
    for testcase in testcases:
        print "############## Running" + testcase + " ##############"
        query = raw_input("Input Query for "+  testcase+ ":" )
        testcase_dir = config.TESTCASES_DIR + testcase.split('/')[0]
        ip_obj = InputProcessor()
        #Check if the query already exists in the output file
        return_dict = ip_obj.query_already_exists(testcase_dir,query)

        #Processing the file and getting the output and storing it in output file
        if not return_dict:
            print "Processing File"
            return_dict =  ip_obj.process_input(config.TESTCASES_DIR+testcase,query)

            fp_obj = FileProcessor()
            if fp_obj.create_outfile(testcase_dir,return_dict):
                pass
            else:
                fp_obj.update_outfile(testcase_dir, return_dict)

        print return_dict[query]







