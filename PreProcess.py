import json
from periodic_table import ELEMENTS, lookupEle

string = []

with open("string_2.json", "r") as f:
    string_2 = json.load(f)["response"]
for each in string_2:
    formula = each["formula"]
    string.append({lookupEle(element): number for element, number in formula.items()})
    
print(len(string))
   
with open("string_3.json", "r") as f:
    string_3 = json.load(f)["response"]
for each in string_3:
    formula = each["formula"]
    string.append({lookupEle(element): number for element, number in formula.items()})
   
print(len(string))

with open("string.json", "w") as f:
    json.dump({"names": string}, f)
