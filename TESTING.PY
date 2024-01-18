def fibonacci(n):
    for c in range(0, n):
        print(c)
        if c == 5:
            try:
                a = c / 0
            except Exception as e:
                print(e)
print(fibonacci(10))