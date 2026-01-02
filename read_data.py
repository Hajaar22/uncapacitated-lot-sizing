from typing import List, Tuple


def read(filename: str) -> Tuple[int, List[int], List[int], List[int], List[int]]:
    with open(filename, "r") as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines if line.strip() != ""]

    n = int(lines[0])
    d = list(map(int, lines[1].split()))
    f = list(map(int, lines[2].split()))
    p = list(map(int, lines[3].split()))
    h = list(map(int, lines[4].split()))

    return n, d, f, p, h
