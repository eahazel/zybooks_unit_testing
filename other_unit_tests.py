# Count Inputs
import re

def check_inputs(file_path, num_inputs):
    """
    Checks how many inputs the user asked for

    Args:
        file_path (str): The path to the file to search.
        num_inputs (int): The number of inputs the program expects

    Returns:
        bool: True the correct number of inputs are found, False otherwise.
        int: number of found inputs in the program
    """
    try:
        count = 0
        with open(file_path, 'r') as file:
            for line in file:
                if(line[0] == '#'):
                    continue
                if("input(" in line):
                    count += 1
        if count == num_inputs:
            return True, count
        return False, count
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return False, count
    except Exception as e:
        print(f"An error occurred: {e}")
        return False, count

def test_passed(test_feedback):
    """
    Tests if the student's code asks for the proper amount of inputs
    
    Args:
        test_feedback: An object with a 'write' method to provide feedback.

    Returns:
        bool: True if all checks pass, False otherwise.
    """
    file_path = "main.py"
    expected_input = 3

    passed, found_input = check_inputs(file_path, expected_input)
    if(not passed):
        test_feedback.write(f"Test FAILED. Your file must contain {expected_input} inputs.  You only have {found_input}" + (" input." if found_input == 1 else " inputs."))
        return False

    # If all checks pass, the test passes
    test_feedback.write(f"Test PASSED.  You asked for the right amount of input.")
    return True

# Check Input types

import re

def check_inputs(file_path):
    """
    Checks how many inputs the user asked for

    Args:
        file_path (str): The path to the file to search.

    Returns:
        bool: True if an input of each type was found, 
        False otherwise.
    """
    # Fill in with how many of each type
    # of input this problem requires
    expected_float = 1
    expected_int = 1
    expected_string = 1

    float_count = 0
    int_count = 0
    string_count = 0

    try:
        with open(file_path, 'r') as file:
            for line in file:
                stripped_line = line.strip()
                if stripped_line.startswith('#'):
                    continue
                int_count += len(re.findall(re.escape("int(input("), line))
                float_count += len(re.findall(re.escape("float(input("), line))
                string_count += len(re.findall(r'(?<!int\()(?<!float\()input\(', line))
        return expected_int == int_count and expected_float == float_count and string_count == expected_string

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def test_passed(test_feedback):
    """
    Tests if the student's code asks for the proper amount of inputs
    
    Args:
        test_feedback: An object with a 'write' method to provide feedback.

    Returns:
        bool: True if all checks pass, False otherwise.
    """
    file_path = "main.py"

    if(check_inputs(file_path)):
        test_feedback.write(f"Test PASSED.")
        return True
    
    test_feedback.write(f"Test FAILED. Your inputs are not of the correct type.")
    return False    