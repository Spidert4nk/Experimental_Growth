from decimal import Decimal
import decimal

decimal.setcontext(decimal.Context(150))


def format_result(result: str) -> str:
    """Format the result by adding "," to the right place.

    Args:
        result (str): A string.

    Returns:
        str: The same string with "," at the right place
    """
    # This means that the exponent symbol shows up.
    if "E" in result:
        # Currently the result is an int with a lot of decimal and the exponent symbol at the end.
        # This can be ennoying if the "see decimal" checkbox is not checked.
        current_int, decimal = result.split(".")
        real_decimal, exponent = decimal.split("E")
        # We combine the single int with all is decimal
        integer = f"{current_int}{real_decimal}"
        # We decrease the value of the exponent by the length of the decimal
        exponent = int(exponent) - len(real_decimal)

        integer_copy = integer[::-1]
        new_integer = []

        while len(integer_copy) > 3:
            new_integer.append(integer_copy[0:3])
            integer_copy = integer_copy[3:]

        new_integer.append(integer_copy[0:3])
        new_integer = ",".join(new_integer)[::-1]
        # Now we just have a big integer with the exponent symbol at the end, so we're able to
        # see it completly without the need to check the "see decimal" checkbox.
        return f"{new_integer}E+{exponent}"

    elif "." in result:
        integer, decimal = result.split(".")

        integer_copy = integer[::-1]
        new_integer = []

        while len(integer_copy) > 3:
            new_integer.append(integer_copy[0:3])
            integer_copy = integer_copy[3:]

        new_integer.append(integer_copy[0:3])
        new_integer = ",".join(new_integer)[::-1]

        return f"{new_integer}.{decimal}"
    else:
        return result


def more_accurate_results(
    master_time: int,
    master_start_value: Decimal,
    master_growth_value: Decimal,
    master_add_value: Decimal,
    time: Decimal,
    start_value: Decimal,
    growth_value: Decimal,
    add_value: Decimal,
    use_master_time: bool,
    group_cell: bool,
    value_by_times: bool,
) -> str:
    """[summary]

    Args:
        master_time (int): An int representing the value of the 'time' in the Master_cell.
        master_start_value (Decimal): A Decimal Object representing the value of the 'starting value' in the Master_cell.
        master_growth_value (Decimal): A Decimal Object representing the value of the 'growth rate' in the Master_cell.
        master_add_value (Decimal): A Decimal Object representing the value of the 'added value' in the Master_cell.
        time (Decimal): An int representing the value of the 'time' in the Child_cell.
        start_value (Decimal): A Decimal Object representing the value of the 'starting value' in the Child_cell.
        growth_value (Decimal): A Decimal Object representing the value of the 'growth rate' in the Child_cell.
        add_value (Decimal): A Decimal Object representing the value of the 'added value' in the Child_cell.

    Returns:
        str: A string representing the result. This string is being formated by format_result() before being return.
    """
    times = Decimal(time)
    if use_master_time:
        times += Decimal(master_time)

    added = Decimal(master_add_value) + Decimal(add_value)
    #if group_cell: #This should be called "if times_additive" since that's what it's doing. Make a new condition and repurpose this one? Leave group_cell alone
    #    added *= times
    
    if value_by_times:
        added *= times

    starts = Decimal(master_start_value) + Decimal(start_value)
    growths = (
        1+((Decimal(master_growth_value) + Decimal(growth_value))/100)
    )

    result = Decimal(added) + (
        Decimal(starts) * (Decimal(growths)
                           ** Decimal(times)))

    return format_result(str(result))
