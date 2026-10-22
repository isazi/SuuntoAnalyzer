import math
import numpy
import matplotlib.pyplot as plt

EARTH_RADIUS = 6378137.0
TILE_SIZE = 256
MAX_ZOOM = 19


def web_mercator(lat: list, lon: list) -> tuple:
    x = numpy.radians(lon) * EARTH_RADIUS
    y = numpy.log(numpy.tan(numpy.pi / 4 + numpy.radians(lat) / 2)) * EARTH_RADIUS
    return x, y


def tile_zoom(ax) -> int:
    xmin, xmax = ax.get_xlim()
    width = ax.get_position().width * ax.figure.bbox.width
    resolution = (xmax - xmin) / width
    zoom = math.ceil(math.log2(2 * math.pi * EARTH_RADIUS / (TILE_SIZE * resolution)))
    return max(0, min(MAX_ZOOM, zoom))


def update_basemap(ax, contextily, updating: list):
    # add_basemap changes the axes limits, which would trigger this function again
    if updating:
        return
    updating.append(True)
    try:
        for artist in list(ax.images) + list(ax.texts):
            artist.remove()
        try:
            contextily.add_basemap(ax, crs="EPSG:3857", zoom=tile_zoom(ax))
        except Exception as error:
            print(f"Could not load map tiles: {error}")
        ax.figure.canvas.draw_idle()
    finally:
        updating.clear()


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
        ax.set_axis_off()
        updating = []
        update_basemap(ax, contextily, updating)
        # Reload the tiles at a suitable zoom level when zooming or panning
        for event in ("xlim_changed", "ylim_changed"):
            ax.callbacks.connect(
                event, lambda _: update_basemap(ax, contextily, updating)
            )
    else:
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
    ax.legend()
    plt.show()
