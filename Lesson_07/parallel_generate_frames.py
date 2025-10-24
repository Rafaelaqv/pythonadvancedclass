from mpi4py import MPI
import generate_frame

# get the MPI communicator
comm = MPI.COMM_WORLD

# get the rank of the current process
rank = comm.rank

# run the generate_frame function on each process
generate_frame.generate_frame(rank)