import sys, io
import random
import importlib

# What type of unit test are you performing?
# UPDATE FOR EACH PROBLEM
output_check = True
var_check = False
fun_check = False

# create the actual answer
# return has to be a list
# UPDATE FOR EACH PROBLEM
def actual_answers(ingredient_to_check):
    
    basic = ["water", "stone", "herb", "moss", "granite", "spider", "mushroom", "root"]
    intermediate = ["quicksilver", "obsidian flake", "mandrake root", "eye of newt", "spider silk"]
    advanced = ["dragonscale", "phoenix feather", "griffin talon", "starlight dust", "unicorn horn", "crystal"]
    def is_in_book(ingredient, book_name):
        if(ingredient in basic):
            return book_name == "Book of Basics"
        if(ingredient in intermediate):
            return book_name == "Adept's Almanac"
        if(ingredient in advanced):
            return book_name == "Archmage's Grimoire"

    if is_in_book(ingredient_to_check, "Book of Basics"):
        return ["Common"]
    elif is_in_book(ingredient_to_check, "Adept's Almanac"):
        return ["Rare"]
    elif is_in_book(ingredient_to_check, "Archmage's Grimoire"):
        return ["Legendary"]
    else:
        return ["Unknown"]

# If you are checking a function or variable what is it's name
# UPDATE FOR EACH PROBLEM
var_or_fun_name = 'get_accessory_cost'

# The number of arguments the function needs
# to account for the location of the desired args in the inputs
# remeber the stop must be one # passed where you want to stop
# UPDATE FOR EACH PROBLEM
fun_arg_start = 0
fun_arg_stop = 1

# How many interations of the test do you want to run?
iterations = 5
test_inputs_raw = []

#create your inputs all main inputs must be accounted for
for i in range(iterations):
    # Set up randomized values for inputs
    ingredient_list = ["water", "stone", "herb", "moss", "granite", "spider", "mushroom", "root"]
    ingredient_to_check = random.choice(ingredient_list)

    # Craft inputs
    test_inputs_raw.append([ingredient_to_check])

#Nothing after this should need adjustment
def test_passed(test_feedback):

    test_passed = True
    for raw_inputs in test_inputs_raw:
        test_input = '\n'.join([str(x) for x in raw_inputs])

        learner_code, stu_output = handle_run_test_main(test_input)

        if stu_output == 'ValueError':
            test_feedback.write(f"Check your Variable types")
            return False
        
        if stu_output == 'EOFError':
            test_feedback.write(f"There are more inputs then expected")
            return False

        if fun_check:
            raw_inputs = raw_inputs[fun_arg_start:fun_arg_stop]

        answers = actual_answers(*raw_inputs)

        if output_check == True:
            test_passed = check_outputs(answers, stu_output, test_feedback)
            if test_passed:
                test_feedback.write(f"Output is Correct")
            else:
                test_feedback.write(f"Output is Incorrect")
                break
        if var_check == True:
            test_passed = test_variable(var_or_fun_name, answers, learner_code, test_feedback)
            if test_passed:
                test_feedback.write(f"Variable is Correct")
            else:
                test_feedback.write(f"Variable is Incorrect")
                break
        if fun_check == True:
            test_passed = test_function(var_or_fun_name, answers, learner_code, test_feedback, *raw_inputs)
            if test_passed:
                test_feedback.write(f"Function is Correct")
            else:
                test_feedback.write(f"Function is Incorrect")
                break
   
    return test_passed

def check_outputs(answers, output, test_feedback):
    result = True
    for answer in answers:
        if str(answer) in output:
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
        if type(answer) == type(test_var):
            if(answer == test_var):
                pass
            else:   
                result = False
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
    print(stu_ans)
    print(answers)
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

    try:    
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
    
    except ValueError as e:
        # Give back stdin and stdout control to zybooks
        sys.stdout = stdout
        sys.stdin = stdin
        return None, 'ValueError'
    
    except EOFError as e:
        sys.stdout = stdout
        sys.stdin = stdin
        return None, 'EOFError'