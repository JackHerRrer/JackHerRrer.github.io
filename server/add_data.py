import re
import os

# get absolute path of the script 
script_path = os.path.abspath(__file__)

# get dir of the script
script_dir = os.path.dirname(script_path)

# use script dir has base path for the data file, that way the script can be launched from anywhere
data_file = f'{script_dir}/../data/data.js'

def add_data(time:int, density:int, temperature:float, battery:float, angle:float):
  """Add a time and density value to the first dataset of data.js

  Args:
      time (int): the date in unix time to add
      density (int): the density to add
  """

  # Read in the file
  with open(data_file, 'r') as file:
    filedata = file.read()

  # Add the time to the first data set found in the file 
  regex = r"(time.*)\],?"
  subst = f"\\g<1>{time}, ],"
  result = re.sub(regex, subst, filedata, 1, re.MULTILINE)

  # Add the density to the first data set found in the file 
  regex2 = r"(density.*)\],?"
  subst2 = f"\\g<1>{density}, ],"
  result2 = re.sub(regex2, subst2, result, 1, re.MULTILINE)

  # Add the temperature to the first data set found in the file 
  regex3 = r"(temperature.*)\],?"
  subst3 = f"\\g<1>{temperature}, ],"
  result3 = re.sub(regex3, subst3, result2, 1, re.MULTILINE)

  # Add the battery to the first data set found in the file 
  regex4 = r"(battery.*)\],?"
  subst4 = f"\\g<1>{battery}, ],"
  result4 = re.sub(regex4, subst4, result3, 1, re.MULTILINE)

  # Add the angle to the first data set found in the file 
  regex5 = r"(angle.*)\],?"
  subst5 = f"\\g<1>{angle}, ],"
  result5 = re.sub(regex5, subst5, result4, 1, re.MULTILINE)

  # Write the file out again
  with open(data_file, 'w') as file:
    file.write(result5)

def add_dataset():
  
  # Read in the file and turn it to a list of strings
  with open(data_file, 'r') as file:
    lines = file.readlines()

  # The text that will be added
  empty_dataset = """    {
        'comment':'',
        'time': [],
        'density': [],
        'temperature': [],
        'battery': [],
        'angle': [],
    },
"""

  insert_index = lines.index('data = [\n') + 1

  # insert the empty dataset after 'data = ['
  lines.insert(insert_index, empty_dataset)
  print(insert_index)

  with open(data_file, 'w') as file:
    for l in lines:
      file.write(l)
      print(l)


add_dataset()
add_data(1717533700000, 1000, 28.652, 5.33, 88.36)