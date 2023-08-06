import pkgutil


def main():
    """
    Read data from the data file
    and print it to console
    """
    data = pkgutil.get_data(__name__, "Data.txt").decode()
    print(data)


if __name__ == "__main__":
    main()
