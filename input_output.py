from random import random
from master_cell import Master_cell
from child_cell import Child_cell
from decimal import Decimal


def format_name(name: str) -> str:
    """Format the given <name> into a new string.

    Args:
        name (str): A string.

    Returns:
        str: A string compose of "Name :<name>".
    """
    return f"<Name :>{name}\n"


def format_notes(notes: str) -> str:
    """Format the given <notes> into a new string without new lines.

    Args:
        notes (str): A string.

    Returns:
        str: A string compose of "<Notes :>'notes'" where 'notes' is the given notes without any new lines.
    """
    one_line_notes = "".join(
        ["\\n" if elem == "\n" else elem for elem in list(notes)])
    return f"<Notes :>{one_line_notes}\n"


def decode_notes(notes_line: str) -> str:
    """Decode the notes_line to get only the name.

    Args:
        notes_line (str): A one line, string.

    Returns:
        str: A string with possibly multiple lines.
    """
    notes = "\n".join(notes_line.split("\\n"))
    return notes


def format_dic(dic: dict, master: bool = False) -> str:
    """Format the given 'dic' into a new string.

    Args:
        dic (dict): A dictionnary
        master (bool, optional): A bool, if False -> "<Values :>" else -> "<Master_Values :>". Default to False.

    Returns:
        str: A string compose of "<Values :>'dic'" or A string compose of "<Master_Values :>'dic'".
    """
    if not master:
        return f"<Values :>{dic}\n"
    return f"<Master_Values :>{dic}\n"


def decode_dic(dic_line: str) -> dict:
    """Decode the dic_line to get the dict.

    Args:
        dic_line (str): A string compose of "{...}"

    Returns:
        dict: A dict with the keys and values of {...}.
    """
    returning_dic = {}
    if ":" not in dic_line and len(dic_line) < 3:
        return returning_dic
    dic_line = dic_line[1:-1]

    lists = [0, 0]
    if "[" in dic_line:
        start = dic_line.index("[")
        stop = dic_line.index("]")
        list_part = dic_line[start:stop + 1]
        lists = list_part.replace("[", "").replace("]", "").split(",")
        lists = [int(char) for char in lists]
        dic_line = dic_line.replace(list_part, "LIST")

    items = dic_line.split(",")
    for item in items:
        item = item.replace(":'", "")
        key, value = item.split(":")
        key = key.strip().replace("'", "")+" :"
        value = value.strip()
        if "Decimal" in value:
            value = value.replace(
                "Decimal(", "").replace(")", "").replace("'", "")
            value = Decimal(value)
        elif "." in value:
            value = value.replace("'", "")
            value = Decimal(value)
        elif "None" in value:
            value = None
        elif "LIST" in value:
            value = lists
        else:
            value = value.replace("'", "")
            value = int(value)

        returning_dic[key] = value

    return returning_dic


def format_decimal(decimal: bool) -> str:
    """Format the given 'decimal' into a new string.

    Args:
        decimal (bool): A boolean.

    Returns:
        str: A string compose of "Decimal_shown :'decimal'".
    """
    return f"<Decimal_shown :>{decimal}\n"


def decode_decimal(decimal: str) -> bool:
    """Get the decimal info and turn it into a bool.

    Args:
        decimal (str): A string of decimal info.

    Returns:
        bool: The bool transcription of the decimal info
    """
    if decimal == "True":
        return True
    return False

def format_value_by_times(value_by_times: bool) -> str:
    """Format the given 'value_by_times' into a new string.
    
    Args:
        group_time (bool): A boolean.
    
    returns:
        str: A string composed of "Value_by_times : value_by_times"""
    return f"<Value_by_times :>{value_by_times}\n"


def format_group_time(group_time: bool) -> str:
    """Format the given 'group_time' into a new string.

    Args:
        group_time (bool): A boolean.

    Returns:
        str: A string compose of "Group_time :'group_time'".
    """
    return f"<Group_time :>{group_time}\n"


def decode_group_time(group_time: str) -> bool:
    """Get the group_time info and turn it into a bool.

    Args:
        group_time (str): A string of group_time info.

    Returns:
        bool: The bool transcription of the group_time info
    """
    if group_time == "True":
        return True
    return False


def format_added_random(random: bool) -> str:
    """Format the given 'group_time' into a new string.

    Args:
        group_time (bool): A boolean.

    Returns:
        str: A string compose of "Group_time :'group_time'".
    """
    return f"<Added_random :>{random}\n"


def decode_added_random(random: str) -> bool:
    """Get the group_time info and turn it into a bool.

    Args:
        group_time (str): A string of group_time info.

    Returns:
        bool: The bool transcription of the group_time info
    """
    if random == "True":
        return True
    return False


def format_use_master(use_master: bool) -> str:
    """Format the given 'use_master' into a new string.

    Args:
        use_master (bool): A boolean.

    Returns:
        str: A string compose of "Use_master :'use_master'".
    """
    return f"<Use_master :>{use_master}\n"


def decode_use_master(use_master: str) -> bool:
    """Get the use_master info and turn it into a bool.

    Args:
        use_master (str): A string of use_master info.

    Returns:
        bool: The bool transcription of the use_master info
    """
    if use_master == "True":
        return True
    return False


def format_master(master: Master_cell) -> str:
    """Format all the 'master' info into a string.

    Args:
        master (Master_cell): A 'Master_cell' object.

    Returns:
        str: A string with the formated info of 'master'.
    """
    return format_dic(master.value_dict)


def decode_master(master_lines: str) -> dict:
    """Decode the master_lines and get the info.

    Args:
        master_lines (str): A visual representation of a dict.

    Returns:
        dict: A dict with all the master_lines info.
    """
    master_lines = master_lines.replace("<Values :>", "")
    return decode_dic(master_lines)


def format_child(child: Child_cell) -> str:
    """Format all the 'child' info into a string.

    Args:
        child (Child_cell): A 'Child_cell' object.

    Returns:
        str: A string with the formated info of 'child'.
    """
    return_string = ""
    return_string += format_name(child.name)
    return_string += format_notes(child.notes)
    return_string += format_dic(child.value_dict)
    return_string += format_dic(child.master_current_value, True)
    return_string += format_decimal(child.decimal_shown)
    return_string += format_added_random(child.random)
    return_string += format_use_master(child.use_master_time)
    return_string += format_group_time(child.group_times)
    return_string += format_value_by_times(child.value_by_times)
    return return_string


def decode_child(name: str, notes_line: str, values_line: str, master_values_line: str, decimal: str, random: str, use_master: str, group_time: str) -> list:
    """Decode all the strings relative to the child and get the infos.

    Args:
        name (str): A string of name info.
        notes_line (str): A string of notes_line info.
        values_lines (str): A string of values_lines info, compose of "{...}".
        master_values_line (str): A string of master_values_line info, compose of "{...}".
        decimal (str): A string of decimal info.
        use_master (str): A string of use_master info.
        group_time (str): A string of group_time info.

    Returns:
        list: A list with all the info retrieved from the arguments.
    """
    child_info = []

    child_info.append(name)
    child_info.append(decode_notes(notes_line))
    child_info.append(decode_dic(values_line))
    child_info.append(decode_dic(master_values_line))
    child_info.append(decode_decimal(decimal))
    child_info.append(decode_added_random(random))
    child_info.append(decode_use_master(use_master))
    child_info.append(decode_group_time(group_time))

    return child_info


def format_all(master: Master_cell, children_list: list[Child_cell], seed: int, existing_random: dict, randoms_cells: dict) -> str:
    """Format all the 'master' and 'children_list' info into a single string.

    Args:
        master (Master_cell): A 'Master_cell' object.
        children_list (list[Child_cell]): A list of 'Child_cell' objects.
        seed (int): The seed to generate random value

    Returns:
        str: A string with the formated info of 'master' followed be the formated info of each child.
    """
    return_string = f"<Seed>{seed}</Seed>\n"
    return_string += f"<Randoms>{existing_random}</Randoms>\n"
    return_string += "<Master>\n"
    return_string += format_master(master)
    return_string += "</Master>\n"
    for child in children_list:
        return_string += "<Child>\n"
        return_string += format_child(child)
        return_string += "</Child>\n"

    return return_string


def decode_all(list_of_lines: list[str]) -> list[dict, list[dict, str]]:
    """Decode all the info given in the lines.

    Args:
        list_of_lines (list[str]): A lists of lines.

    Returns:
        list[dict,list[dict,str]]: A list containing the info of the master_cell + possible child_cell.
    """
    file = "".join(list_of_lines)
    file = file.replace("\n", "").replace("<Seed>", "")
    seed, rest = file.replace("<Randoms>", "").split("</Seed>")
    randoms, rest = rest.replace("<Master>", "").split("</Randoms>")
    master_line, children_list_part = rest.split("</Master>")
    # The first elem of this list would be an empty elem, we don't want it
    children_list_lines = children_list_part.replace(
        "</Child>", "").split("<Child>")[1::]

    info_list = [int(seed), decode_dic(randoms), decode_master(master_line)]
    children_list = []
    for child in children_list_lines:
        child = child[8::]
        name, rest_of_info = child.split("<Notes :>")
        notes_line, rest_of_info = rest_of_info.split("<Values :>")
        values_line, rest_of_info = rest_of_info.split("<Master_Values :>")
        master_values_line, rest_of_info = rest_of_info.split(
            "<Decimal_shown :>")
        decimal, rest_of_info = rest_of_info.split("<Added_random :>")
        random, rest_of_info = rest_of_info.split("<Use_master :>")
        use_master, group_time = rest_of_info.split("<Group_time :>")

        children_list.append(decode_child(
            name, notes_line, values_line, master_values_line, decimal, random, use_master, group_time))
    info_list.append(children_list)

    return info_list
