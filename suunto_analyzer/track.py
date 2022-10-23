import folium
from suunto_analyzer.json_reader import SuuntoJSON

def plot_track(activity: SuuntoJSON):
    map = folium.Map(location=activity.coordinates[0], zoom_start=15)
    track = folium.PolyLine(activity.coordinates, color="red")
    map.save("test.html")