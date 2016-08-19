import argparse
import detector_functions

# system arguments - -g, -c, -fl,  -n, and -o
parser = argparse.ArgumentParser()

# make exclusive groups
input_group = parser.add_mutually_exclusive_group()
function_group = parser.add_mutually_exclusive_group()
# mutually exclusive system arguments -g and -c for using gap_detector
# function or ompare files_function
function_group.add_argument('-g', '--gapdetector', action='store_true',
                            help='Runs the gapdetector - requires input of'
                            + ' the files location and output name and orbit'
                            + ' time')
function_group.add_argument('-c', '--comparefiles', action='store_true',
                            help='Compares a filelist to the NASA filelist'
                            + ' and returns the days that have files missing'
                            + ' from the NASA list, requires two inputs,'
                            + ' and one output')
# mutually exclusive systems args -fl and -n for retrieving file input
# and output
# -fl for full fille addresses and names
# -n for shortcut using just the dataname ie 01kmCLay
input_group.add_argument('-fl', '--filelocations', nargs='+',
                         help='Full path and name of input and output files')
input_group.add_argument('-n', '--name',
                         help='Name of data to be checked - can only be'
                         + ' 01kmCLay, 05kmCLay, 05kmALay, and VFM')
# orbit time used for finding gaps, normally 5940 seconds
parser.add_argument('-o', '--orbittime',
                    type=int, help='The expected orbit time in seconds')
args = parser.parse_args()


# begin main program
print("Welcome to the Calipso Data Gap Detector")
# if no function was chosen in the terminal, quits program
if (not args.gapdetector) & (not args.comparefiles):
    print('-g or -c needed to run the program')
    print('add -h or --help to see command line arguments that can be used')

# gapdetector was chosen in sys args
elif(args.gapdetector):
    print('Gapdetector!')
    # initiallize blank variables that will be used as arguments for
    # gap _detector function
    data_location = ''
    gap_time = 0
    output_name = ''
    # no file names were recieved by sys args
    if (not args.filelocations) & (not args.name):
        data_location = input("Enter the path where the data is located\n")
        output_name = input("Enter the name you want for the output file\n")
    # assigns the direct values of the -fl strings into the function variables
    elif args.filelocations:
        data_location = args.filelocations[0]
        output_name = args.filelocations[1]
    # uses the keyword name to make a shortcut to the files location, and
    # creating a default output name
    elif args.name:
        data_location = '/mnt/oco2/calipso/' + args.name
        output_name = 'Results/' + args.name + '_gap_results'

    # asks for orbit time if none was given in sys args
    if not args.orbittime:
        gap_time = int(input("Enter the normal gap time in seconds:\n"))
    else:
        gap_time = args.orbittime

    # makes data list and checks for gaps
    print(data_location)
    data_list = detector_functions.create_filename_list_from_location(data_location)
    data_list.sort()
    detector_functions.check_gaps(data_list, output_name, gap_time)
    print("Finished gap check. See results at ", output_name)

# -c chosen in sys args
elif(args.comparefiles):
    print('Filecompare!')
    # initialize blank parameters that will be passed into the compare files
    # function
    data_location = ''
    NASA_files_loc = ''
    output_name = ''
    # nothing given through -fl or -n, asks for input from the user
    if (not args.filelocations) & (not args.name):
        data_location = input("Enter the path where the data is located\n")
        NASA_files_loc = input("Enter the path and name of the NASA_files text\n")
        output_name = input("Enter the name you want for the output file\n")
    # -fl, takes the sys arg and puts it directly into the file locs and
    # output name
    elif args.filelocations:
        data_location = args.filelocations[0]
        NASA_files_loc = args.filelocations[1]
        output_name = args.filelocations[2]
    # -name, takes the keyword name and uses it as the keyword in finding
    # the default location of the files, the NASA files, and output name
    elif args.name:
        data_location = '/mnt/oco2/calipso/' + args.name
        NASA_files_loc = 'NASAfilelists/' + args.name + '_all'
        output_name = 'Results/' + args.name + '_filecompare_results'

    # compares files and prints result
    detector_functions.compare_files(NASA_files_loc, data_location,
                                     output_name)
    print("Finished comparing files. See results at ", output_name)
