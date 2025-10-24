# === Import libraries === 
""" Import libraries """
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cmocean
import pandas as pd
import os
from mpi4py import MPI

# Resto do código funciona normalmente...
 
# === MPI setup === 
comm = MPI.COMM_WORLD 
rank = comm.Get_rank()
size = comm.Get_size()
print(f"[Rank {rank}] inicializado (total de {size})") 
 
# === Diretório de saída === 
# ⭐ CORREÇÃO: Salvar no mesmo diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "animation_frames_new")
os.makedirs(output_dir, exist_ok=True)

if rank == 0:  # Só printar uma vez
    print(f"📁 Diretório de saída: {output_dir}") 
 
# === Abrir datasets === 
ds_tcw = xr.open_dataset('/N/project/easg690_fall2025/data/ERA5/ds633.0/e5.oper.an.sfc/202106/e5.oper.an.sfc.128_136_tcw.ll025sc.2021060100_2021063023.nc') 
ds_mslp = xr.open_dataset('/N/project/easg690_fall2025/data/ERA5/ds633.0/e5.oper.an.sfc/202106/e5.oper.an.sfc.128_151_msl.ll025sc.2021060100_2021063023.nc') 

# ⭐ DESCOBRIR QUAL DIA É O ÍNDICE 48 E FILTRAR
time_48 = pd.to_datetime(ds_tcw["TCW"].isel(time=48).time.values)
target_date = time_48.strftime('%Y-%m-%d')

print(f"[Rank {rank}] Índice 48 = {time_48}")
print(f"[Rank {rank}] Animando o dia: {target_date}")

# Filtrar para apenas aquele dia
ds_tcw_day = ds_tcw.sel(time=target_date)
ds_mslp_day = ds_mslp.sel(time=target_date)

print(f"[Rank {rank}] Total de frames: {len(ds_tcw_day.time)}")
 
# === Configurações do mapa === 
clon, clat = -60, -20 
projection = ccrs.Orthographic(clon, clat) 
extent = [-90, -30, -60, 15] 
plt.rcParams.update({ 
    "font.size": 11, 
    "axes.labelweight": "bold", 
    "axes.titleweight": "bold", 
    "axes.linewidth": 1.2, 
    "font.family": "sans-serif" 
}) 
 
# === Loop paralelo === 
for i in range(rank, len(ds_tcw_day.time), size): 
    # Extrair as variáveis (mesmo jeito que você fazia!)
    tcw = ds_tcw_day["TCW"].isel(time=i) 
    mslp = ds_mslp_day["MSL"].isel(time=i) / 100  # Converter Pa para hPa
    
    # Extrair tempo como datetime (mesmo jeito!)
    time = pd.to_datetime(tcw.time.values) 
 
    # === Criar figura === 
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), subplot_kw=dict(projection=projection)) 
 
    # === Painel 1: TCW === 
    im1 = tcw.plot( 
        ax=axes[0], 
        transform=ccrs.PlateCarree(), 
        cmap=cmocean.cm.rain, 
        cbar_kwargs={
            'label': 'Total Column Water (kg m$^{-2}$)', 
            'shrink': 0.85,
            'pad': 0.05
        }, 
        vmin=0, vmax=60,
        add_colorbar=True
    ) 
    axes[0].set_title(f"Total Column Water\n{time.strftime('%Y-%m-%d %H:%M UTC')}", 
                      fontsize=12, pad=10) 
    axes[0].coastlines(linewidth=0.8, color='black', alpha=0.7) 
    axes[0].set_extent(extent, crs=ccrs.PlateCarree()) 
    axes[0].gridlines(draw_labels=False, linewidth=0.4, color="gray", alpha=0.5, linestyle='--')
    
    for spine in axes[0].spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.2)
    
    axes[0].text(0.02, 0.98, '(a)', transform=axes[0].transAxes,
                fontsize=14, fontweight='bold', va='top', ha='left',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
 
    # === Painel 2: MSLP === 
    im2 = mslp.plot( 
        ax=axes[1], 
        transform=ccrs.PlateCarree(), 
        cmap=cmocean.cm.thermal, 
        cbar_kwargs={
            'label': 'Mean Sea Level Pressure (hPa)', 
            'shrink': 0.85,
            'pad': 0.05
        }, 
        vmin=950, vmax=1040,
        add_colorbar=True
    ) 
    axes[1].set_title(f"Mean Sea Level Pressure\n{time.strftime('%Y-%m-%d %H:%M UTC')}", 
                      fontsize=12, pad=10) 
    axes[1].coastlines(linewidth=0.8, color='black', alpha=0.7) 
    axes[1].set_extent(extent, crs=ccrs.PlateCarree()) 
    axes[1].gridlines(draw_labels=False, linewidth=0.4, color="gray", alpha=0.5, linestyle='--')
    
    for spine in axes[1].spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.2)
    
    axes[1].text(0.02, 0.98, '(b)', transform=axes[1].transAxes,
                fontsize=14, fontweight='bold', va='top', ha='left',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
 
    plt.tight_layout() 
 
    # === Salvar figura === 
    output_file = os.path.join(output_dir, f"panel_tcw_mslp_{i:05d}.png") 
    fig.savefig(output_file, dpi=300, bbox_inches="tight", facecolor="white") 
    plt.close(fig) 
    print(f"[Rank {rank}] → Figura {i+1}/{len(ds_tcw_day.time)}: {output_file}")

print(f"[Rank {rank}] ✅ Concluído!")