#!/usr/bin/env python3
import argparse


def main(args) -> int:
    with open(args.infile, 'r') as fin:
        v_is_present = False

        # quick loop to check if the inputs are present
        for line in fin:
            for arg in args.cue:
                if arg in line:
                    # print("True:", line)
                    v_is_present = True
                    break
        
    # write to the file, changed or not
    with open(args.infile, 'r') as fin:
        with open(args.outfile, 'a') as fout:
            if v_is_present:
                for line in fin:
                    # print("Line:", line)
                    if args.replace[0] in line:
                        line = args.replace[1]
                    # print(line)
                    fout.write(line)
    return 0


parser = argparse.ArgumentParser(
    description="Returns the times processes run from log text files.")
parser.add_argument(dest="infile",
                    nargs='?',
                    type=str,
                    help="<Required> log's full path")

parser.add_argument('-c', dest="cue",
                    nargs='+',
                    default=[
                        "<COMMUNICATION_SUBTYPE>TDCD</COMMUNICATION_SUBTYPE>", 
                        "<COMMUNICATION_SUBTYPE>TDBD</COMMUNICATION_SUBTYPE>",
                        "<COMMUNICATION_SUBTYPE>TDBX</COMMUNICATION_SUBTYPE>"],
                    help="Text possibly present to change 'mail' to 'pdf' delivery method")

parser.add_argument('-r', dest="replace",
                    nargs='+',
                    default=["<RECIPIENT_DELIVERY_METHOD>MAIL</RECIPIENT_DELIVERY_METHOD>",
                             "<RECIPIENT_DELIVERY_METHOD>PDF</RECIPIENT_DELIVERY_METHOD>"],
                    help="Text possibly present to change 'mail' to 'pdf' delivery method")

parser.add_argument('-o', dest="outfile",
                    nargs='?',
                    type=str,
                    required=True,
                    help="Save to file <path to file> ")

parser.add_argument('-v', "--version",
                    action="version",
                    version="Harper_R 0.1",
                    help="Show program version")

args = parser.parse_args()


if __name__ == "__main__":
    if not main(args):
        print(args.infile + " processed successfully.")
