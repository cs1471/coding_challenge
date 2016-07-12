import sys
import getopt
# import pdb
from parse_file import Parser

def main(argv):
    try:
        fileImport = Parser()  # initialize parser class object
        opts, args = getopt.getopt(argv, "i:o:")  # check for command line options where i = input file and o = outputfile
        fileImport.setOptions(args, opts) #pass to parser function 

    except getopt.GetoptError:
        print("There is an error reading your file in")
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])