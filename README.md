# RRD bcs_timer

This Python-based script is used to show how long an entire project takes to run by individual processes

The general input log file lines need to be formatted as such:
```
Start app_process:  full_process <2021-01-22 18:30:07>
End app_process:  full_process <2021-01-22 18:41:42>
```
Each line must have at least those 4 entities in it
An alternative, for example, would look something like this:
```
Begin process:  begin_process 2021022 18:30:07>
Finsish process:  begin_process 20210122 18:41:42>
```
so long as the names of the processes are the same, and the date and time are formatted the same as eachother, this script should do the job nicely

### Required:
Input log file to be timed, it is suggested to use the full path

### Optional:
__-v__ or __--version__ Displays the version number

__-h__ or __--help__ Displays help to the command line

__-o__ Outputs program log times to any file

__-c__ Allows selection of the cue or the string at the beginning of the line that contains the date and time on it, this should be formatted as such: {-c "Start app_process" "End app_process"} you can use 'begin' instead of 'Start' or 'finish' instead of 'End', but in this version- there needs to be two words in each parenthesis group

__-d__ Input date format to be captured in log documents:
- default: __"%Y-%m-%d %H:%M:%S"__ this string is formatted as such for the python module [datetime](https://docs.python.org/3/library/datetime.html), refer to their documentation for the chart __strftime() and strptime() Format Codes__ near the bottom of the page

__-L__ Allows selection of truncation level, options are:
- __0__ will display output in ints
- __1__ will display floats with a tenths decimal number
- __2__ will display floats with a hundredths decimal number
> etc...

__-t__ Allows you to format time output, options are:
- __f__ is full(default), it will make output the most readable by formatting anything over 60 seconds to be displayed in minutes, and anything over 60 minutes to be displayed in hours
- __h__ is hours, it will display output in hours only
- __m__ is minutes, it will display output in minutes only
- __s__ is seconds, it will display output in seconds only
