
def bezier(t: float) -> float:
    """ Calculates a bezier curve"""
    assert 0 <= t <= 1
    return t * t * (3.0 - 2.0 * t)
