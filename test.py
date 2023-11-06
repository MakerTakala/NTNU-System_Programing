data = [1, 2, 3, 4, 5]

for index, d in enumerate(data):
    print(index, d)
    if index == 2:
        data.insert(index + 1, 9)

print(data)
