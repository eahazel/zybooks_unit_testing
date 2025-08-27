import sys, io
import random
import importlib

def test_passed(test_feedback):
    # Set the name of the function we are testing
    test_function_name = 'diff_numbers'

    # Set to True if print out is being checked
    check_printing = True
    check_function = False

    test_passed = True
    for i in range(1,5):
        # Set up randomized values for inputs
        x = random.randint(1,50)
        y = random.randint(1,50)

        # Craft inputs
        test_input=f"{x}\n{y}"

        # Set up real answer based on those inputs
        act_ans = abs(x-y)

        # Save off stdin, stdout
        stdin = sys.stdin
        stdout = sys.stdout

        # Initialize test harness stdin and stdout
        sys.stdin = io.StringIO(test_input)
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

        # Verify the function exists in the imported module
        if not hasattr(learner_code, test_function_name):
            test_feedback.write(f"The description the '{test_function_name}' function should exist, but it is not present in your program.")
            return False
        else:
            # test_function is now the function we are grading/validating
            test_function = getattr(learner_code, test_function_name)
        
        # Verify the attribute is actually a callable function
        if not callable(test_function):
            test_feedback.write(f"The description the '{test_function_name}' function should exist, but it is not present in your program.")
            return False

        # Call the student's function (implementation may vary)
        stu_ans = test_function(x, y)

        log_strings = {
            True: 'SUCCESS',
            False: 'FAILURE'
        }

        # If we're grading function, check if function returns expected answer
        if check_function:
            success = stu_ans == act_ans
            if not success:
                test_passed = False
            test_feedback.write(f"Test {i} --> Checking Function --> {log_strings[success]} --> '{test_function_name}({x}, {y})' Returned: {stu_ans}, Expected: {act_ans}")

        # If we're grading print statements, ensure correct output is somewhere in student's prints (implementation may vary)
        if check_printing:
            success = str(act_ans) in stu_printed
            if success:
                test_feedback.write(f"Test {i} --> Checking Output --> Using Inputs '{x}' and '{y}' --> {log_strings[success]} --> Found '{act_ans}' in output, as expected")
            else:
                test_feedback.write(f"Test {i} --> Checking Output --> Using Inputs '{x}' and '{y}' --> {log_strings[success]} --> Did not find '{act_ans}' in output!")
                test_passed = False

    return test_passed
