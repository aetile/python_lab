# python_lab
Finite-state mower fleet automation in a bitmap field

### Python version
This lab was tested with version 2.7 and 3.6

### Dependencies
Python libraries used in this lab are the following:

```
sys:      used to pass arguments with sys.argv
os:       used for manipulating files on the system
logging:  used to log events and errors
pprint:   used for nice printing of 2D arrays
```

### Principles
This lab was written with the following assertions:

```
- Mowers are finite-state machines which can do 1 of 3 actions when receiving an instruction:
      -> step
      -> turn left
      -> turn right
- Finite-state is managed with dictionaries rather than if..elif statements
- Mowers receive instructions from an input file containing:
       -> field measures
       -> mower position
       -> mower list of instructions
- Mower field is a rectangular bitmap used to detect mower collisions:
       -> 0: no mower present
       -> 1: a mower is already there
- Mowers act sequentially, one after the other
- Mowers should ignore instructions asking them to cross field borders
- Mowers should ignore instructions asking them to collide another mower
- Mowers should report their final position in an output file
```

### Executing the lab
Execute the MowItNow.py module with the following arguments: input file name and output file name
```
cd ./python_lab
python MowItNow.py input.txt output.txt
```

### Running lab tests
Execute the test_MowItNow.py module in the tests directory without passing any argument
```
cd ./tests
python test_MowItNow.py
