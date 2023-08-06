from scipy.special.orthogonal import p_roots
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

def gauss_rule(f, a: float, b: float, n: int) -> float:
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

def plot_gauss_quadrature(f, a: float, b: float, n: int) -> None:
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
    plt.show()

def midpoint_rule(f, a: float, b: float,
                  n: int) -> float:
    """
    Returns a numerical approximation of the definite integral
    of f between a and b by the midpoint rule.

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
        result += f((xn + xn_1)/2)

        xn += step
        xn_1 += step

    return step * result

def plot_midpoint_rule(f, a: float, b: float,
                       n: int) -> None:
    """
    Plots a numerical approximation of the definite integral of f
    between a and b by the midpoint rule with n iterations.

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

    # Calculate the approximate sum by using the midpoint rule
    aprox_sum = midpoint_rule(f, a, b, n)
    step = (b-a)/n

    # Initial Values
    i = a
    midpoint_list = []

    # Create midpoint rectangles to approximate the area
    for _ in range(n):

        P1 = (i, 0)
        P2 = (i + step, 0)
        P3 = (i, f((2*i + step)/2))
        P4 = (i + step, f((2*i + step)/2))

        midpoint_list.append([[P1, P2, P4, P3]])

        i += step

    # Plot created midpoint rectangles
    for midpoint in midpoint_list:
        polygon = Polygon(midpoint[0])
        x1, y1 = polygon.exterior.xy
        plt.plot(x1, y1, c="red")
        plt.fill(x1, y1, "y")

    # Plot function f
    plt.plot(X, Y, 'g')
    plt.title(f'n={n}, aprox_sum={aprox_sum}')
    plt.show()

def leftpoint_rule(f, a: float, b: float,
                  n: int) -> float:
    """
    Returns a numerical approximation of the definite integral
    of f between a and b by the leftpoint rule.

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
        result += f(xn)

        xn += step
        xn_1 += step

    return step * result

def plot_leftpoint_rule(f, a: float, b: float,
                       n: int) -> None:
    """
    Plots a numerical approximation of the definite integral of f
    between a and b by the leftpoint rule with n iterations.

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

    # Calculate the approximate sum by using the leftpoint rule
    aprox_sum = leftpoint_rule(f, a, b, n)
    step = (b-a)/n

    # Initial Values
    i = a
    leftpoint_list = []

    # Create leftpoint rectangles to approximate the area
    for _ in range(n):

        P1 = (i, 0)
        P2 = (i + step, 0)
        P3 = (i, f((2*i + step)/2))
        P4 = (i + step, f((2*i + step)/2))

        leftpoint_list.append([[P1, P2, P4, P3]])

        i += step

    # Plot created leftpoint rectangles
    for leftpoint in leftpoint_list:
        polygon = Polygon(leftpoint[0])
        x1, y1 = polygon.exterior.xy
        plt.plot(x1, y1, c="red")
        plt.fill(x1, y1, "y")

    # Plot function f
    plt.plot(X, Y, 'g')
    plt.title(f'n={n}, aprox_sum={aprox_sum}')
    plt.show()

def rightpoint_rule(f, a: float, b: float,
                  n: int) -> float:
    """
    Returns a numerical approximation of the definite integral
    of f between a and b by the rightpoint rule.

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
        result += f(xn)

        xn += step
        xn_1 += step

    return step * result

def plot_rightpoint_rule(f, a: float, b: float,
                       n: int) -> None:
    """
    Plots a numerical approximation of the definite integral of f
    between a and b by the rightpoint rule with n iterations.

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

    # Calculate the approximate sum by using the rightpoint rule
    aprox_sum = rightpoint_rule(f, a, b, n)
    step = (b-a)/n

    # Initial Values
    i = a
    rightpoint_list = []

    # Create rightpoint rectangles to approximate the area
    for _ in range(n):

        P1 = (i, 0)
        P2 = (i + step, 0)
        P3 = (i, f((2*i + step)/2))
        P4 = (i + step, f((2*i + step)/2))

        rightpoint_list.append([[P1, P2, P4, P3]])

        i += step

    # Plot created rightpoint rectangles
    for rightpoint in rightpoint_list:
        polygon = Polygon(rightpoint[0])
        x1, y1 = polygon.exterior.xy
        plt.plot(x1, y1, c="red")
        plt.fill(x1, y1, "y")

    # Plot function f
    plt.plot(X, Y, 'g')
    plt.title(f'n={n}, aprox_sum={aprox_sum}')
    plt.show()

def simpson_rule(f, a: float, b: float,
                 n: int) -> float:
    """
    Returns a numerical approximation of the definite integral of f
    between a and b by the Simpson rule.

    Parameters:
        f(function): function to be integrated
        a(float): low bound
        b(float): upper bound
        n(int): number of iterations of the numerical approximation

    Returns:
        result(float): the numerical approximation of the definite integral

    """

    assert n % 2 == 0   # to verify that n is even

    # Definition of step and the result
    step = (b - a)/n
    result = f(a) + f(b)          # first and last

    # Moving Variables in X-axis
    xn = a + step

    # Sum of y-pairs
    for i in range(n-1):
        if i % 2 == 0:
            result += 4 * f(xn)
        else:
            result += 2 * f(xn)

        xn += step

    return (step/3) * result


def plot_simpson_rule(f, a: float,
                      b: float, n: int) -> None:

    """
    Plots a numerical approximation of the definite integral of f
    between a and b by Simpson's rule with n iterations.

    Parameters:
        f(function): function to be integrated
        a(float): low bound
        b(float): upper bound
        n(int): number of iterations of the numerical approximation

    Returns:
        result(None): None

    """
    def parabola_from_3(x1, y1, x2, y2, x3, y3):
        """
        Get a, b, c coefficients of a parabola from 3 points (x,y)
        """
        denominator = ((x1-x2) * (x1-x3) * (x2-x3))
        assert denominator != 0

        a = (x3 * (y2-y1) + x2 * (y1-y3) + x1 * (y3-y2))
        b = (x3*x3 * (y1-y2) + x2*x2 * (y3-y1) + x1*x1 * (y2-y3))
        c = (x2*x3 * (x2-x3) * y1 + x3*x1 * (x3-x1) * y2+x1 * x2 * (x1-x2)*y3)

        a, b, c = a/denominator, b/denominator, c/denominator

        return a, b, c

    def f_parabola(x, a_parab, b_parab, c_parab):
        """
        Get the parabola function from a, b, c coefficients
        """
        return a_parab*x**2 + b_parab*x + c_parab

    # Define the X and Y of f
    X = np.linspace(a, b, 100)
    Y = f(X)

    # Plot Size
    plt.figure(figsize=(15, 6))

    # Calculate the approximate sum by using Simpson's rule
    aprox_sum = simpson_rule(f, a, b, n)
    step = (b-a)/n

    # Initial Values
    i = a
    parabola_list = []

    # Create the points of parabolas to approximate the area
    for _ in range(n//2):

        P1 = (i, f(i))
        P2 = (i + 2*step, f(i + 2*step))
        P_mid = (i + step, f(i + step))

        parabola_list.append([[P1, P2, P_mid]])

        i += 2 * step

    # Plot fixed parabolas (separated by "red" bar plot)
    for simpson in parabola_list:
        a_parab, b_parab, c_parab = parabola_from_3(
                        simpson[0][0][0], simpson[0][0][1],
                        simpson[0][1][0], simpson[0][1][1],
                        simpson[0][2][0], simpson[0][2][1])

        x_test = list(np.linspace(simpson[0][0][0], simpson[0][1][0], 100))
        y_test = list()

        for element in x_test:
            y_test.append(f_parabola(element, a_parab, b_parab, c_parab))

        plt.plot(x_test, y_test, c="red")
        plt.bar([simpson[0][0][0],  simpson[0][1][0]],
                [simpson[0][0][1], simpson[0][1][1]],
                width=0.01, color="red")
        plt.fill_between(x_test, y_test, color="yellow")

    # Plot function f
    plt.plot(X, Y, 'g')
    plt.title(f'n={n}, aprox_sum={aprox_sum}')
    plt.show()

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
    plt.show()

