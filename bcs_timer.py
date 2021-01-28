#!/usr/bin/env python3
from datetime import datetime
import argparse


def main(args) -> int:
    # open the in file in stdin
    fin = open(args.INFILE.name, 'r')

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
    total_time = 0

    for i in range(len(process_lst)):
        ind_process = process_lst[i].split()

        if "End" in ind_process:

            # get name of process
            process_name = ind_process[1]

            start_time = start_table[process_name]

            end_time = get_time_formatted(time_lst[i])

            del start_table[process_name]

            actual_time = end_time - start_time

            total_time += actual_time

            if process_name in final_table:
                final_table[process_name] += actual_time
            else:
                final_table[process_name] = actual_time

        else:
            process_name = ind_process[1]

            end_time = get_time_formatted(time_lst[i])

            start_table[process_name] = end_time
    final_table["total"] = total_time

    for key in final_table:
        final_table[key] = scale_time(final_table[key])
        out_string += str(key) + ' ' + str(final_table[key]) + '\n'

    cust_out(out_string)


def scale_time(time_seconds):
    updated_time = 0
    if args.time_format == 'f':
        updated_time = full_format(time_seconds)
    elif args.time_format == 's':
        updated_time = seconds_format(time_seconds)
    elif args.time_format == 'm':
        updated_time = minutes_format(time_seconds)
    elif args.time_format == 'h':
        updated_time = hours_format(time_seconds)
    return updated_time


def hours_format(num):
    updated_time = num / 3600
    updated_time = handle_truncate(updated_time)
    return str(updated_time) + " hours"


def minutes_format(num):
    updated_time = num / 60
    updated_time = handle_truncate(updated_time)
    return str(updated_time) + " minutes"


def seconds_format(num):
    return str(int(num)) + " seconds"


def full_format(num):
    updated_time = 0
    if num >= 3600:
        updated_time = hours_format(num)
    elif num >= 60:
        updated_time = minutes_format(num)
    else:
        updated_time = seconds_format(num)
    return updated_time

def handle_truncate(num):
    if args.truncate_level == 0:
        return int(num)
    return truncate(num, args.truncate_level)

def truncate(f, n):
    s = '%.12f' % f
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])


def get_time_formatted(time_lst: list) -> int:
    dt_obj = datetime.strptime(time_lst, args.date_format)
    return dt_obj.timestamp()


def cust_out(out_string: str):
    if args.outfile:
        fout = open(args.outfile.name, 'w')
        fout.write(out_string)
        fout.close()
    else:
        print(out_string)


# handle arguments:
parser = argparse.ArgumentParser(
    description="Returns the times of bcs projects from fulllog.txt files by default, could be used for others.")
parser.add_argument(dest="INFILE", 
                    nargs='?',
                    type=argparse.FileType('r'),
                    help="fulllog.txt's full path")

parser.add_argument('-v', "--version", 
                    action="version", 
                    version="BCS Timer Version 1.0",
                    help="Show program version")

parser.add_argument('-o', dest="outfile",
                    nargs='?',
                    type=argparse.FileType('w'),
                    help="Save to file <path to file> ")

parser.add_argument('-d', dest="date_format",
                    nargs='?',
                    default="%Y-%m-%d %H:%M:%S",
                    type=str,
                    help="select date format to be used in document")

parser.add_argument('-l', dest="truncate_level",
                    nargs='?',
                    default=3,
                    type=int,
                    help="Select decimal rounding level")

parser.add_argument('-t', dest="time_format",
                    nargs='?',
                    default="f",
                    type=str,
                    choices=['f', 's', 'm', 'h'],
                    help="select time format full(default), seconds, minutes, or hours only")


# parser.add_argument('-r', '--run', help="Time during run") # may or may not implement, seems unnecissary

args = parser.parse_args()

if __name__ == "__main__":
    main(args)
