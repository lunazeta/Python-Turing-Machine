# Python Turing Machine

This is a python program which takes a description of a Turing Machine and executes it, returning the result.

It has two modes:
 - Graphical (can be initialised using TuringMachine.run(graphicsMode=True))
 - Command-line (this is the default setting)

# How do I create my own Turing Machine?

 - Create a file with the extension ".turing"
 - To create a start state you must begin by writing "start:", before then writing the start state (this can be anything, however I personally use sN)
 - To set a halting state, you must write "halt:", before then writing the halting state (again, there are no naming rules, however I personally only use sH)
 - To set up a tape, you must first write "tape:", before writing your tape (the tape can use any alphabet)

Once you all of this set up, you can now finally start making your delta function:

A delta function has the following syntax:

 - "{currentState},{readChar} -> {nextState},{writeChar},{leftWrite}"
 - leftWrite can be either of the following:
    - "<", denoting a move left operation
    - ">", denoting a move right operation
    - "_", denoting the head to stay in place

# How do I run my Turing Machine?

Initialising a turing machine is easy:

```python
import interpreter as tur
myTuringMachine = tur.TuringMachine("yourTuringMachine.turing")
myTuringMachine.run(graphicsMode=True)
```

This will run the file "yourTuringMachine.turing" in graphics mode