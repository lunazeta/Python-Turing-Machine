from .graphicsDisplay import *
from .exceptions import InvalidFileTypeError

# Acts in a similar way to a list, but everything is index from the original start point
class Tape:

    # If the index is not in range of the current defined tape, then return a blank symbol
    def __getitem__(self, index: int):
        if index in range(self.min, self.max + 1):
            return self.tape[index - self.min]
        else:
            return "_"

    def __setitem__(self, index: int, value):
        if index in range(self.min, self.max + 1):
            self.tape[index - self.min] = value
        elif index < self.min:
            self.min = index
            self.tape[0] = value
        else:
            self.max = index
            self.tape.append(value)

    def return_tape(self):
        string = ""
        for i in self.tape:
            string += i
        return string

    def __init__(self, tape: str):
        self.min = 0
        self.max = len(tape) - 1
        self.tape = list(tape)

# Iterprets a line of the delta function and adds it to the dict
def interpret_delta(line: str, delta_function: dict):
    #sN,1 -> sM,1,>

    left_right = line.split("->")
    if len(left_right) != 2:
        raise SyntaxError

    left = left_right[0].strip().split(",")
    right = left_right[1].strip().split(",")

    if len(left) != 2 or len(right) != 3:
        raise SyntaxError
    
    start_state = left[0]
    read = left[1]
    if len(read) != 1:
        raise SyntaxError
    
    end_state = right[0]
    write = right[1]
    if len(write) != 1:
        raise SyntaxError

    left_or_right = right[2]
    if left_or_right not in ["<",">","-"]:
        raise SyntaxError

    if start_state not in delta_function:
        delta_function[start_state] = {}
    delta_function[start_state][read] = [end_state, write, left_or_right]

    return delta_function

def getParameter(line: str, parameter: str):
    if not line.startswith(parameter + ":"):
        raise SyntaxError
    
    left_right = line.split(":")
    if len(left_right) != 2:
        raise SyntaxError
    
    return left_right[1].strip()

# Interpret one line from the Turing Machine file
def interpret_line(line: str, delta_function: dict, arguments: list, requiredParameters: list):
    if line == "\n" or line == "":
        return None, None
    for param in enumerate(requiredParameters):
        try:
            arguments[param[1]] = getParameter(line, param[1])
            requiredParameters.pop(param[0])
            return arguments, None
        except SyntaxError:
            pass
    delta_function = interpret_delta(line, delta_function)
    return None, delta_function

# Execute one cycle of the Turing Machine
def stepTuringMachine(delta_function: dict, tape: Tape, currentIndex, current_state):
        detail = delta_function[current_state][tape[currentIndex]]
        current_state, tape[currentIndex] = detail[0], detail[1]
        
        if detail[2] == "<":
            currentIndex -= 1
        elif detail[2] == ">":
            currentIndex += 1
        
        return current_state, currentIndex, tape

class TuringMachine:

    REQUIRED_PARAMETERS = ["start", "tape", "halt"]

    def _interpretFile(self):
        line = "\n"
        arguments = {}
        delta_function = {}
        END_OF_FILE = ""

        with open(self.file, "r") as f:
            while line != END_OF_FILE:
                line = f.readline()
                argumentsTemp, delta_functionTemp = interpret_line(line, delta_function, arguments, self.REQUIRED_PARAMETERS)

                # Check which return value has been returned (i.e. the parameter not returned will be None)
                # And update accordingly
                if not argumentsTemp and delta_functionTemp: 
                    delta_function = delta_functionTemp
                elif not (argumentsTemp or delta_functionTemp):
                    pass
                else:
                    arguments = argumentsTemp 
        
        delta_function[arguments["halt"]] = {}
        return delta_function, arguments

    def _init(self):
        start_state, halting_state = self.arguments["start"], self.arguments["halt"]
        tape = Tape(self.arguments["tape"])
        current_state = start_state
        return halting_state, tape, current_state

    def _run_without_graphics(self, stepMode: bool):
        halting_state, tape, current_state = self._init()
        currentIndex = 0
        operations = [[current_state, currentIndex, [tape.return_tape(), tape.min, tape.max]]]

        while current_state != halting_state:
            if stepMode:
                print(" "*currentIndex + "H")
                print(tape.return_tape())
                input("Press enter to continue... ")
            
            current_state, currentIndex, tape = stepTuringMachine(self.delta_function, tape, currentIndex, current_state)
            operations.append([current_state, currentIndex, [tape.return_tape(), tape.min, tape.max]])
        
        return operations, tape

    # Run the Turing Machine first, then iterate over each step in a graphical display
    def _run_with_graphics(self):
        operations, tape = self._run_without_graphics(False)
        
        tape_display = TapeDisplay()
        tape_display.run(operations)
        

    def run(self, stepMode=False, graphics_mode=False):
        if not graphics_mode:
            operations, tape = self._run_without_graphics(stepMode)
            print("Result: " + tape.return_tape().strip("_"))
        else:
            self._run_with_graphics()

    def __init__(self, file: str):
        if not file.endswith(".turing"):
            raise InvalidFileTypeError("File type must be .turing")
        self.file = file
        self.delta_function, self.arguments = self._interpretFile()
        self.halting_state = self.arguments["halt"]

if __name__ == "__main__":
    my_turing_machine = TuringMachine("example.turing")
    my_turing_machine.run(graphics_mode=True)