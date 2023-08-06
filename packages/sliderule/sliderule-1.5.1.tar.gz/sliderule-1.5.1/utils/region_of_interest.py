#
# Requests SlideRule to process the provided region of interest twice:
# (1) perform ATL06-SR algorithm to calculate elevations in region
# (2) retrieve photon counts from each ATL06 extent
#
# The region of interest is passed in as a json file that describes the
# geospatial polygon for the region. An example json object is below:
#
# {
#   "region": [{"lon": 86.269733430535638, "lat": 28.015965655545852},
#              {"lon": 86.261403224371804, "lat": 27.938668666352985},
#              {"lon": 86.302412923741514, "lat": 27.849318271202186},
#              {"lon": 86.269733430535638, "lat": 28.015965655545852}]
# }
#

import sys
import logging
import time
import geopandas as gpd
import matplotlib.pyplot as plt
from sliderule import icesat2
from utils import parse_command_line

###############################################################################
# LOCAL FUNCTIONS
###############################################################################

def process_atl06_algorithm(parms, asset):

    # Latch Start Time
    perf_start = time.perf_counter()

    # Request ATL06 Data
    gdf = icesat2.atl06p(parms, asset)

    # Latch Stop Time
    perf_stop = time.perf_counter()

    # Build DataFrame of SlideRule Responses
    num_elevations = len(gdf)

    # Display Statistics
    perf_duration = perf_stop - perf_start
    print("Completed in {:.3f} seconds of wall-clock time".format(perf_duration))
    if num_elevations > 0:
        print("Reference Ground Tracks: {}".format(gdf["rgt"].unique()))
        print("Cycles: {}".format(gdf["cycle"].unique()))
        print("Received {} elevations".format(num_elevations))
    else:
        print("No elevations were returned")

    # Return DataFrame
    return gdf

###############################################################################
# MAIN
###############################################################################

if __name__ == '__main__':

    # Set Script Defaults
    cfg = {
        "url":          'localhost',
        "organization": None,
        "asset":        'atlas-local',
        "region":       'examples/grandmesa.geojson',
        "verbose":      True
    }

    # Parse Configuration Parameters
    parse_command_line(sys.argv, cfg)

    # Configure Logging
    logging.basicConfig(level=logging.INFO)

    # Region of Interest #
    region = icesat2.toregion(cfg["region"])

    # Configure SlideRule #
    icesat2.init(cfg["url"], cfg["verbose"], organization=cfg["organization"])

    # Build ATL06 Request #
    parms = {
        "poly": region["poly"],
        "raster": region["raster"],
        "srt": icesat2.SRT_LAND,
        "cnf": icesat2.CNF_SURFACE_HIGH,
        "atl08_class": ["atl08_ground"],
        "ats": 10.0,
        "cnt": 10,
        "len": 40.0,
        "res": 20.0,
        "maxi": 1
    }

    # Parse Algorithm Parameters
    parse_command_line(sys.argv, parms)

    # Get ATL06 Elevations
    atl06 = process_atl06_algorithm(parms, cfg["asset"])

    # Check Results Present
    if len(atl06) == 0:
        print("No ATL06 data available")
        sys.exit()

    # Calculate Extent
    lons = [p["lon"] for p in region["poly"]]
    lats = [p["lat"] for p in region["poly"]]
    lon_margin = (max(lons) - min(lons)) * 0.1
    lat_margin = (max(lats) - min(lats)) * 0.1
    extent = (min(lons) - lon_margin, max(lons) + lon_margin, min(lats) - lat_margin, max(lats) + lat_margin)

    # Create Plot
    fig = plt.figure(num=None, figsize=(24, 12))

    # Plot ATL06 Ground Tracks
    ax1 = plt.subplot(231)
    ax1.set_title("Zoomed ATL06 Ground Tracks")
    atl06.plot(ax=ax1, column='h_mean', cmap='plasma', markersize=0.5)
    ax1.plot(lons, lats, linewidth=1.5, color='r', zorder=2)

    # Plot ATL06 Along Track Slope
    ax2 = plt.subplot(232)
    ax2.set_title("Zoomed ATL06 Along Track Slope")
    atl06.plot(ax=ax2, column='dh_fit_dx', cmap='inferno', markersize=0.5)
    ax2.plot(lons, lats, linewidth=1.5, color='r', zorder=2)

    # Plot Global View
    ax3 = plt.subplot(233)
    ax3.set_title("Global Reference")
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world.plot(ax=ax3, color='0.8', edgecolor='black')
    atl06.plot(ax=ax3, marker='o', color='red', markersize=2.5, zorder=3)
    ax3.set_xlim(-180,180)
    ax3.set_ylim(-90,90)
    ax3.set_aspect('equal', adjustable='box')

    # Plot Number of Fit Photons per ATL06 Ground Tracks
    ax4 = plt.subplot(234)
    atl06.hist("n_fit_photons", bins=100, ax=ax4)
    ax4.set_title("Number of Fit Photons")

    # Plot Final Window Size per ATL06 Ground Tracks
    ax5 = plt.subplot(235)
    atl06.hist("w_surface_window_final", bins=100, ax=ax5)
    ax5.set_title("Final Window Size")

    # Plot Number of Fit Photons per ATL06 Ground Tracks
    ax6 = plt.subplot(236)
    atl06.hist("rms_misfit", bins=100, ax=ax6)
    ax6.set_title("RMS of Fit")

    # Show Plot
    plt.show()