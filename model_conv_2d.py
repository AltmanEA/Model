from numpy import array, zeros, correlate, random
from scipy.signal import correlate2d

stages = [0, 0]
method_code = {
    0: 'search_2d_full_valid',
}


def get_method(stage):
    return globals()[method_code[stage]]


def search_2d_full_valid(x, y, stages=0):
    result = correlate2d(x, y, 'valid')
    nx, mx = x.shape
    ny, my = y.shape
    nz = nx-ny+1
    mz = mx-my+1
    flops = nz*mz*(2*ny*my-1)
    return result, flops


def search_2d_12_valid(x, y, stage):
    nx, mx = x.shape
    ny, my = y.shape
    x00 = x[0:nx:2, 0:mx:2]
    x01 = x[0:nx:2, 1:mx:2]
    x10 = x[1:nx:2, 0:mx:2]
    x11 = x[1:nx:2, 1:mx:2]
    y00 = y[0:nx:2, 0:mx:2]
    y01 = y[0:nx:2, 1:mx:2]
    y10 = y[1:nx:2, 0:mx:2]
    y11 = y[1:nx:2, 1:mx:2]

    a0 = x00 - x10
    a1 = x01 - x11
    b0 = y11 - y01
    b1 = y11 - y00

    c1 = get_method(stage)(a0, b0, stage - 1)
    c2 = get_method(stage)(a1, b1, stage - 1)
    c3 = get_method(stage)(a1, b0, stage - 1)
    c4 = get_method(stage)(a1, b1, stage - 1)



def search_2d_9_valid(x, y, stage):
    nx, mx = x.shape
    ny, my = y.shape
    x00 = x[0:nx:2, 0:mx:2]
    x01 = x[0:nx:2, 1:mx:2]
    x10 = x[1:nx:2, 0:mx:2]
    x11 = x[1:nx:2, 1:mx:2]
    y00 = y[0:nx:2, 0:mx:2]
    y01 = y[0:nx:2, 1:mx:2]
    y10 = y[1:nx:2, 0:mx:2]
    y11 = y[1:nx:2, 1:mx:2]

    a0 = x00 - x10
    a1 = x01 - x11
    b00 = y00 + y10
    b01 = y01 + y11
    b10 = y10 + y11
    b11 = y11 + y01

    c1 = get_method(stage)(b00 + b01, x00, stage - 1)
    c2 = get_method(stage)(b10 + b11, x10, stage - 1)
    c3 = get_method(stage)(b01 + b11, x10, stage - 1)
    out = zeros((nx//2, mx//2))
    return out


# test
for n in [2, 4, 8, 16]:
    y = array(random.randint(0, 10, (n, n)))
    x = array(random.randint(0, 10, (3*n-1, 3*n-1)))
    r, f = get_method(0)(x, y)
    print(f)

i=0
