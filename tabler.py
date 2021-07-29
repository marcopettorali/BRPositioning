data = []
with open("output.csv", "r") as file:
    for line in file:
        data.append(line)
print(data)
with open("coverage_intersecting_flower.csv", "w") as file:
    for j in range(200,600,10):
            file.write(f";{j}")
    file.write("\n")
    for i in range(200,600,10):
        file.write(f"{i};")
        for j in range(200,600,10):
            index = int((i - 200 )/10 * 40 + (j - 200 )/10)
            file.write(data[index].split(";")[] + ";")
        file.write("\n")