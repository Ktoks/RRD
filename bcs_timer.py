#!/usr/bin/env python3
from datetime import datetime
import argparse
date_format = '%Y-%m-%d %H:%M:%S' # left this here in case of changes, could use a list of different expected formats


def main(args) -> int:
    # open the in file in stdin
    fin = open(args.infile.name, 'r')

    time_lst = []
    process_list = []

    for line in fin:

        if "Start app_process: " in line:
            process_name, date, the_time = setup_str_lst(line)

            process_list.append("Start " + process_name)
            time_lst.append(date + ' ' + the_time)

        elif "End app_process: " in line:
            process_name, date, the_time = setup_str_lst(line)

            process_list.append("End " + process_name)
            time_lst.append(date + ' ' + the_time)

    fin.close()
    full_print(process_list, time_lst)
    return 0


def setup_str_lst(line) -> tuple:
    strlst = line.split()

    # find name of process
    process_name = strlst[2]

    # find date and time in string
    date = strlst[3][1:]
    the_time = strlst[4][:-2]
    return process_name, date, the_time


def full_print(process_lst: str, time_lst: str):
    start_table = {}
    final_table = {}
    out_string = ""

    for i in range(len(process_lst)):
        ind_process = process_lst[i].split()

        if "End" in ind_process:

			# get name of process
            process_name = ind_process[1]

            start_time = start_table[process_name]

            end_time = get_time_formatted(time_lst[i])

            del start_table[process_name]

            actual_time = end_time - start_time

            if process_name in final_table:
                final_table[process_name] += actual_time
            else:
                final_table[process_name] = actual_time

        else:
            process_name = ind_process[1]

            end_time = get_time_formatted(time_lst[i])

            start_table[process_name] = end_time

    for key in final_table:
        out_string += str(key) + ' ' + str(final_table[key]) + '\n'

    cust_out(out_string)


def get_time_formatted(time_lst: list) -> int:
    dt_obj = datetime.strptime(time_lst, date_format)
    return dt_obj.timestamp()


def cust_out(out_string: str):
    if args.outfile:
        fout = open(args.outfile.name, 'w')
        fout.write(out_string)
        fout.close()
    else:
        print(out_string)
        

# handle arguments:
parser = argparse.ArgumentParser(description="Returns the times of bcs projects from fulllog.txt files")
parser.add_argument(dest="infile", type=argparse.FileType('r'), help="fulllog.txt's full path")
parser.add_argument('-v', "--version", help="Show program version", action="version", version="BCS Timer Version 1.0")
parser.add_argument('-o', '--out', dest="outfile", nargs='?', type=argparse.FileType('w'), help="Save to file <path to file> ")
# parser.add_argument('-r', '--run', help="Time during run") # may or may not implement, seems unnecissary

args = parser.parse_args()

if __name__ == "__main__":
    main(args)
