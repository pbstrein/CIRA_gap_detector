from os import listdir
from os.path import isfile, join
from datetime import date
import datetime
"""GapFunctions v3.0
This module contains all the functions for the gapdetector script
This module reads the file names of calipso satelite data, and detects if there
    are any abnormal gaps in the data based on the satelite orbit
It reads the file name, parses the title to find the date and time of the
    satelite transmision, and compares it to the previous file, and checks
    whether it is  within what should be an orbit time. If there is a gap, it
    is noted and calculates how many data files should have been uploaded in
    the gap by finding the time in seconds of the gap, and calucating how many
    data files should be there by the orbit time in seconds. The orbit time
    and the file location are both given by the user.

Changelog v2.0
    This version of the code uses objects instead of many functions,
    simplyfing the code

Changelog v3.0
    Changed the ouput to display the dates when they had gaps, displayed the
    dates in order before the summary, and updated the summary to include how
    many dates needed to be updated. All information is written to an output
    file instead of being printed. Also removed unneeded functions like
    fing_avg_orbit.

    Added day_change, collect_gap_dates, and get_gap_dates_ordered functions to
    simply the check_gaps function
Changelog 4.0
    Added a function compare_files which compares the files in a folder to a 
    raw text file containing all the data files NASA has for that specific 
    project. Returns a result of all the days that have at least one file 
    missing from our folder and NASAs files.
    """


class CalipsoFile:
    """This object contains all the necessary information for parsing a given
       filename, containing the date of the file, the time, and the time in
       total seconds. Also contains functions for setting the time and date,
       retrieving the time and date as strings, and finding the days between
       two different
       dates.
    """

    def __init__(self):
        """everything is set to empty because empty objects will be used every now and
           then"""
        self.date = {}
        self.time = {}
        self.time_in_seconds = 0

    def is_empty(self):
        """checks if the current object does not contain any information"""
        if((not bool(self.date)) | (not bool(self.date))):
            return True
        else:
            return False

    def set_date(self, calipso_file_name):
        """sets the time from parsing a specific filename where the time is in the
           format year-month-day: ie 2016-07-04 is July 4th, 2016
           the date must be located at char 36-45 in the filename string"""
        index = calipso_file_name.find('V3-30.')
        self.date = {'year': calipso_file_name[(index + 6):(index + 10)],
                     'month': calipso_file_name[(index + 11):(index + 13)],
                     'day': calipso_file_name[(index + 14):(index + 16)]}

    def set_time(self, calipso_file_name):
        """sets the time from parsing a specific filename where time is in the
        format hour-minute-second: ie 16-15-04 is 4:15:04pm; must be located
        at char:47-54"""
        index = calipso_file_name.find('V3-30.')
        self.time = {'hour': calipso_file_name[(index + 17):(index + 19)],
                     'minute': calipso_file_name[(index + 20):(index + 22)],
                     'second': calipso_file_name[(index + 23):(index + 25)]}
        self.time_in_seconds = int(self.time['hour']) * 3600 + int(self.time['minute']) * 60 + int(self.time['second'])

    def get_time(self):
        """retrieves time and returns as a string hour-minute-second"""
        str_time = self.time['hour'] + "-" + self.time['minute'] + "-" + self.time['second']
        return str_time

    def get_date(self):
        """retrieves date and returns as a string in the format year-month-day
        """
        str_date = self.date['year'] + "-" + self.date['month'] + "-" + self.date['day']
        return str_date

    def get_date_normal(self):
        """retrieves date and returns as a string in the format month-day-year
        """
        str_normal_date =self.date['month'] + "-" + self.date['day'] + "-" + self.date['year']
        return str_normal_date

    def compare_date(self, comparing_date):
        """compares the objects date to another date, and sees if the comparing date
           is later, or higher, than the objects date
           returns false if current object is greater than the compared date
           returns true if current object is smaller than the compared date"""
        return (self.get_date() < comparing_date)

    def find_days_ahead(self, dict_comparing_date):
        """Finds the number of days between the self object and a given date
        dict"""
        if( (not bool(self.date)) | (not bool(dict_comparing_date))):
            return 0
        return (date(int(self.date['year']), int(self.date['month']),
                 int(self.date['day'])) -
            date(int(dict_comparing_date['year']), int(dict_comparing_date['month']),
                 int(dict_comparing_date['day']))).days


def create_list():
    """creates a list of all the strings in the current directory and returns
     the list"""
    file_list = [f for f in listdir("/Users/ciraweb/Documents/CIRA_Projects/calipso_gap_recognition/CalipsoData") if isfile(join("/Users/ciraweb/Documents/CIRA_Projects/calipso_gap_recognition/CalipsoData", f))]
    return file_list


def create_filename_list_from_location(location):
    """creates a list of all the file names in the given directory - excludes
    folders"""
    file_list = [f for f in listdir(location) if isfile(join(location, f))]
    return file_list


def import_NASA_files(file_loc):
    s = ''
    raw_list = []
    file_only_list = []
    with open(file_loc, 'r') as f:
        s = f.read()

    raw_list = s.split()
    for f in range(len(raw_list)):
        if 'CAL' in raw_list[f]:
            file_only_list.append(raw_list[f])
    return file_only_list


def day_change(prev_file, current_file):
    """ Checks the day change between the files, and returns the seconds of the
        previous day as a negative number of the seconds of how many days
        behind it was. If the previous day is not behind, it returns previous
        file's time
        in seconds"""
    new_time = prev_file.time_in_seconds
    """checks if there is a day change
    if current.time < prev. time or the date is just bigger"""
    if((current_file.get_time() < prev_file.get_time()) |
        (current_file.get_date() > prev_file.get_date())):
        """if it only a day or less a previous day, make prev_file 1 day smaller
        (86400 seconds) for checking for gaps"""
        if(current_file.find_days_ahead(prev_file.date) <= 0):
            new_time = prev_file.time_in_seconds - 86400
        else:
            """sets previous time back by how many days
            86400 seconds in a day * number of days"""
            new_time = prev_file.time_in_seconds - (86400 * current_file.find_days_ahead(prev_file.date))
    return new_time


def check_gap_dates(prev_file, current_file, current_gaps, gap_time):
    """Finds all the dates where there are data gaps and returns as a string
    """
    date = datetime.datetime(int(prev_file.date['year']),
                             int(prev_file.date['month']),
                             int(prev_file.date['day']))
    # prints to output the number of missing files, when, and where
    s = 'There are ' + str(current_gaps) + ' missing files from the following dates:\n'
    # check if prev_file date needs to be printed, and print if needed
    if(prev_file.time_in_seconds + gap_time < 86400):
        s += date.strftime('%m-%d-%Y\n')
    for f in range(current_file.find_days_ahead(prev_file.date) - 1):
        date += datetime.timedelta(days=1)
        s += date.strftime('%m-%d-%Y\n')
    if(current_file.time_in_seconds - gap_time > 0):
        date = datetime.datetime(int(current_file.date['year']),
                                 int(current_file.date['month']),
                                 int(current_file.date['day']))
        s += date.strftime('%m-%d-%Y\n')
    return s


def collect_gap_dates(prev_file, current_file, gap_time):
    """Finds all the dates, and returns them as a set
       Note: Similar to check_gap_dates, but returns a set instead of an string
       """
    dates_set = set()
    date = datetime.datetime(int(prev_file.date['year']),
                             int(prev_file.date['month']),
                             int(prev_file.date['day']))
    # add the date if there is a gap in the prev_file day
    if(prev_file.time_in_seconds + gap_time< 86400):
        dates_set.update([date.strftime('%Y-%m-%d')])
    # adds dates for all the days between prev_file and current_file
    for f in range(current_file.find_days_ahead(prev_file.date) - 1):
        date += datetime.timedelta(days=1)
        dates_set.update([date.strftime('%Y-%m-%d')])
    # adds the date for the current_file if there is a gap
    if(current_file.time_in_seconds - gap_time > 0):
        date = datetime.datetime(int(current_file.date['year']),
                                 int(current_file.date['month']),
                                 int(current_file.date['day']))
        dates_set.update([date.strftime('%Y-%m-%d')])
    return dates_set


def get_gap_dates_ordered(dates_set):
    """Returns a string with all the dates in order from a set"""
    temp_list = []
    temp_list = sorted(dates_set)
    s = ''
    s += "These are the dates that need downloading\n"

    # finds all the dates in the list, and adds spaces when it changes months
    for f in range(len(temp_list)):
        if(f != 0 & f != len(temp_list)):
            if((temp_list[f][5:7] > temp_list[f-1][5:]) & (temp_list[f][5:7] == temp_list[f][5:7])):                
                s += '\n'
        s += temp_list[f] + '\n'
    return s


def check_gaps(filename_list, output_name, gap_time_limit):
    """ This is the main function to check for gaps in the data.
    filename_list - the list of the filenames of the data that will be checked
    for
                    gaps
    gap_time_limit - the expected time in secons of a normal transmission from
                     the satelite any time between transmisions that are higher
                     than this number are counted as a gap

    The function uses a loops of the size of the filename list. Each loop it
    has two CalipsoFile Objects that contains the data from the current file in
    the loop, and the previous file in the loop. Beginning every instance of
    the
    loop, the datafile gets copied into the previous CalipsoFIle object, and
    the
    new CalipsoFile is read in from the filelist. It then checks if there has
    been
    a change of date, and checks the previous time to the current time. If the
    difference between the times is bigger than an orbit, or gap_time_limit, a
    gap
    is called, is noted, and counts how many files should have been in the gap.
    The files missing in the gap, the gap location, and the where the gap is in
    the files are all printed to the console and to a text document called
    output.
    At the end of the output file, is a summary of how many files are missing,
    and
    how many different locations or times there were gaps.
    """
    prev_file, current_file = CalipsoFile(), CalipsoFile()  # begin as empty
    total_gaps, total_locations = 0, 0
    # used for when making changes when the files change days
    prev_file_negative_time = 0
    used_dates = set()
    # open output file for writing results
    output_file = open(output_name, 'w')

    # loops through the whole file list
    for f in range(len(filename_list)):
        """skips the current file if it does not contain a keyword, meaning it
           is a faulty file or not a datafile we want to check"""
        if(filename_list[f].find('CAL') == -1):
            continue

        """transfers information for checking, makes new object based on current
        file, and sets the files data"""
        prev_file = current_file
        prev_file_negative_time = prev_file.time_in_seconds
        current_file = CalipsoFile()
        current_file.set_date(filename_list[f])
        current_file.set_time(filename_list[f])

        """skips current instance of loop if both previous and current files
        are not already readin from the file list"""
        if(prev_file.is_empty() | current_file.is_empty()):
            continue

        """checks if there was a day change, if so, returns negative number, if not,
        returns the prev_file time in seconds"""
        prev_file_negative_time = day_change(prev_file, current_file)

        """checks if there is a gap
        if the time between data files is bigger than the orbit/gap time"""
        if((current_file.time_in_seconds - prev_file_negative_time) > gap_time_limit):
            # calculates the datafiles that should have been in the gap
            gaps = (current_file.time_in_seconds - prev_file_negative_time) // gap_time_limit
            # for total gaps in the whole file list for summary
            total_gaps += gaps
            total_locations += 1 #adds for locations to be printed in summary

            # runs process to find all dates in gap, and returns it as a string
            output_string = check_gap_dates(prev_file, current_file, gaps,gap_time_limit)
            # finds all the dates, and puts it into the set for later usage
            used_dates.update( collect_gap_dates(prev_file, current_file, gap_time_limit))                           

            output_string += '\n'
            output_file.write(output_string)

    output_string = get_gap_dates_ordered(used_dates)

    output_string += '\n'
    output_file.write(output_string)
    """prints a summary of how many total files were missing in the list, and
    how many locations they were missing from in total"""
    output_string = 'Summary: \nTotal files missing: ' + str(total_gaps) +'\nDifferent locations: ' + str(total_locations) + '\nTotal dates that need downloading: ' + str(len(used_dates))
    output_file.write(output_string)
    output_file.close()


def compare_files(NASA_files_loc, CIRA_files_loc, output_file_name):
    """Compares a list of the NASA calpiso files to the CIRA calipso
    files, and prints to the output all the days that have 1+ file missing
    """
    CIRA_set = set()
    tmp_read = ''
    num_files_missing = 0
    dates_set = set()
    output_str = ''
    NASA_files = import_NASA_files(NASA_files_loc)

    CIRA_files = create_filename_list_from_location(CIRA_files_loc)

    # sort the lists
    NASA_files.sort()
    CIRA_files.sort()
    # puts CIRA_files into a set to make it easier to find matches
    # assumes that there are no duplicates in CIRA_files
    for i in range(len(CIRA_files)):
        if (CIRA_files[i].find('CAL') == -1):
            print(CIRA_files[i])
        temp_set = set([CIRA_files[i]])
        CIRA_set.update(temp_set)
    # compares each file in NASA list to the files in the given CIRA_list
    for i in range(len(NASA_files)):
        # NASA file is not in our CIRA file
        if NASA_files[i] not in CIRA_set:
            # creates Calipso files that can contain dates
            current_file = CalipsoFile()
            current_file.set_date(NASA_files[i])
            current_file.set_time(NASA_files[i])
            # makes the date and puts it into a set, no need for duplicates
            date = datetime.datetime(int(current_file.date['year']),
                                     int(current_file.date['month']),
                                     int(current_file.date['day']))
            dates_set.update([date.strftime('%Y-%m-%d')])

            num_files_missing += 1  # counter for files missing, used in summary
    # takes all the dates missing, and puts them into a string to be outputed
    output_str = get_gap_dates_ordered(dates_set)
    # summary of check
    summary = "Summary\n" + "NASA had " + str(len(NASA_files)) + " files\n" + "oco2 had " + str(len(CIRA_files))+ " files\n" + "Files found missing: " + str(num_files_missing) + "\n" +  "Total dates with files missing: " + str(len(dates_set))
    # writes to output
    with open(output_file_name, 'w') as file:
        file.write(output_str)
        file.write(summary)
