"""
Name:    reqs.csv
Author:  ReddyFan
Date:    2023/12/2 23:12
Desc:  
"""


def read_csv(csv_name: str):
    with open("reqs.csv", "r") as f:
        for line in f:
            word = line.strip().split()
            yield word[0]


if __name__ == '__main__':
    with open("req4.txt", "w") as f:
        for line in read_csv("reqs.csv"):
            f.write(line + "\n")


