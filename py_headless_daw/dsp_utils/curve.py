def get_curve_value(start_val: float, end_val: float, curve_ratio: float, curve_power: float, phase: float):
    """
    this is a simple function for producing transition from start_val to end_val with
    different amounts of skewness

    curve_ratio of 0.0 means linear transition.

    anything above 0 up to 1 means slow start and speeding up towards the end,
    1.0 being the extreme case when no linear component is present at all

    the range [-1.0..0] is the exact opposite to the above.

    the curve_power is the power of the x**power function to get the calculate the skewed
    component
    """
    linear_value = start_val + (end_val - start_val) * phase
    if curve_ratio >= 0:
        curve_value = start_val + (end_val - start_val) * (phase ** curve_power)
    else:
        curve_value = start_val + (end_val - start_val) * (1 - (1 - phase) ** curve_power)

    abs_ratio = abs(curve_ratio)

    return linear_value * (1 - abs_ratio) + curve_value * abs_ratio
