unprocessed_data = []
full_list = []
sorted_list = []
with open('layout.txt') as f:
    lines = f.readlines()
    for li in lines:
        unprocessed_data.append(li.strip("\n"))

for line in unprocessed_data:
    for char in line:
        full_list.append(int(char))

temp = []
for i, char in enumerate(full_list):
    temp.append(char)
    if (i + 1) % len(unprocessed_data[0]) == 0:
        sorted_list.append(temp)
        temp = []

print(full_list)
print(sorted_list)
