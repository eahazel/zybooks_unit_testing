import sys, io
import random
import importlib

# What type of unit test are you performing?
# UPDATE FOR EACH PROBLEM
output_check = True
var_check = False
fun_check = False

#create the actual answer
# UPDATE FOR EACH PROBLEM
def actual_answers(name, age, num):
    return f"Name: {name}",f"Age: {age}",f"Favorite Number: {num}"

# If you are checking a function or variable what is it's name
# UPDATE FOR EACH PROBLEM
var_or_fun_name = 'diff_numbers'

# How many interations of the test do you want to run?
iterations = 5
test_inputs_raw = []

#create your inputs
for i in range(iterations):
    # Set up randomized values for inputs
    name_list = ['Michael', 'Bobby', 'Ed', 'Fred', 'James']
    name = random.choice(name_list)
    age = random.randint(18,50)
    num = round(random.random() * 50, 1) 

    # Craft inputs
    test_inputs_raw.append([name, age, num])

#Nothing after this should need adjustment
def test_passed(test_feedback):

    test_passed = True
    for raw_inputs in test_inputs_raw:
        test_input = '\n'.join([str(x) for x in raw_inputs])

        learner_code, stu_output = handle_run_test_main(test_input)

        answers = actual_answers(*raw_inputs)

        if output_check == True:
            test_passed = check_outputs(answers, stu_output, test_feedback)
            if test_passed == False:
                break
        if var_check == True:
            test_passed = test_variable(var_or_fun_name, answers, learner_code, test_feedback)
            if test_passed == False:
                break
        if fun_check == True:
            test_passed = test_function(var_or_fun_name, answers, learner_code, test_feedback, *raw_inputs)
            if test_passed == False:
                break
    
    if test_passed:
        test_feedback.write(f"Output is Correct")
    else:
        test_feedback.write(f"Output is Incorrect")
    
    return test_passed

def check_outputs(answers, output, test_feedback):
    result = True
    for answer in answers:
        if answer in output:
            pass
        else:
            result = False
    return result

def test_variable(var_name, answers, learner_code, test_feedback):

    #checks to see that the varible is in the learner code
    if not hasattr(learner_code, var_name):
        test_feedback.write(f"The variable '{var_name}' should exist, but it is not present in your program.")
        return False
    else:
        test_var = getattr(learner_code, var_name)

    #Checking the students stored value == the expected answer
    result = True
    for answer in answers:
        if(answer == test_var):
            pass
        else:   
            result = False
    return result
    
def test_function(fun_name, answers, learner_code, test_feedback, *args):
    # Verify the function exists in the imported module
    if not hasattr(learner_code, fun_name):
        test_feedback.write(f"The description the '{fun_name}' function should exist, but it is not present in your program.")
        return False
    else:
        # test_function is now the function we are grading/validating
        test_fun = getattr(learner_code, fun_name)
    
    # Verify the attribute is actually a callable function
        if not callable(test_fun):
            test_feedback.write(f"The description the '{fun_name}' function should exist, but it is not present in your program.")
            return False
    
    #call the students function
    stu_ans = test_fun(*args)

    #Checking the students function returned the expected answer
    result = True
    for answer in answers:
        if(answer == stu_ans):
            pass
        else:   
            result = False
    return result

# Boilerplate to enable multiple runs of the main.py the students are writing
# returns the loaded 'main' module as 'student_main'
# returns a string with all the stdout from student code 'stu_printed'
def handle_run_test_main(test_input):
    # Save off stdin, stdout
    stdin = sys.stdin
    stdout = sys.stdout

    # Initialize test harness stdin and stdout
    sys.stdin = io.StringIO(test_input)
    sys.stdout = io.StringIO()

    # Load or reload the module/script
    if 'main' in sys.modules:
        student_main = importlib.reload(sys.modules['main'])
    else:
        student_main = importlib.import_module('main')

    # Collect any outputs
    stu_printed = sys.stdout.getvalue().strip()

    # Give back stdin and stdout control to zybooks
    sys.stdout = stdout
    sys.stdin = stdin

    return student_main, stu_printed