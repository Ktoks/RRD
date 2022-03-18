autoRun
========================

### This project is currently in its architectural phase (Nothing is completed at this time)
#### Architect: [@kacystocks][kacystocks]
---------------
- ### An 'automated run' script to be executed from a home directory and/or bashrc for now. In the future, if it's adopted, version 2.0 could be a binary
- ### It automatically runs a powerstream instance of the app it's pointed to, times the run(total and subprocesses), and provides usage stats

- ### It is configurable per user using ~/.autoRun.cfg which is generated with a defaults section
- ### This defaults section is so the user can copypasta configurations they wish to change

## Main features(first features to be implemented):
- #### It should fail and print an error if user config file has improper syntax
- #### If defaults section of config is edited, edits will be moved to user section of the config file, leaving a clean defaults section
- #### It should look at the run dir and/or ..pjt/.autoRun.log to sequencially choose a new order number each time it's run
- #### It should fail early if it can't find an execution command to run
- #### It should fail early if it can't find a data file in input or child of input
- #### It should find the most recently used data file either in run, or by looking in input for the most recently modified data file
- #### It should time the run and append to ..pjt/.autoRun.log and tee the output to the cli how long it spent in each subprocess and the user that ran it
- #### During it's BETA phase, it will also tee output to a centralized log file to track usage(for testing and usage tracking purposes so see if it's worth building a binary, this can't be turned off while using BETA in the cfg file)

## Default features(set both in userspace and pjt{where pjt overrides userspace}):
- #### do not check if running in tmux
- #### do not call own tmux instance
- #### do not spawn in seperate window, or hidden instance that will return output upon completion
- #### do not kill instance upon completion
- #### do not only display output on errors
- #### do not ask for pattern recognition in ..pjt/.autoRun and/or run dirs for > 1 control file-based apps
- #### check ..pjt/.autoRun.log file to find commands before run dir(which could be empty)
- #### log svn version upon every run (log svn version on [rc=0, rc!=0])
- #### run using sequential n #s ([randomized, onm, svn-based, and favorited] where favorite renames past runs to keep using the same n#)
- #### always auto_order_number=n
- #### always xmit_on=n
- #### always emails_on=n
- #### always dupcheck=n
- #### always lvl=t
- #### always lvlc=t
- #### do not update ../pjt/.autoRun.cfj in current project

## Support

## License
The code will available at [GitHub][home] under the [MIT license][license].

[license]: http://revolunet.mit-license.org
[home]: https://github.com/
[kacystocks]: https://github.com/kacystocks
