from simplempi.parfor import parfor, pprint #this initializes mpiy
import generate_frame as generate_frame # load the generate_frame function

# define the number of timesteps
n_frames = 720

# create a list of the timesteps to loop over
times = list(range(n_frames))

for t in parfor(times):
    #print which timestep is being worked on
    pprint(f'Working on timestep{t}')
    # run the generate_frame function on each process
    generate_frame.generate_frame(t)