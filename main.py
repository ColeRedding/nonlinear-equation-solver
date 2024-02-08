import tkinter as tk
import math


def solve_equation():
    equation = equation_entry.get()
    method = method_var.get()
    stopping_criterion = stopping_criterion_var.get()
    threshold = float(threshold_entry.get())
    start_value_1 = float(start_value_1_entry.get())

    result, iterations = None, None

    if method == 'Bisection':
        result, iterations = bisection(start_value_1, float(start_value_2_entry.get()), threshold, stopping_criterion, equation)
    elif method == 'False Position':
        result, iterations = false_position(start_value_1, float(start_value_2_entry.get()), threshold, stopping_criterion, equation)
    elif method == 'Secant':
        result, iterations = secant(start_value_1, float(start_value_2_entry.get()), threshold, equation, stopping_criterion)
    elif method == 'Newton':
        result, iterations = newton(start_value_1, threshold, equation, stopping_criterion)
    else:
        output_label.config(text="Invalid Method")
        return

    if result is not None and iterations is not None:
        true_error = abs(eval(equation.replace('(x)', str(result))))
        output_label.config(text=f"Root: {result}\nTrue Error: {true_error}\nNumber of Iterations: {iterations}")
    else:
        output_label.config(text="Error: Unable to compute.")


def bisection(x1, x2, delta, flag, equation):
    x3 = 0
    x4 = 0
    iterations = 0
    error = 1

    equation = equation.replace('^', '**')
    func = lambda x: eval(equation.replace('(x)', str(x)))
    while error > delta:
        if func(x1) * func(x2) < 0:
            iterations += 1
            x3 = (x1 + x2) / 2
            if func(x3) == 0:
                return x3, iterations
            else:
                if func(x1) * func(x3) < 0:
                    x2 = x3
                    x4 = x1
                else:
                    x1 = x3
                    x4 = x2
            if flag == 1:
                error = abs(x3 - x4)
            elif flag == 2:
                error = abs(x3 - x4) / abs(x3)
            elif flag == 3:
                error = abs(func(x3))
            else:
                output_label.config(text="Error: Invalid flag choice made.")
    return x3, iterations


def false_position(x1, x2, delta, flag, equation):
    x = 0
    iterations = 0
    error = 1
    equation = equation.replace('^', '**')
    func = lambda x: eval(equation.replace('(x)', str(x)))
    x = x2
    x3 = 0
    while error > delta:
        iterations += 1
        x3 = x2 - (func(x2) * (x1 - x2)) / (func(x1) - func(x2))
        if func(x3) == 0:
            return x3, iterations
        if func(x1) * func(x3) < 0:
            x2 = x3
        else:
            x1 = x3
        if flag == 1:
            error = abs(x - x3)
        elif flag == 2:
            error = abs(x - x3) / abs(x3)
        elif flag == 3:
            error = abs(func(x3))
        else:
            output_label.config(text="Error: Invalid flag choice made.")
        x = x2
    return x3, iterations


def secant(x0, x1, delta, equation, flag):
    x2 = 0
    iterations = 0
    error = 1
    equation = equation.replace('^', '**')
    func = lambda x: eval(equation.replace('(x)', str(x)))
    while error > delta:
        iterations += 1
        x2 = x1 - (func(x1) * ((x0 - x1) / (func(x0) - func(x1))))
        x0 = x1
        x1 = x2
        if func(x2) == 0:
            return x2, iterations
        if flag == 1:
            error = abs(x0 - x1)
        elif flag == 2:
            error = abs(x0 - x1) / abs(x1)
        elif flag == 3:
            error = abs(func(x1))
        else:
            output_label.config(text="Error: Invalid flag choice made.")
    return x1, iterations


def derivative(func, x, h=0.0001):
    return (func(x + h) - func(x)) / h


def newton(x0, delta, equation, flag):
    max_iter = 99
    equation = equation.replace('^', '**')
    func = lambda x: eval(equation.replace('(x)', str(x)))

    def f(x):
        return func(x)

    x_n = x0
    count = 0
    while count < max_iter:
        f_val = f(x_n)
        f_prime_val = derivative(f, x_n)
        x_n1 = x_n - f_val / f_prime_val
        if flag == 1:
            approximate_error = abs(x_n1 - x_n)
            count += 1
            if approximate_error < delta:
                x_n = x_n1
                break
        elif flag == 2:
            approximate_error = abs(x_n1 - x_n) / abs(x_n1)
            count += 1
            if approximate_error < delta:
                x_n = x_n1
                break
        elif flag == 3:
            true_absolute_error = abs(f_val / f_prime_val)
            count += 1
            if true_absolute_error < delta:
                x_n = x_n1
                break
        else:
            output_label.config(text="Error: Invalid flag choice made.")
        x_n = x_n1
    return x_n, count

# GUI Setup


root = tk.Tk()
root.title("Nonlinear Equation Solver")

equation_label = tk.Label(root, text="Enter Equation:")
equation_label.pack()
equation_entry = tk.Entry(root)
equation_entry.pack()

method_label = tk.Label(root, text="Choose Method:")
method_label.pack()
method_var = tk.StringVar()
method_var.set("Bisection")
method_options = ['Bisection', 'False Position', 'Secant', 'Newton']
method_dropdown = tk.OptionMenu(root, method_var, *method_options)
method_dropdown.pack()

stopping_criterion_label = tk.Label(root, text="Choose Stopping Criterion:")
stopping_criterion_label.pack()
stopping_criterion_var = tk.IntVar()
stopping_criterion_var.set(1)
stopping_criterion_options = [1, 2, 3]
stopping_criterion_dropdown = tk.OptionMenu(root, stopping_criterion_var, *stopping_criterion_options)
stopping_criterion_dropdown.pack()

threshold_label = tk.Label(root, text="Enter Threshold:")
threshold_label.pack()
threshold_entry = tk.Entry(root)
threshold_entry.pack()

start_value_1_label = tk.Label(root, text="Enter Start Value 1:")
start_value_1_label.pack()
start_value_1_entry = tk.Entry(root)
start_value_1_entry.pack()

start_value_2_label = tk.Label(root, text="Enter Start Value 2:")
start_value_2_label.pack()
start_value_2_entry = tk.Entry(root)
start_value_2_entry.pack()

solve_button = tk.Button(root, text="Solve", command=solve_equation)
solve_button.pack()

output_label = tk.Label(root, text="")
output_label.pack()

root.mainloop()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
