# Name test "Output Test"
# Import Statements

import sys, importlib, random, math
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout
from types import ModuleType

# ***Adjust this section as needed for the Lab***

# Feedback options, lab_feedback gives a lot of feedback, test_feedback provides minimun feedback

lab_feedback = True
PA_feedback = False

# Create the answer you are looking for based on inputs, *** return must be a list
def actual_answers(age):
    return [age + 4]

# How many interations of the test do you want to run?
iterations = 5

#create your inputs all main inputs must be accounted for

test_inputs_raw = []

for i in range(iterations):
    # Create the inputs using random
    
    #random strings
    #name_list = ["Edward", "James", "David", "Tiffany", "Claire", "Sarah"]
    #name = random.choice(name_list)
    
    #random int
    age = random.randint(18, 24)

    #random float
    #decimal = round(random.random() * 1000, 2)

    # Craft inputs, *** must be a list
    test_inputs_raw.append([age])

# ***After this point nothing should need to be changed***

def test_passed(test_feedback):

    test_passed = True

    for raw_inputs in test_inputs_raw:

        sink = StringIO()
        with redirect_stdout(sink):
            with patch("builtins.input", side_effect = raw_inputs) as mock_input:
                main = fresh_import('main', test_feedback)

        answers = actual_answers(*raw_inputs)

        if lab_feedback:
            test_feedback.write(f"given the inputs of {raw_inputs} your code was:")

        test_passed = check_outputs(answers, sink.getvalue(), test_feedback)

    return test_passed
        
# Brings in the student's code, catches the ValueError and EOFError
def fresh_import(module_name: str = 'main', feedback_file = None) -> ModuleType:
    try:
        if module_name in sys.modules:
            del sys.modules[module_name]
    except ValueError as e:
        if feedback_file:
            feedback_file.write(f"Check your input variable data types and conversions")
    except EOFError as e:
        if feedback_file:
            feedback_file.write(f"There are more inputs then expected")
    return importlib.import_module(module_name)

def check_outputs(answers, output, test_feedback):
    result = True
    for answer in answers:
        if str(answer) in output:
            if PA_feedback:
                test_feedback.write(f"Correct, your printed value matches the expected value\n")
            elif lab_feedback:
                test_feedback.write(f"Correct, Your printed value matches the expected value of: {answer}\n")
        else:
            result = False
            if PA_feedback:
                test_feedback.write(f"Incorrect, your printed value does not match the expected value\n")
            elif lab_feedback:
                test_feedback.write(f"Incorrect, Your printed value does not match the expected value of: {answer}\n")

    return result