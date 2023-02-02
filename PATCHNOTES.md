# Patch notes

## v1.0.0

 - Command line Turing Machines
 - Graphical Turing Machines

## v1.1.0
 
 - A start to creating diagram support for the Turing Machines:
```python
from qwhatyTuring import interpreter, diagrams

myTur = interpreter.TuringMachine("example.turing")
diagram = diagrams.Diagram(myTur.deltaFunction, myTur.haltingState)
diagram.run()
```
 - You can place and move nodes which represent the states of the Turing Machine