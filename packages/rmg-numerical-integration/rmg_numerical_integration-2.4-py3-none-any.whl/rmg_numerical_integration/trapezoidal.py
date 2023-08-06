import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon


def trapezoidal_rule(f, a: float, b: float,
                     n: int) -> float:
    """
    Returns a numerical approximation of the definite integral of f
    between a and b by the trapezoidal rule.

    Parameters:
        f(function): function to be integrated
        a(float): low bound
        b(float): upper bound
        n(int): number of iterations of the numerical approximation

    Returns:
        result(float): the numerical approximation of the definite integral

    """

    # Definition of step and the result
    step = (b - a)/n
    result = 0

    # Moving Variables in X-axis
    xn = a
    xn_1 = xn + step

    # Sum of y-pairs
    for i in range(n):
        result += f(xn) + f(xn_1)

        xn += step
        xn_1 += step

    return (step/2) * result


def plot_trapezoidal_rule(f, a: float, b: float,
                          n: int) -> None:

    """
    Plots a numerical approximation of the definite integral of f
    between a and b by the trapezoidal rule with n iterations.

    Parameters:
        f(function): function to be integrated
        a(float): low bound
        b(float): upper bound
        n(int): number of iterations of the numerical approximation

    Returns:
        result(None): None

    """

    # Define the X and Y of f
    X = np.linspace(a, b, 100)
    Y = f(X)

    # Plot Size
    plt.figure(figsize=(15, 6))

    # Calculate the approximate sum by using the trapezoidal rule
    aprox_sum = trapezoidal_rule(f, a, b, n)
    step = (b-a)/n

    # Initial Values
    i = a
    trapezoidal_list = []

    # Create trapezoids to approximate the area
    for _ in range(n):

        P1 = (i, 0)
        P2 = (i + step, 0)
        P3 = (i, f(i))
        P4 = (i + step, f(i + step))

        trapezoidal_list.append([[P1, P2, P4, P3]])

        i += step

    # Plot created trapezoids
    for trapezoid in trapezoidal_list:
        polygon = Polygon(trapezoid[0])
        x1, y1 = polygon.exterior.xy
        plt.plot(x1, y1, c="red")
        plt.fill(x1, y1, "y")

    # Plot function f
    plt.plot(X, Y, 'g')
    plt.title(f'n={n}, aprox_sum={aprox_sum}')