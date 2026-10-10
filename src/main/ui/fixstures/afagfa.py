def adjm(x):
    while x < 100:
        yield x
        x += 1
x = adjm(1)
for i in x:
    print(i)

for i in x:
    print(100-i)