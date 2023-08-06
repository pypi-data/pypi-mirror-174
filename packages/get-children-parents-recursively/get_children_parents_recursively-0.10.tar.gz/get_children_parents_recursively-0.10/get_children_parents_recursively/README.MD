#### A function to fetch all children/parents from an object/list of objects recursively

```python
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
```
