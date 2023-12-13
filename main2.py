def fac(n):
    r = 1
    while (n > 1):
        r = r*n
        n -= 1
    return r


def comb(n, r):
    return fac(n)/(fac(r)*fac(n-r))


def num_ways(k, n):
    if n == 1:
        return (k+1)/2
    else:
        return k*()


print("HEllo world")
