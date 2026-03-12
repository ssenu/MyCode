def max3(a, b, c):
    max = a
    if b>max: max=b
    if c>max: max=c
    print(f"max3({a}, {b}, {c}) = {max}")


max3(3,2,1)
max3(2,3,1)
max3(3,1,1)
max3(2,1,3)
max3(2,2,1)

