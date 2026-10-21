import numpy
import matplotlib.pyplot as plt

EARTH_RADIUS = 6378137.0


def web_mercator(lat: list, lon: list) -> tuple:
    x = numpy.radians(lon) * EARTH_RADIUS
    y = numpy.log(numpy.tan(numpy.pi / 4 + numpy.radians(lat) / 2)) * EARTH_RADIUS
    return x, y


def plot_track(activities: list):
    try:
        import contextily
    except ImportError:
        contextily = None
        print("Install the optional dependency 'contextily' to plot on a map.")
    fig, ax = plt.subplots()
    for activity in activities:
        # Suunto stores coordinates in radians
        lat, lon = numpy.degrees(list(zip(*activity.coordinates)))
        if contextily:
            x, y = web_mercator(lat, lon)
            ax.plot(x, y, label=activity.name)
        else:
            ax.plot(lon, lat, label=activity.name)
    if contextily:
        ax.set_aspect("equal")
        contextily.add_basemap(ax, crs="EPSG:3857")
        ax.set_axis_off()
    else:
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
    ax.legend()
    plt.show()
