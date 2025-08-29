#Import Statements
import sys, io, importlib
import random

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

    #setting the variable or function we are checking for
    test_variable_name = 'E'
    
    #Checking that the variable is present
    if not hasattr(learner_code, test_variable_name):
        test_feedback.write(f"The description the variable '{test_variable_name}' should exist, but it is not present in your program.")
        return False
    
    #setting up the expected answer
    answer =  m * (c_speed**2)
     
    #printing the input values
    print(f"Mass input: {m} (kg).")
    
    #Checking the students stored value == the expected answer
    if(answer == learner_code.E):
        print(f"Your answer matches the expected answer: {answer} Joules")
        return True
    else:   
        print(f"Incorrect.\nYour answer: {learner_code.E}\nExpected answer: {answer}")
        return False
