import json

json_input = input("Input data: ")

bi_e = 0
si_e = 0
sn_e = 0
ns_e = 0
st_e = 0
at_e = 0

str_to_dict = json.loads(json_input)

for dic in str_to_dict:
    for el in dic.items():
        if el[0] == "bus_id":
            if type(el[1]) is not int or el[1] == "":
                bi_e += 1
        if el[0] ==  "stop_id":
            if type(el[1]) is not int or el[1] == "":
                si_e += 1
        if el[0] == "stop_name":
            if type(el[1]) is not str or el[1] == "":
                sn_e += 1
        if el[0] == "next_stop":
            if type(el[1]) is not int or el[1] == "":
                ns_e += 1
        if el[0] == "stop_type":
            if type(el[1]) is not str:
                st_e += 1
            elif len(el[1])>1:
                st_e += 1
        if el[0] == "a_time":
            if type(el[1]) is not str or el[1] == "":
                at_e += 1

print("Type and required field validation:", bi_e + si_e + sn_e + ns_e + st_e + at_e, "errors")
print("bus_id", bi_e)
print("stop_id", si_e)
print("stop_name", sn_e)
print("next_stop", ns_e)
print("stop_type", st_e)
print("a_time", at_e)