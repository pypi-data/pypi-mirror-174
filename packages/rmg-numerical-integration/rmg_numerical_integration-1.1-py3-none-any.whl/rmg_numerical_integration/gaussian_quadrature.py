from scipy.special.orthogonal import p_roots
import numpy as np
import matplotlib.pyplot as plt


def gauss_rule(f, n: int, a: float, b: float) -> float:
    """
    Returns a numerical approximation of the definite integral
    of f between a and b by the Gauss quadrature rule.

    Parameters:
        f(function): function to be integrated
        a(float): low bound
        b(float): upper bound
        n(int): number of iterations of the numerical approximation

    Returns:
        result(float): the numerical approximation of the definite integral

    """

    # Get the points (xn) and weights (wn) from Legendre polynomials
    list_points_weights = p_roots(n)
    points = list_points_weights[0]
    weights = list_points_weights[1]

    # Calculate the approximate sum by using the Gaussian quadrature rule
    result = 0
    for weight, point in zip(weights, points):
        result += weight * f(0.5 * (b - a) * point + 0.5 * (b + a))

    return 0.5 * (b - a) * result

def plot_gauss_quadrature(f, n: int, a: float,
                          b: float) -> None:
    """
    Plots a numerical approximation of the definite integral of f
    between a and b by the Gauss quadrature rule with n iterations.

    Parameters:
        f(function): function to be integrated
        a(float): low bound
        b(float): upper bound
        n(int): number of iterations of the numerical approximation

    Returns:
        result(None): None

    """

    # Define the X and Y of f
    x = np.linspace(a, b, 100)
    y = f(x)

    # Calculate the approximate sum by using the Gauss quadrature rule
    aprox_sum = gauss_rule(f, a, b, n)

    # Initial Values
    [points, weights] = p_roots(n)
    xn = a

    # Plot approximate rectangles
    for i in range(n):
        plt.bar(xn, f(points[i]), width=weights[i], alpha=0.25,
                align='edge', edgecolor='r')
        xn += weights[i]

    # Plot function f
    plt.axhline(0, color='black')  # X-axis
    plt.axvline(0, color='black')  # Y-axis
    plt.plot(x, y)
    plt.title(f'n={n}, aprox_sum={aprox_sum}')