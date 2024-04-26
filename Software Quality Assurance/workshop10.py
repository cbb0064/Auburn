import json
import random
import traceback

def load_naughty_strings(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    try:
        if y == 0:
            return "Undefined (division by zero)"
        return x / y
    except Exception as e:
        return f"Error: {str(e)}"

def fuzzValues(val1, val2):
    operations = [add, subtract, multiply, divide]
    try:
        # Attempt to convert both values to floats
        val1 = float(val1)
        val2 = float(val2)
        operation = random.choice(operations)
        return operation(val1, val2)
    except ValueError:
        return "Error: invalid input for arithmetic operation"
    except Exception as e:
        return f"Error: {str(e)}"

def simpleFuzzer(naughty_strings):
    errors = []
    for x in naughty_strings:
        try:
            # Modify x to generate alphanumeric strings
            mod_x = x + str(random.randint(1, 10))
            result = fuzzValues(x, mod_x)
            if "Error" in str(result):
                errors.append(f"Input {x}, {mod_x}: {result}")
        except Exception as e:
            error_message = f"Crashed with input {x}: {traceback.format_exc()}"
            errors.append(error_message)

    # Record errors, limiting to seven
    return errors[:7]

if __name__ == '__main__':
    naughty_strings = load_naughty_strings("blns.json")
    error_logs = simpleFuzzer(naughty_strings)
    for error in error_logs:
        print(error)

