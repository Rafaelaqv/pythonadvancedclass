#!/usr/bin/env python3

# import MPI
from mpi4py import MPI

# get the communicator
comm = MPI.COMM_WORLD

# get the mpi rank
rank = comm.rank

# set the individual result for each rank
my_number = rank

# gather the results on rank 0
full_list = comm.gather(my_number, root=0)

# calculate the average rank; only rank 0 can do this
if rank == 0:
    avg_rank = sum(full_list) / len(full_list)
else:
    avg_rank = None

# print the list
print(f"{rank}: {full_list}, avg_rank = {avg_rank}")