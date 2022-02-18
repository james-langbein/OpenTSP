import math


def combinations_calculator(n, r=1):
    """Calculates number of combinations."""
    return int((math.factorial(n)) / (math.factorial(r) * math.factorial(n - r)))


def permutations_calculator(n, r=1):
    """Returns the full range of permutations for the instance's edges. This is used by the solve method to exhaust
    the permutations generator without going over the maximum number of permutations."""
    return int((math.factorial(n)) / (math.factorial(n - r)))


def angle(vertex, start, dest):
    """Calculates the signed angle between two edges with the same origin. Origin is the 'vertex' argument, 'start' is
    the end of the edge to calculate the angle from.
    Positively signed result means anti-clockwise rotation about the vertex."""
    def calc_radians(ab):
        if ab > math.pi:
            return ab + (-2 * math.pi)
        else:
            if ab < 0 - math.pi:
                return ab + (2 * math.pi)
            else:
                return ab + 0

    AhAB = math.atan2((dest.y - vertex.y), (dest.x - vertex.x))
    AhAO = math.atan2((start.y - vertex.y), (start.x - vertex.x))
    AB = AhAB - AhAO
    res = calc_radians(AB)
    # in between 0 - math.pi = do nothing, more than math.pi = +(-2 * math.pi), less than zero = do nothing
    # below is calc_radians() as a one-liner:
    # AB = math.degrees(AB + (-2 * math.pi if AB > math.pi else (2 * math.pi if AB < 0 - math.pi else 0)))

    return math.degrees(res)
