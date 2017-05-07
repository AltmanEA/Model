from sympy import *

x_0 = Symbol('x_0')
x_1 = Symbol('x_1')
x_2 = Symbol('x_2')
x_3 = Symbol('x_3')
x_4 = Symbol('x_4')
x_5 = Symbol('x_5')
x_6 = Symbol('x_6')
h_0 = Symbol('h_0')
h_1 = Symbol('h_1')
h_2 = Symbol('h_2')
h_3 = Symbol('h_3')

y_0 = h_0 * x_0 + h_1 * x_1
y_1 = h_0 * x_1 + h_1 * x_2

sub1 = x_1 * (h_0 + h_1)
sub2 = h_0 * (x_0 - x_1)
sub3 = h_1 * (x_2 - x_1)

print('First decomposition ', y_0 - simplify(sub1 + sub2), y_1 - simplify(sub1 + sub3))

yy_0 = h_0 * x_0 + h_1 * x_1 + h_2 * x_2 + h_3 * x_3
yy_1 = h_0 * x_1 + h_1 * x_2 + h_2 * x_3 + h_3 * x_4
yy_2 = h_0 * x_2 + h_1 * x_3 + h_2 * x_4 + h_3 * x_5
yy_3 = h_0 * x_3 + h_1 * x_4 + h_2 * x_5 + h_3 * x_6

s1_1 = x_1 * (h_0 + h_1) + x_3 * (h_2 + h_3)
s1_2 = h_0 * (x_0 - x_1) + h_2 * (x_2 - x_3)
s1_3 = h_1 * (x_2 - x_1) + h_3 * (x_4 - x_3)
s1_4 = x_3 * (h_0 + h_1) + x_5 * (h_2 + h_3)
s1_5 = h_0 * (x_2 - x_3) + h_2 * (x_4 - x_5)
s1_6 = h_1 * (x_4 - x_3) + h_3 * (x_6 - x_5)

print('Second decomposition ', yy_0 - simplify(s1_1 + s1_2), yy_1 - simplify(s1_1 + s1_3),
      yy_2 - simplify(s1_4 + s1_5), yy_3 - simplify(s1_4 + s1_6))

s2_1 = x_3 * (h_0 + h_1 + h_2 + h_3) + (h_0 + h_1) * (x_1 - x_3)
s2_4 = x_3 * (h_0 + h_1 + h_2 + h_3) + (h_2 + h_3) * (x_5 - x_3)
s2_2 = (x_2 - x_3) * (h_0 + h_2) + h_0 * (x_0 - x_1 - x_2 + x_3)
s2_5 = (x_2 - x_3) * (h_0 + h_2) + h_2 * (x_3 - x_2 + x_4 - x_5)
s2_3 = (x_4 - x_3) * (h_1 + h_3) + h_1 * (x_2 - x_1 + x_3 - x_4)
s2_6 = (x_4 - x_3) * (h_1 + h_3) + h_3 * (x_3 - x_4 + x_6 - x_5)

print('Third decomposition ', yy_0 - simplify(s2_1 + s2_2), yy_1 - simplify(s2_1 + s2_3),
      yy_2 - simplify(s2_4 + s2_5), yy_3 - simplify(s2_4 + s2_6))

t0 = x_1 - x_3
t1 = x_5 - x_3
t2 = x_2 - x_3
t3 = x_4 - x_3
t4 = x_0 - x_1 - t2
t5 = x_4 - x_5 - t2
t6 = x_2 - x_1 - t3
t7 = x_6 - x_5 - t3

s3_1 = x_3 * (h_0 + h_1 + h_2 + h_3) + (h_0 + h_1) * t0
s3_4 = x_3 * (h_0 + h_1 + h_2 + h_3) + (h_2 + h_3) * t1
s3_2 = t2 * (h_0 + h_2) + h_0 * t4
s3_5 = t2 * (h_0 + h_2) + h_2 * t5
s3_3 = t3 * (h_1 + h_3) + h_1 * t6
s3_6 = t3 * (h_1 + h_3) + h_3 * t7

print('Forth decomposition ', yy_0 - simplify(s3_1 + s3_2), yy_1 - simplify(s3_1 + s3_3),
      yy_2 - simplify(s3_4 + s3_5), yy_3 - simplify(s3_4 + s3_6))


# print("trying", simplify(s1_6 - s2_6))