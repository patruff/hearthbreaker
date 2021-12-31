import os
import re

count = 0
id_string_list = []

with open(os.path.join(os.path.dirname(__file__),"latest_replays5.html"), 'r', encoding="utf8") as f:
    html_text = f.read()
    html_split = html_text.split('a href="/replay/')

    for thing in html_split:
        class_split = thing.split('class=')

        for thing2 in class_split:
            print(len(thing2))

            # this will grab all of the replay id strings
            if len(thing2) == 24:
                print("Thing2 is " + thing2.strip())
                print("Count is " + str(count))
                count = count + 1

                stripped_thing = thing2.replace('\"', '').strip()

                id_string_list.append(stripped_thing)

    # print(html_split)
    
print(id_string_list)
print(str(len(id_string_list)))
del id_string_list[0]

print(id_string_list)
print(str(len(id_string_list)))

with open("replay_strings.txt", "a") as outfile:
    strings = "\n".join(id_string_list)
    good_strings = "\n" + strings
    outfile.write(good_strings)

# <a href="/replay/c58rH8jVsSAamnQnd8qnif" class=