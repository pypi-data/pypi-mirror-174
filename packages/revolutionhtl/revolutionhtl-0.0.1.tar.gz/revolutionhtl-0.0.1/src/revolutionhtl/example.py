def add_one(number):
    k= number + 1
    print(k)
    return k

if __name__ == "__main__":
    import sys
    add_one(int(sys.argv[1]))