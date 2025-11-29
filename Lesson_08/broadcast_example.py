#!/usr/bin/env python3

# import MPI
from mpi4py import MPI

# get the communicator
comm = MPI.COMM_WORLD

# get the mpi rank
rank = comm.rank

if rank == 0:
    # (represents reading a file from a list like in the example above)
    full_list = list(range(100))
else:
    full_list = None

# broadcast the list; this copies full_list to all the other processes
my_list = comm.bcast(full_list, root=0)

# print the list
print(f"{rank}: {my_list}")