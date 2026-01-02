import sys
from read_data import read


def main():
    if len(sys.argv) != 2:
        print("Usage: python dp_uls.py instance_file.dat")
        sys.exit(1)

    filename = sys.argv[1]

    n, d, f, p, h = read(filename)

    print(f"Number of periods: {n}")
    print(f"Demand: {d}")
    print(f"Fixed costs: {f}")
    print(f"Production costs: {p}")
    print(f"Holding costs: {h}")


if __name__ == "__main__":
    main()
