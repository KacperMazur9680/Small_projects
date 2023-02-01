import json
import re
import sys

json_input = input()

str_to_dict = json.loads(json_input)

error_dic = {"bus_id": 0,
             "stop_id": 0,
             "stop_name": 0,
             "next_stop": 0,
             "stop_type": 0,
             "a_time": 0}

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

# Bus line info:
bus_dic = {}

print("Line names and number of stops:")
for dic in str_to_dict:
    for el in dic.items():
        if el[0] == "bus_id":
            if el[1] not in bus_dic.keys():
                bus_dic.update({el[1]: 1})
            else:
                bus_dic[el[1]] += 1

for k,v in bus_dic.items():
    print(f"bus id: {k}, stops: {v}")


print("\nType and required field validation:", sum(error_dic.values()), "errors")
for k,v in error_dic.items():
    print(f"{k}: {v}")

# Bus start-stops checker/shower:
stop_dic = {}

for dic in str_to_dict:
    for el in dic.items():
        if el[0] == "bus_id":
            id = el[1]
            if id not in stop_dic:
                stop_dic.update({id:{}})

        if el[0] == "stop_name":
            s_name = el[1]

        if el[0] == "stop_type":
            s_type = el[1]
            if s_type == "S" or s_type == "F":
                stop_dic[id].update({s_type: s_name})
            else:
                if s_type not in stop_dic[id].keys():
                    stop_dic[id].update({s_type:[s_name]})
                else:
                    stop_dic[id][s_type].append(s_name)

for bus_id, bus_info in stop_dic.items():
    if "S" not in bus_info or "F" not in bus_info:
        print(f"There is no start or end stop for the line: {bus_id}")
        sys.exit()

start = set()
trans = []
stop = set()

for info in stop_dic.values():
    for el in info.items():
        if el[0] == "S":
            start.add(el[1])
            trans.append(el[1])
        elif el[0] == "F":
            stop.add(el[1])
            trans.append(el[1])
        else:
            for s_name in el[1]:
                trans.append(s_name)


for s_name in trans[:]:
    if trans.count(s_name) == 1:
        trans.remove(s_name)

trans = set(trans)

print(f"\nStart stops:", len(start), sorted(list(start)))
print(f"Transfer stops:", len(trans), sorted(list(trans)))
print(f"Finish stop:", len(stop), sorted(list(stop)))

# Time checking:
time_error = {}
buses = []

for dic in str_to_dict:
    for el in dic.items():
        if el[0] == "bus_id":
            bus = el[1]
            if bus not in buses:
                buses.append(bus)
                time = 0
        if el[0] == "stop_name":
            name = el[1]

        if el[0] == "a_time":
            s_time = int(el[1].replace(":",""))
            if s_time > time:
                time = el[1].replace(":","")
                time = int(time)
            else:
                if bus not in time_error.keys():
                    time_error.update({bus: name})
                else:
                    continue

print("\nArrival time test:")
if len(time_error) == 0:
    print("OK")
else:
    for id, name in time_error.items():
        print(f"bus_id line {id}: wrong time on station {name}")

# Checking if on demand stops are not initial, transfer or final stops:
full_list = list(start) + list(trans) + list(stop)
demand_error = []

for info in stop_dic.values():
    for key, val in info.items():
        if key == "O":
            for el in val: 
                if el in full_list:
                    demand_error.append(el)

demand_error = set(demand_error)

if len(demand_error) == 0:
    print("OK")
else:
    print(f"Wrong stop type: {sorted(list(demand_error))}")