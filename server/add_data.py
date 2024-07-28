import re

def add_data(time:int, density:int):
  """Add a time and density value to the first dataset of data.js

  Args:
      time (int): the date in unix time to add
      density (int): the density to add
  """

  # Read in the file
  with open('data/data.js', 'r') as file:
    filedata = file.read()

  # Add the time to the first data set found in the file 
  regex = r"(time.*)\],?"
  subst = f"\\g<1>{time}, ],"
  result = re.sub(regex, subst, filedata, 1, re.MULTILINE)

  # Add the density to the first data set found in the file 
  regex2 = r"(density.*)\],?"
  subst2 = f"\\g<1>{density}, ],"
  result2 = re.sub(regex2, subst2, result, 1, re.MULTILINE)

  # Write the file out again
  with open('data/data.js', 'w') as file:
    file.write(result2)

def add_dataset():
  
  # Read in the file and turn it to a list of strings
  with open('data/data.js', 'r') as file:
    lines = file.readlines()

  # The text that will be added
  empty_dataset = """    {
        'comment':'',
        'time': [],
        'density': [],
    },
"""

  insert_index = lines.index('data = [\n') + 1

  # insert the empty dataset after 'data = ['
  lines.insert(insert_index, empty_dataset)
  print(insert_index)

  with open('data/data.js', 'w') as file:
    for l in lines:
      file.write(l)
      print(l)


add_dataset()
add_data(1717533700000, 1000)