import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--files",
                    help="<Required> full path to the input csv files(input is as follows: -f file1 file2 file3 etc...",
					nargs='+', 
					dest="input_csv",
					required=True)
parser.add_argument("-o", "--output",
                    help="full path to the output csv, default is {input_csv}.output.csv",
					default="output.csv",
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
	for file_in in args.input_csv:
		fin = open(file_in, 'r', encoding = "ISO-8859-1")
		is_first_line = True

		column = file_in.split("_")[0]

		# set up the header
		if first_file:
			first_line = fin.readline()
			first_line = do_replace(first_line)
			new_str += first_line + '\n'
			is_first_line = False
			first_file = False
		
		# for each line of the current file
		for line in fin:

			if is_first_line:
				is_first_line = False
				continue

			line = do_replace(line)

			# add new column to string
			new_str += column + "," + line + "\n"

		fin.close()
	fout = open(args.output, "w")
	fout.write(new_str)
	fout.close()


"""Get rid of `"`, replace `|` with `,`, and get rid of excess space"""
def do_replace(line):
	line = line.strip()
	line = line.replace("|", ",")
	line = line.replace("   ", " ")
	line = line.replace("  ", " ")
	line = line.replace("\"", "")
	return line


if __name__ == "__main__":
    main()
