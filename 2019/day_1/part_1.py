if __name__ == '__main__':
    print(sum(list(map(lambda m: int(m) // 3 - 2, open('input').readlines()))))
