from functions import flatten,ignore

def test_flatten2D():
    temp = [list(range(10)) for _ in range(3)]
    assert all(not isinstance(i, list) for i in flatten(temp))

def test_ignore():
    full_list = list(range(20))
    ignored_items = ( 1, 2, 5, 6 )
    assert all(i not in ignored_items for i in ignore(
        full_list, *ignored_items))
