# import libraries
from mpi4py import MPI
import generate_frame

# get the 'communicator'
comm = MPI.COMM_WORLD

# get the 'rank' of the process
my_rank = comm.rank # ! ! ! This is different for every 'copy' of this script that is run in parallel

i = my_rank # set the timestep to the rank 
generate_frame.generate_frame(i)