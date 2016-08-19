#Calypso Gap Detector

### Summary
This program reads the files in a calypso data directory, parses all the data titles, and finds the days that have gaps in the data, and prints it out in the output. There are two modes - gap detector mode and compare files mode which essentially do the same thing, but in two different ways.

Gap detector reads only the data files, and based on the titles, sees if there is a gap greater than a user specified amount (typically 5940 seconds, about 98.5 minutes.) For all the gaps it finds, it outputs the days that have gaps, so we know which days need data to be redownloaded.

Compare files takes a list of all the calypso files that NASA has, and compares them to the files that in are in a user-specified folder. If there are files NASA has, but the local directory does not, then there is a missing data file that needs to be downloaded, and it outputs the day that was missing, to re-download that data.

————————————————————————————————————————————————————————————————————————————————————

### Program Requirements
To run, this program needs 3 things -
1. All of the calipso files in a  folder - the user specifies which folder the program will check. 
2. Command line prompts to select which program to run `-g` or `—-gapdetector` to run the gap detector program, or `-c` or `—-comparefiles` to run the NASA to Calipso File check
  - if using `-g`, you also need to use:
    -`fl` or `—-filelocations` to specify where the Calypso files are located followed by a space, and then the location and name of the results file
      - **NOTE**: you instead use `-n` or `—-name` for a shortcut, instead of giving a full file path, you may put in just the (i.e. 01kmCLay) which has a path automatically set up 	to select 01kmCLay files)
    - `-o` or `—-orbittime` to specify how long a orbit is (normally 5940 	seconds)
- if using `-c` you also need:
  - a text document with a list of the NASA files. The document does NOT  need to be pretty - it just needs to contain the files. The program filters out all other text or titles and grabs only the file titles
  -to use `-fl` or `—-filelocations` to specify where the Calipso files - needs to be followed with three file paths separated by spaces - the oco2 file directory, the file path to the NASA lists, and the path and title of the results file
    - for example, if I wanted to use 01kmClay, i would type	`-c -fl /mnt/oco2/calipso/01kmCLay [location of nasa files] results_01kmCLay`
  - OR use `-n` or `—-name` as a shortcut by only using the name of 	the files, for example 01kmCLay, that has it automatically pathed to both the oco2 files and the NASA file list and a title and location for the results file

————————————————————————————————————————————————————————————————————————————————————

### Example
For Gap Detector:
`python main.py -g /mnt/oco2/calipso/01kmCLay results_01kmCLay 5940 `
			OR 
`python main.py -g 01kmCLay 5940`

For Compare Files:
`python main.py -c /mnt/oco2/calipso/01kmCLay /peter/CalipsoFileDetector/NASAfilelists/01kmCLay_all results_01kmCLay`
			OR
`python main.py -c 01kmCLay`

- Note - there is no difference between python3 and python, use whatever you want
- Note - its much shorter to use the shortcut, but also less flexible

————————————————————————————————————————————————————————————————————————————————————

Output
The output is pretty much the same for both programs, only the titles are different. It first prints out a list of all the files that have gaps in them, then it creates a list of all the days that have files missing (and therefore need redownloading) and finishes up with a short summary of the program. The title for -g (unless changed by user) is results/[mission_name]_gap_results and for -c (unless changed by user) is results/[mission_name]_filecompare_results

————————————————————————————————————————————————————————————————————————————————————

### Tips and Warnings
1. Use -n to make the command line arguments much shorter and easier. It has all the file paths hardcoded for both input and output. However, if you change how things are bathed, or want to access something from a different location, you can still use -fl to give the specific file path of the input and output files
  - NOTE - you cannot use both -n and -fl
2. The command line arguments are not necessary, just helpful. If you do not use the command line arguments, then the computer will prompt you for all the information it needs to run.

————————————————————————————————————————————————————————————————————————————————————

### Command Line Arguments
- `-h` `—-help` - Command line help
- `-g` `—-gapdetector` - Runs the gap detector function
- `-c` `—-comparefiles` - Runs the program that compares the oco2 files to a list of the NASA files
`-fl` `—-filelocatoins` - A list of the input files, then the output files, if using `-g`, it needs to have 2 file paths, if using `-c`, it needs 3 file 			paths, 2 input and one output
`-n` `—-name` - A shortcut that only requires the mission type (i.e. 01kmCLay), that has the input and output paths automatically made based on the title
`-o` `—-orbittime` - use only for `-g`, it is the expected orbit time in seconds

————————————————————————————————————————————————————————————————————————————————————

### Default values
`-g`
```
with -n, data_location = /mnt/oco2/calipso/[user_input_calipso_name]
	 output_name = Results/[user_input_calipso_name]_gap_results
```
`-c`
```
with -n, data_location = /mnt/oco2/calipso/[user_input_calipso_name
	  NASA_files_loc = NASAfilelists/[user_input_calipso_name]_all
	  output_name = Results/[user_input_calipso_name]_filecompare_results
```
