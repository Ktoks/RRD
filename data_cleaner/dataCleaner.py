import argparse

convert_bad_to_comma_delimited = False

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file",
                    help="<Required> full path to the input '|' seperated file(input is as follows: -f filename)",
					dest="input",
					required=True)
parser.add_argument("-g", "--good",
                    help="full path to the 'good' output csv, default is good_output.csv",
					default="good_output.csv",
					dest="gOutput",
                    required=False)
parser.add_argument("-b", "--bad",
                    help="full path to the 'bad' output csv, default is bad_output.csv",
					default="bad_output.csv",
					dest="bOutput",
                    required=False)


args = parser.parse_args()

def main():

    goodString = []
    badString = ""

    goodCount = 0
    badCount = 0
    totalCount = 0

    with open(args.input, 'r') as fin:
        for line in fin:
            line = line.strip()
            if len(line) < 3:
                continue
            if convert_bad_to_comma_delimited and "," in line:
                strBegin = 0
                locComma = 0

                for i in range(len(line)):
                    if line[i] == ",":
                        locComma = i
                        
                    elif line[i] == "|":
                        if locComma == 0:
                            strBegin = i
                        else:
                            line = line[:strBegin + 1] + '"' + line[strBegin + 1:i] + '"' + line[i:]
                            break

            if "TRAILER_TOTAL" in line:
                tempLST = line.split("|")
                newGoodString = ""
                newBadString = ""
                for i in range(len(tempLST) - 1):
                    if i == 1:
                        totalCount = float(tempLST[i])
                        newGoodString += str(float(goodCount)) + '|'
                        newBadString += str(float(badCount)) + '|'
                    else:
                        newGoodString += tempLST[i] + '|'
                        newBadString += tempLST[i] + '|'
                goodString.append(newGoodString)
                if convert_bad_to_comma_delimited:
                    badString += newBadString.replace("|", ",")
                else:
                    badString += newBadString
            elif "BD" == line[:2]:
                goodString.append(line)
                if convert_bad_to_comma_delimited:
                    badString += line.replace("|", ",")
                else:
                    badString += line
            elif "|||||||||" in line:
                if convert_bad_to_comma_delimited:
                    badString += line.replace("|", ",")
                else:
                    badString += line
                badCount += 1
            else:
                goodString.append(line)
                goodCount += 1

    # check to ensure no rows were lost or created

    if badCount + goodCount != totalCount:
        print("Error: count off:", badCount, "+", goodCount, "vs", totalCount)
        exit(1)
    
    with open(args.gOutput, 'w', newline='\r\n') as fout:
        for line in goodString:

            fout.write(line +"\n")

    original_file = ""
    with open(args.input, 'r') as fin:
        for line in fin:
            line = line.strip()
            original_file += line

    with open(args.gOutput, 'r') as fin:
        errs = []
        for line in fin:
            line = line.strip()
            if "TRAILER_TOTAL" in line:
                break
            if not line in original_file:
                errs.append(line)

        for err in errs:
            print("line not in file:", err)
            exit(1)

    if len(badString) != 0:
        with open(args.bOutput, 'w') as fout:
            fout.write(badString)
            print("Bad output file in", args.bOutput)


if __name__ == "__main__":
    main()