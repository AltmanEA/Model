stages = [0, 0]
method_code = {
    0: 'full',
    1: 'cor9'
}


def get_method(stage):
    return globals()[method_code[stages[stage]]]


def full(n, m, stage=0):
    return (m-n+1)**2 * n**2, (m-n+1)**2 * (n**2-1)


def cor9(n, m, stage=0):
    method = get_method(stage)
    submul, subadd = method(n//2, m//2, stage - 1)
    muls = n**3
    adds = 5 * n**2 // 4 + 5 * m**2 // 4
    adds += n*((n**2//2-1)+2*(n**2//4-1))
    size2 = (n//2)*((m+1)//2-1)
    adds += 8 * size2 + 9 * n * m // 4
    return muls + 9*submul, adds + 9*subadd


n = 4
m = 2*n-1
mul, add = cor9(n, m, 1)
print("n -", n, "mul - ", mul, "add - ", add, "flops -", mul+add)
