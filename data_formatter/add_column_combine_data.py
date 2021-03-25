import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--files",
                    help="<Required> full path to the input csv files(input is as follows: -f file1 file2 file3 etc...",
					nargs='+', 
					dest="input",
					required=True)
parser.add_argument("-o", "--output",
                    help="full path to the output csv, default is {input_csv}.output.csv",
					default="{input_csv}.output.csv",
					dest="output",
                    required=False)
parser.add_argument("-n", "--name",
                    help="The header name of the column",
                    default="LETTER_ID",
                    dest="header",
					required=False)
args = parser.parse_args()

"""outputs a file merged from input files, comma seperated, 
with an column added to discern where each line came from"""
def main():
	new_str = args.header + ","
	first_file = True

	# for each input file
	for file_in in args.input:
		fin = open(file_in, 'r')
		is_first_line = True

		column = file_in[0:3]

		# set up the header
		if first_file:
			first_line = fin.readline()
			first_line = first_line.replace("|", ",")
			new_str += first_line
			is_first_line = False
			first_file = False
		
		# for each line of the current file
		for line in fin:
			line = line.strip()
			if is_first_line:
				is_first_line = False
				continue

			line = line.replace("|", ",")

			# add new column to string
			new_str += column + "," + line + "\n"

		fin.close()
	fout = open(args.output, "w")
	fout.write(new_str)
	fout.close()


if __name__ == "__main__":
    main()
