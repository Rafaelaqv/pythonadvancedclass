import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd
import cartopy
import cmocean
import os

""" Make a function to plot and save the data at a given timestep. """

def generate_frame(
        i : int,
        input_file = "/N/project/easg690_fall2025/data/ERA5/ds633.0/e5.oper.an.sfc/202106/e5.oper.an.sfc.128_136_tcw.ll025sc.2021060100_2021063023.nc",
        output_dir = "./animation_frames/"):

        # prevent matplotlib from displaying the plot
        plt.ioff()

        # make sure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # load the data file 
        ds_in = xr.open_dataset(input_file, chunks = -1)

        # get the variable at the requested timestep
        tcw = ds_in['TCW'].isel(time=i)

        # plot the variable on an orthographic projection centered on Bloomington, IN
        clat = 39.1653
        clon = -86.5264
        projection = cartopy.crs.Orthographic(clon, clat)
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection=projection))

        # plot the data
        tcw.plot(
        ax = ax,
        transform = cartopy.crs.PlateCarree(),
        cmap = cmocean.cm.rain,
        cbar_kwargs = dict(label = f'Precipitable Water [mm]'),
        vmin = 0,
        vmax = 60,
        )

        # get the time of the timestep
        time = tcw.time.values

        # convert it to a datetime object
        time = pd.to_datetime(time)

        # add a title with a nicely formatted date
        ax.set_title(time.strftime("%Y-%m-%d %H:%M UTC"), fontsize=18)

        # add coastlines
        ax.coastlines(alpha = 0.3)

        # save the plot
        output_file = os.path.join(output_dir, f"tcw_{i:05d}.png")
        # save the plot
        fig.savefig(output_file, dpi=300, bbox_inches="tight")

        # close the figure
        plt.close(fig)

        return output_file