# CSV Data File Mocker

## This project is meant to be a test data creater for RRD developers
<br><br>

#### I have yet to determine if this tool would be worth my time- I will take a poll to determine value and interest
<br><br>

---

<br><br>

## The plan is to create a versatile mocker that can take 3 types of input:<br><br>

- ### Options via CLI (_to be implemented first_)
  > This would be used as a quick mocker- and could be used inline in scripts to create a temporary datafile to be deleted once used

<br>

- ### Configuration files (_yaml_)
  > This would allow users to create an easily readable file to be passed to the mocker to select whatever options the project requires

<br>

- ### Single data line inputs (_implemented last_)
  > This would allow users to create a file of any size from a single line example

<br><br>

---
<br><br>

## The tool would parse the inputs, as well as options for the number of records
<br>

### Possible options to be implemented:
- Select "," or "|" as column seperators<br>
- Select if sequential data is needed (possibly for debugging purposes)<br>
- Select if random data is needed(default)<br>
- Select if 2 or more files are to be created simultaneously<br>
- Logging to a second file(for debugging purposes)

<br><br>

---

<br><br>

## The tool would save the data row-by row of creation- allowing the user to halt it at any time by pressing CTRL-C

<br><br>

---

<br><br>

## The tool would run sequentially per each data file to be created- could concurrently run if multiple data files are to be created