from typing import Any

from flatten_any_dict_iterable_or_whatsoever import fla_tu
from flatten_everything import flatten_everything, ProtectedDict


def get_attr_loop(obj, func=None, parent=None):
    try:
        yield from get_attr_loop(getattr(obj, func)(), func, parent=obj)

    except Exception:

        pass
    if isinstance(obj, list):
        for o in obj:
            yield from get_attr_loop(obj=o, func=func, parent=None)
    yield ProtectedDict({"item": parent, func: obj})


def read_and_flatten_all(
    allitems,
    delete_duplicates=True,
    flatten_all=True,
    normalize_children_list=False,
    children_method="children",
):
    if not isinstance(allitems, list):
        if isinstance(allitems, tuple):
            allitems = list(allitems)
        else:
            allitems = [allitems]
    allchildrenlist = []
    for va in allitems:
        if len(va) == 2:
            androidchildren = get_attr_loop(va[0], va[1])
        else:
            androidchildren = get_attr_loop(va[0], None)
        allchildrenlist.append(list(androidchildren).copy())

    allitems = list(flatten_everything(allchildrenlist))
    allitems = [x for x in allitems if x["item"] is not None]
    if normalize_children_list:
        maxlenlist = max([len(x[children_method]) for x in allitems])
        _ = [
            x.__setitem__(
                children_method,
                x.get(children_method)
                + ([None] * (maxlenlist - len(x.get(children_method)))),
            )
            for x in allitems
        ]

    if delete_duplicates:
        allitems = [
            y[1]
            for y in {
                repr(v) + str(v): v for v in list(flatten_everything(allitems))
            }.items()
        ]
    if flatten_all:
        allitems = [x[0] for x in list(fla_tu(allitems))]
        if delete_duplicates:
            allitems = [
                y[1]
                for y in {
                    repr(v) + str(v): v for v in list(flatten_everything(allitems))
                }.items()
            ]
    return allitems


def get_all_children_parents_recursively(
    item: Any,
    children_parents_method: str = "children",
    delete_duplicates: bool = True,
    flatten_all: bool = False,
    normalize_children_list: bool = False,
) -> list:
    r"""
    $pip install get-children-parents-recursively
    from get_children_parents_recursively import get_all_children_parents_recursively
    import psutil #lets use psutil as an example

    item = psutil.Process(15328) #'chrome.exe'

    test1 = get_all_children_parents_recursively(
        item,
        children_parents_method="children",
        delete_duplicates=False,
        flatten_all=False,
        normalize_children_list=False,
    )

    test1
    Out[3]:
    [{'item': psutil.Process(pid=3660, name='chrome.exe', status='running', started='23:49:19'),
      'children': []},
     {'item': psutil.Process(pid=9664, name='chrome.exe', status='running', started='23:49:19'),
      'children': []},
     {'item': psutil.Process(pid=16444, name='chrome.exe', status='running', started='23:49:19'),
      'children': []},
     {'item': psutil.Process(pid=14144, name='chrome.exe', status='running', started='23:49:19'),
      'children': []},
     {'item': psutil.Process(pid=18376, name='chrome.exe', status='running', started='23:49:19'),
      'children': []},
     {'item': psutil.Process(pid=7160, name='chrome.exe', status='running', started='23:49:21'),
      'children': []},
     {'item': psutil.Process(pid=15328, name='chrome.exe', status='running', started='23:49:19'),
      'children': [psutil.Process(pid=3660, name='chrome.exe', status='running', started='23:49:19'),
       psutil.Process(pid=9664, name='chrome.exe', status='running', started='23:49:19'),
       psutil.Process(pid=16444, name='chrome.exe', status='running', started='23:49:19'),
       psutil.Process(pid=14144, name='chrome.exe', status='running', started='23:49:19'),
       psutil.Process(pid=18376, name='chrome.exe', status='running', started='23:49:19'),
       psutil.Process(pid=7160, name='chrome.exe', status='running', started='23:49:21')]}]


    test2 = get_all_children_parents_recursively(
        item,
        children_parents_method="children",
        delete_duplicates=True,
        flatten_all=False,
        normalize_children_list=False,
    )

    test2
    Out[4]:
    [{'item': psutil.Process(pid=3660, name='chrome.exe', status='running', started='23:49:19'),
      'children': []},
     {'item': psutil.Process(pid=9664, name='chrome.exe', status='running', started='23:49:19'),
      'children': []},
     {'item': psutil.Process(pid=16444, name='chrome.exe', status='running', started='23:49:19'),
      'children': []},
     {'item': psutil.Process(pid=14144, name='chrome.exe', status='running', started='23:49:19'),
      'children': []},
     {'item': psutil.Process(pid=18376, name='chrome.exe', status='running', started='23:49:19'),
      'children': []},
     {'item': psutil.Process(pid=7160, name='chrome.exe', status='running', started='23:49:21'),
      'children': []},
     {'item': psutil.Process(pid=15328, name='chrome.exe', status='running', started='23:49:19'),
      'children': [psutil.Process(pid=3660, name='chrome.exe', status='running', started='23:49:19'),
       psutil.Process(pid=9664, name='chrome.exe', status='running', started='23:49:19'),
       psutil.Process(pid=16444, name='chrome.exe', status='running', started='23:49:19'),
       psutil.Process(pid=14144, name='chrome.exe', status='running', started='23:49:19'),
       psutil.Process(pid=18376, name='chrome.exe', status='running', started='23:49:19'),
       psutil.Process(pid=7160, name='chrome.exe', status='running', started='23:49:21')]}]


    test3 = get_all_children_parents_recursively(
        item,
        children_parents_method="children",
        delete_duplicates=True,
        flatten_all=True,
        normalize_children_list=False,
    )

    test3
    Out[5]:
    [psutil.Process(pid=3660, name='chrome.exe', status='running', started='23:49:19'),
     psutil.Process(pid=9664, name='chrome.exe', status='running', started='23:49:19'),
     psutil.Process(pid=16444, name='chrome.exe', status='running', started='23:49:19'),
     psutil.Process(pid=14144, name='chrome.exe', status='running', started='23:49:19'),
     psutil.Process(pid=18376, name='chrome.exe', status='running', started='23:49:19'),
     psutil.Process(pid=7160, name='chrome.exe', status='running', started='23:49:21'),
     psutil.Process(pid=15328, name='chrome.exe', status='running', started='23:49:19')]


    test3 = get_all_children_parents_recursively(
        item,
        children_parents_method="children",
        delete_duplicates=False,
        flatten_all=True,
        normalize_children_list=False,
    )
    test3
    Out[10]:
    [psutil.Process(pid=3660, name='chrome.exe', status='running', started='23:49:19'),
     psutil.Process(pid=9664, name='chrome.exe', status='running', started='23:49:19'),
     psutil.Process(pid=16444, name='chrome.exe', status='running', started='23:49:19'),
     psutil.Process(pid=14144, name='chrome.exe', status='running', started='23:49:19'),
     psutil.Process(pid=18376, name='chrome.exe', status='running', started='23:49:19'),
     psutil.Process(pid=7160, name='chrome.exe', status='running', started='23:49:21'),
     psutil.Process(pid=15328, name='chrome.exe', status='running', started='23:49:19'),
     psutil.Process(pid=3660, name='chrome.exe', status='running', started='23:49:19'),
     psutil.Process(pid=9664, name='chrome.exe', status='running', started='23:49:19'),
     psutil.Process(pid=16444, name='chrome.exe', status='running', started='23:49:19'),
     psutil.Process(pid=14144, name='chrome.exe', status='running', started='23:49:19'),
     psutil.Process(pid=18376, name='chrome.exe', status='running', started='23:49:19'),
     psutil.Process(pid=7160, name='chrome.exe', status='running', started='23:49:21')]



    test4 = get_all_children_parents_recursively(
        item,
        children_parents_method="children",
        delete_duplicates=True,
        flatten_all=False,
        normalize_children_list=True,
    )



    test4
    Out[6]:
    [{'item': psutil.Process(pid=3660, name='chrome.exe', status='running', started='23:49:19'),
      'children': [None, None, None, None, None, None]},
     {'item': psutil.Process(pid=9664, name='chrome.exe', status='running', started='23:49:19'),
      'children': [None, None, None, None, None, None]},
     {'item': psutil.Process(pid=16444, name='chrome.exe', status='running', started='23:49:19'),
      'children': [None, None, None, None, None, None]},
     {'item': psutil.Process(pid=14144, name='chrome.exe', status='running', started='23:49:19'),
      'children': [None, None, None, None, None, None]},
     {'item': psutil.Process(pid=18376, name='chrome.exe', status='running', started='23:49:19'),
      'children': [None, None, None, None, None, None]},
     {'item': psutil.Process(pid=7160, name='chrome.exe', status='running', started='23:49:21'),
      'children': [None, None, None, None, None, None]},
     {'item': psutil.Process(pid=15328, name='chrome.exe', status='running', started='23:49:19'),
      'children': [psutil.Process(pid=3660, name='chrome.exe', status='running', started='23:49:19'),
       psutil.Process(pid=9664, name='chrome.exe', status='running', started='23:49:19'),
       psutil.Process(pid=16444, name='chrome.exe', status='running', started='23:49:19'),
       psutil.Process(pid=14144, name='chrome.exe', status='running', started='23:49:19'),
       psutil.Process(pid=18376, name='chrome.exe', status='running', started='23:49:19'),
       psutil.Process(pid=7160, name='chrome.exe', status='running', started='23:49:21')]}]

       #useful for pandas
       from a_pandas_ex_plode_tool import pd_add_explode_tools
        import pandas as pd
        pd_add_explode_tools()
        df = pd.DataFrame(test4)
        df = pd.concat([df.item, df.children.s_explode_lists_and_tuples()], axis=1)
       df
        Out[7]:
                                                        item  ...                                         children_5
        0  psutil.Process(pid=3660, name='chrome.exe', st...  ...                                               None
        1  psutil.Process(pid=9664, name='chrome.exe', st...  ...                                               None
        2  psutil.Process(pid=16444, name='chrome.exe', s...  ...                                               None
        3  psutil.Process(pid=14144, name='chrome.exe', s...  ...                                               None
        4  psutil.Process(pid=18376, name='chrome.exe', s...  ...                                               None
        5  psutil.Process(pid=7160, name='chrome.exe', st...  ...                                               None
        6  psutil.Process(pid=15328, name='chrome.exe', s...  ...  psutil.Process(pid=7160, name='chrome.exe', st...


    import requests
    import bs4
    soup = bs4.BeautifulSoup(requests.get("http://www.github.com").content, "lxml")
    test5 = get_all_children_parents_recursively(
        soup.find_all("body")[0],
        children_parents_method="find_parents",
        delete_duplicates=True,
        flatten_all=False,
        normalize_children_list=False,
    )

    item        :  <!DOCTYPE html> <html data-a11y-animated-images="s
    find_parents:  []
    item        :  <html data-a11y-animated-images="system" lang="en"
    find_parents:  [<!DOCTYPE html> <html data-a11y-animated-images="
    item        :  <body class="logged-out env-production page-respon
    find_parents:  [<html data-a11y-animated-images="system" lang="en

        Parameters:
            item:Any
                any object that can be recursively iterate
            children_parents_method:str
                name of the method that gets the children/parents item
                (default="children")
            delete_duplicates:bool=True
                Useful if you use flatten_all=True
                default=True)

            flatten_all:bool=False
                Returns all items as a flattened list
                default=False)

            normalize_children_list:bool=False
                Useful if you don't want to flatten the output and want the same length for
                every children list (e.g. for creating a DataFrame)
                (default=False)
        Returns:
            readyitems:list

    """

    allitems = [[x[0], children_parents_method] for x in (fla_tu([item]))]
    readyitems = read_and_flatten_all(
        allitems,
        delete_duplicates=delete_duplicates,
        flatten_all=flatten_all,
        normalize_children_list=normalize_children_list,
        children_method=children_parents_method,
    )
    return readyitems
