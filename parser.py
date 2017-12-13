import sys


with open("test_data.txt") as f:
    line = f.readline()
    line = f.readline()
    for c in line.split("  "):
        if (c.strip() != ""):
            print(c)

