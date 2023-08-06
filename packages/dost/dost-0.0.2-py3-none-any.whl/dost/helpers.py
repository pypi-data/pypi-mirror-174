def get_time():
    from datetime import datetime
    return datetime.now().strftime('%Y:%m:%d_%H:%M:%S - ')


def try_catch_log_check_output(errors: list, save_log: bool, log_file: str):
    """This decorator logs the call time and parameters of a function
    as well as indicating if the function was successful"""

    import sys
    import os
    import time
    import sys
    from typing import get_args
    from functools import wraps
    from typeguard import check_type

    log_path = os.path.abspath(log_file)
    if not os.path.exists(log_path):
        with open(log_path, 'w') as f:
            f.write('')


    def log_wrap(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                start = time.perf_counter()
                result = func(*args, **kwargs)
                try:
                    type_dict = func.__annotations__
                    
                    if 'return' in type_dict:
                        check_type('return', result, type_dict['return'])
                except TypeError:
                    print(f'\n_____________________________\nType mismatch : {func.__qualname__} in "return"\nExpected type : {get_args(type_dict["return"])}\nReceived      : Type {type(result)}\n_____________________________\n')
                    sys.exit(1)
                end = time.perf_counter()
                delta = (end - start)
                if save_log:
                    with open(log_file, 'a', encoding='utf-8') as f:
                        f.write(
                            get_time() + f"Function: {func.__qualname__} succeeded with args: {*args, {**kwargs} } - "
                                         f"execution time: {delta} seconds\n")
                else:
                    print(
                        get_time() + f"Function: {func.__qualname__} succeeded with args: {*args, {**kwargs} } - "
                                     f"execution time: {delta} seconds")
                return result
            except Exception as e:
                if errors:
                    if type(e) in [error[0] for error in errors]:
                        error = [error for error in errors if type(e) == error[0]][0]
                        error_type = error[0].__name__
                        error_msg = str(e) if error[1] == '' else error[1]
                        print(f'You got {error_type} error: {error_msg}')
                        if not save_log:
                            print(
                                get_time() + f"Function: {func.__qualname__} failed with args: {*args, {**kwargs} } and error: {e.__repr__()}")
                        else:
                            with open(log_file, 'a', encoding='utf-8') as f:
                                f.write(
                                    get_time() + f"Function: {func.__qualname__} failed with args: {*args, {**kwargs} } and "
                                                 f"error: {e.__repr__()}\n")
                        # sys.exit(1)
                    else:
                        reporting_to_dev_team(e)
                else:
                    if save_log:
                        with open(log_file, 'a', encoding='utf-8') as f:
                            f.write(
                                get_time() + f"Function: {func.__qualname__} failed with args: {*args, {**kwargs} } and "
                                             f"error: {e.__repr__()}\n")
                    else:
                        print(
                            get_time() + f"Function: {func.__qualname__} failed with args: {*args, {**kwargs} } and error: {e.__repr__()}")
                    reporting_to_dev_team(e)
        return wrapper
    return log_wrap


def reporting_to_dev_team(e):
    import sys
    error_type = type(e).__name__
    error_msg = str(e)
    print(f'You got {error_type} error: {error_msg}. Which is undocumented.')
    print("Reporting to Dev")
    sys.exit(1)


def type_checker(func):
    """Checks the types of the arguments and return value and prints an error if there's a mismatch."""
    from typing import get_args
    from functools import wraps
    from typeguard import check_type
    import sys
    @wraps(func)
    def wrapper(*args, **kwargs):
        varnames = list(func.__code__.co_varnames)
        type_dict = func.__annotations__

        if varnames[0] == 'self':
            real_args = args[1:]
            varnames = varnames[1:]
        else:
            real_args = args
        
        try:
            for param, val in kwargs.items():
                check_type(param, val, type_dict[param])
                varnames.remove(param)
        except TypeError:
            print(f'\n_____________________________\nType mismatch : {func.__qualname__} in [{param}]\nExpected type : {get_args(type_dict[param])}\nReceived      : Type {type(val)}\n_____________________________\n')
            sys.exit(1)

        try:
            for param, val in zip(varnames, real_args):
                check_type(param, val, type_dict[param])
        except TypeError:
            print(f'\n_____________________________\nType mismatch : {func.__qualname__} in [{param}]\nExpected type : {get_args(type_dict[param])}\nReceived      : Type {type(val)}\n_____________________________\n')
            sys.exit(1)
    return wrapper


def dostify(errors:list = None, save_log: bool = True, log_file: str = 'pip-log.txt'):
    from functools import wraps
    def decorator_wrap(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            type_checker(func)(*args, **kwargs)
            return try_catch_log_check_output(errors, save_log, log_file) (func)(*args, **kwargs)
        return wrapper
    return decorator_wrap 