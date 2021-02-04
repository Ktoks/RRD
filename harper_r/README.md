# RRD harper_r

This Python-based script is used to edit lines in a file if another specific line of text is present in the file

The general input lines need to be case sensetive and whitespace sensetive:

So long as the lines match somewhere in the document to the cues(-c) which default to 
```
<COMMUNICATION_SUBTYPE>TDCD</COMMUNICATION_SUBTYPE>,
<COMMUNICATION_SUBTYPE>TDBD</COMMUNICATION_SUBTYPE>,
<COMMUNICATION_SUBTYPE>TDBX</COMMUNICATION_SUBTYPE>
```

Then lines specified as replace \[0\]\(-r\) which default to
```
<RECIPIENT_DELIVERY_METHOD>MAIL</RECIPIENT_DELIVERY_METHOD>
```
will be replaced with replace[1] which defaults to
```
<RECIPIENT_DELIVERY_METHOD>PDF</RECIPIENT_DELIVERY_METHOD>
```

## Required:
Input file file and output file to be parsed, it is suggested to use the full path for each

### Optional:
__-v__ or __--version__ Displays the version number

__-h__ or __--help__ Displays help to the command line

__-o__ Outputs the changed file to a file in append mode, so ensure the file you want made doesn't already exist

__-c__ Allows selection of the cue strings- in this version you can use any number of strings
