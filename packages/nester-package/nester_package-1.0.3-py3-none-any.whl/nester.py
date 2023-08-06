"""This is the nester.py module and it provides one function called print_list_items Which prints lists that may of may not include nested lists"""
def print_list_items (the_list):
    """This function takes a positional argument called “the_list”, which is any Python list (of possibly, nested lists). Each data item in the provided list is
(recursively) printed to the screen on its own line"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_list_items(each_item)
        else:
            print(each_item)
