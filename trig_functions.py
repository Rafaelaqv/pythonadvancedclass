# initialize the value of e
e = 0

# set the number of iterations
N = 100000

# initialize the factorial
kfactorial = 1

# loop to a very large number
for i in range(N):
    # update the factorial
    if i > 0:
        kfactorial = kfactorial * i

    # update the estimate of e
    e = e + 1/kfactorial

# print e
#print(e)

""" This cell calculates pi via the Madhava-Leibniz series: https://en.wikipedia.org/wiki/Approximations_of_%CF%80#Middle_Ages """

# initialize pi to 0
pi = 0

# set the number of terms in the sum
N = 10000

# initialize an empty list store each term, so we can plot convergence later
pi_terms = []

# loop from 1 to N, adding terms to pi
# such that pi ~= 4*(1 - 1/3 + 1/5 - 1/7 + 1/9 ... -(-1)**n / (2n - 1))
for n in range(1,N):
    if n == 1:
        term = 1
    else:
        term = -((-1)**n) / (2*n - 1)
    pi = pi + term
    
    # store the term
    pi_terms.append(4*pi)

# multiply pi by four to get the final answer
pi = 4 * pi

# print the answer
#print(f"pi = {pi:2.7f}")

# define the e**x function
def exp(x):
    """ Calculate e**x"""
    return e**x

""" Define the trig functions """
def cos(x):
    """ Calculate cos(x) as real(e**(i*x))"""

    # calculate e**(i*x)
    z = exp(1.0j*x)
    cos_x = z.real

    # return the real part for cos
    return cos_x

def sin(x):
    """ Calculate cos(x) as real(e**(i*x))"""

    sin_x = (1-cos(x)**2)**0.5
    

    # return the imaginary part for sin
    return sin_x

def tan(x):
    """ Calculate tan(x) as sin(x)/cos(x)"""

    return sin(x)/cos(x)