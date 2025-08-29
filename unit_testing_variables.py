#Import Statements
import sys, io, importlib
import random
import math

# Speed of light for use in equation 1
c_speed = 299792458 # m / s

# Gravitational constant for use in equation 3
G = 6.6743 * (10 ** -11) # m^3 * kg^-1 * s^-2

# Test input
m = float(random.randint(100, 200))
a = float(random.randint(5, 10))
b = float(random.randint(5, 10))
m1 = float(random.randint(1000000, 2000000000))
m2 = float(random.randint(1000, 2000000))
r = float(random.randint(10000, 20000000000))
input_list = [str(m), str(a), str(b), str(m1), str(m2), str(r)]

# Save off stdin, stdout
stdin = sys.stdin
stdout = sys.stdout

# Initialize test harness stdin and stdout
sys.stdin = io.StringIO('\n'.join(input_list))
sys.stdout = io.StringIO()

# Load or reload the module/script
if 'main' in sys.modules:
    learner_code = importlib.reload(sys.modules['main'])
else:
    learner_code = importlib.import_module('main')

# Collect any outputs
stu_printed = sys.stdout.getvalue().strip()

# Give back stdin and stdout control to zybooks
sys.stdout = stdout
sys.stdin = stdin

def test_passed(test_feedback):
    
    #setting up the expected answer
    answer =  G * m1 * m2 / r

    #printing the input values
    test_feedback.write(f"Input:\nMass 1: {m1} kg.\nMass 2: {m2} kg.\nDistance: {r} meters")

    return test_variable('F',answer, test_feedback)


def test_variable(var_name, answer, test_feedback):

    #checks to see that the varible is in the learner code
    if not hasattr(learner_code, var_name):
        test_feedback.write(f"The variable '{var_name}' should exist, but it is not present in your program.")
        return False

    var_name = getattr(learner_code, var_name)

    #Checking the students stored value == the expected answer
    if(answer == var_name):
        test_feedback.write(f"Correct, Your answer matches the expected answer: {answer}")
        return True
    else:   
        test_feedback.write(f"Incorrect, Your answer: {var_name}\nExpected answer: {answer}")
        return False