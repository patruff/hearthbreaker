from os import walk
import os

mypath = './hsreplays_xml'
_, _, filenames = next(walk(mypath), (None, None, []))

# get list of files in the directory
print(filenames)

#for index in range(10):
#    for filename in filename:

for filename in filenames:
    with open('xmls_uploaded.txt', 'r') as f:
        found = False
        for x in f.readlines():
            if x == filename: #or x is filename + "\n":
                found = True

        if found == True:
            found = False
            continue
        else:
            replay_name = filename.strip()
            python_script_with_args = 'python xml_parser.py ' + replay_name
            os.system(python_script_with_args)