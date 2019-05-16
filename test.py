import random as r
global a

a= []
def main():
    for i in range(10):
        b = []
        for j in range(10):
            b.append(r.randint(0,10))
        a.append(b)

    print 'okay'
    printa()
    length()

def length():
    print 'test tilemap y:', len(a)
    print 'test tilemap x:', len(a[0])


def printa():
    global a
    for i in range(len (a)):
        for j in range(len(a[i])):
            print '{}'.format(a[i][j]),
        print

if __name__ == '__main__':
    main()
