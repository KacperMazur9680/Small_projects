import json
import re

json_input = input()

error_dic = {"bus_id": 0,
             "stop_id": 0,
             "stop_name": 0,
             "next_stop": 0,
             "stop_type": 0,
             "a_time": 0}

str_to_dict = json.loads(json_input)

# Type checking:
for dic in str_to_dict:
    for el in dic.items():
        if el[0] == "bus_id":
            if type(el[1]) is not int or el[1] == "":
                error_dic["bus_id"] += 1

        if el[0] ==  "stop_id":
            if type(el[1]) is not int or el[1] == "":
                error_dic["stop_id"] += 1

        if el[0] == "stop_name":
            if type(el[1]) is not str or el[1] == "":
                error_dic["stop_name"] += 1

        if el[0] == "next_stop":
            if type(el[1]) is not int or el[1] == "":
                error_dic["next_stop"] += 1

        if el[0] == "stop_type":
            if type(el[1]) is not str:
                error_dic["stop_type"] += 1
            elif len(el[1])>1:
                error_dic["stop_type"] += 1

        if el[0] == "a_time":
            if type(el[1]) is not str or el[1] == "":
                error_dic["a_time"] += 1

# Format checking:
for dic in str_to_dict:
    for el in dic.items():
        if el[0] == "stop_name":
            try:
                pattern = "([A-Z]\w+ ?)+ (Road|Avenue|Boulevard|Street)$"
                string = el[1]

                result = re.match(pattern, string)
                if result is None:
                    error_dic["stop_name"] += 1
                    print(el[1])
            except TypeError:
                pass
 
        if el[0] == "stop_type":
            try:
                pattern = "S|O|F"
                string = el[1]
                result = re.match(pattern, string)
                
                if result is None:
                    error_dic["stop_type"] += 1
                if el[1] == "":
                    error_dic["stop_type"] -= 1
            except TypeError:
                pass
        
        if el[0] == "a_time":
            try:
                pattern = "^(0[1-9]|1[0-9]|2[0-3]):[0-5][0-9]$"
                string = el[1]
                result = re.match(pattern, string)
                if result is None:
                    error_dic["a_time"] += 1
            except TypeError:
                pass

print("Type and required field validation:", sum(error_dic.values()), "errors")

for k,v in error_dic.items():
    print(k, v)