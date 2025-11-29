""" This cell calculates pi via the Madhava-Leibniz series: https://en.wikipedia.org/wiki/Approximations_of_%CF%80#Middle_Ages """
import simplempi
import numpy as np

# initialize simplepi
smpi = simplempi.simpleMPI()

# initialize pi to 0
pi_part = 0

# set the number of terms in the sum
N = 10000

# loop from 1 to N, adding terms to pi
# such that pi ~= 4*(1 - 1/3 + 1/5 - 1/7 + 1/9 ... -(-1)**n / (2n - 1))
for n in smpi.parfor(range(1,N)):
    if n == 1:
        term = 1
    else:
        term = -((-1)**n) / (2*n - 1)
    pi_part = pi_part + term
    
# gather the pi terms from other ranks 
pi_part_list = smpi.comm.gather(pi_part, root = 0)

if smpi.comm.rank == 0:
    # sum the pi parts
    pi = sum(pi_part_list)

    # multiply pi by four to get the final answer
    pi = 4 * pi

    # print the answer
    print(f"pi = {pi:2.7f}")
    print(f"np.pi = {np.pi:2.7f}")