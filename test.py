import json


file1 = json.loads(open("test.json").read())
file2 =  json.loads(open("test2.json").read())

print(file1)
print(file2)
print(file1 == file2)