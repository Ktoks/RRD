# RRD bcs_timer

This script is used to show how long an entire project takes to run by individual processes.

### Required:
Input log file to be timed, it is suggested to use the full path

### Optional:
__-v__ or __--version__ Displays the version number

__-h__ or __--help__ Displays help to the command line

__-o__ Outputs program log times to any file

__-d__ Input date format to be captured in log documents:
- default: __"%Y-%m-%d %H:%M:%S"__ this string is formatted as such for the python module 'datetime', refer to their documentation

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
