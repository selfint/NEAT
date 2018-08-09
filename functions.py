# functions.py
# Globally useful functions.
# --------------------------

from typing import List, Any, Union

def ignore(array: List[Any], *items: Any) -> List[Any]:
    """
    Returns list without all items in items argument.
    :param array: List to ignore items from
    :param items: Items to ignore in list
    :return: List without items
    """
    return [element for element in array if element not in items]

def flatten(array: List[Union[list, range, set, str]]) -> list:
    """
    Flattens a 2D array into a 1D array.
    :param array: 2D array to flatten
    :return: Flattened 1D array
    """
    return [element for sub_list in array for element in sub_list]


if __name__ == '__main__':
    
    # Test ignore function
    temp = list(range(20))
    print('IGNORE FUNCTION')
    print(temp)
    print(ignore(temp, 1, 2, 5, 6))
    
    # Test flatten function
    print('\nFLATTEN FUNCTION')
    temp = [list(range(10)) for _ in range(3)]
    print(temp)
    print(flatten(temp))
