"""This file contains functions to solve equations."""

def dichotomy(f, x_min, x_max, args_before_x=[], args_after_x=[], accuracy=-3):
    """Search the x value to obtain f(x)=0 with an accuracy of 10^(accuracy).
    
    This function is based on the dichotomous algorithm.

    function is a function with at least one argument x. f must be a continuous function (in the mathematical sense) and must be strictly monotone. f(x_min) and f(x_max) must have different signs (one positive and one negative).
    args_before_x is the list of positional arguments before the variable argument's position
    args_after_x is the list of positional arguments after the variable argument's position
    The value of the variable argument x varies from min_x to max_variable
    """
    a = x_min
    f_a = f(*args_before_x, a, *args_after_x)
    b = x_max
    f_b = f(*args_before_x, b, *args_after_x)

    if f_a*f_b  > 0 :
        #f=0 can have no solution (under the hypothesis of continuous function and strictly monotone function)
        x = None
    #because f is strictly monotone, f_a != f_b, in particular f_a = f_b = 0 is not possible
    elif f_a == 0 :
        x = a
    elif f_b == 0 :
        x = b
    else :
        while b-a > 10**accuracy :
            m = a + (b-a)/2
            f_a = f(*args_before_x, a, *args_after_x)
            f_m = f(*args_before_x, m, *args_after_x)
            if f_m == 0 :
                break
            elif f_a*f_m > 0 :
                a = m
            else :
                b = m
        x = a + (b-a)/2
    return x
    