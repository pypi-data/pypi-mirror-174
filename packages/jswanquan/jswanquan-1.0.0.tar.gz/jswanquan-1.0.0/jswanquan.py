"""This is a standard way to include a multiple-line comment in your code."""
def print_lol(the_list):
    """if there is a list in a list as an item,you can use this jswanquan."""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)
