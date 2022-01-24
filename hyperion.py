import osmnx as ox
import networkx as nx
import plotly.graph_objects as go
import numpy as np

class Hyperion():
    def __init__(self, area_name, type_search = "drive"):
        self.geo_data = ox.graph_from_place(area_name, network_type = type_search)
        self.route_map = fig = go.Figure()
    def get_node_route(self, origin_point, destination_point):
        origin_node = ox.get_nearest_node(self.geo_data, origin_point) 
        destination_node = ox.get_nearest_node(self.geo_data, destination_point)
        return nx.shortest_path(self.geo_data, origin_node, destination_node, weight = 'length')
    def node_list_to_path(self, node_list):
        edge_nodes = list(zip(node_list[:-1], node_list[1:]))
        lines = []
        for u, v in edge_nodes:
            data = min(self.geo_data.get_edge_data(u, v).values(), key=lambda x: x['length'])
            if 'geometry' in data:
                xs, ys = data['geometry'].xy
                lines.append(list(zip(xs, ys)))
            else:
                x1 = self.geo_data.nodes[u]['x']
                y1 = self.geo_data.nodes[u]['y']
                x2 = self.geo_data.nodes[v]['x']
                y2 = self.geo_data.nodes[v]['y']
                line = [(x1, y1), (x2, y2)]
                lines.append(line)
        return lines
    def node_list_path_to_lat_lon(self, route):
        lines = self.node_list_to_path(route)
        long = []
        lat = []
        for i in range(len(lines)):
            z = list(lines[i])
            l1 = list(list(zip(*z))[0])
            l2 = list(list(zip(*z))[1])
            for j in range(len(l1)):
                long.append(l1[j])
                lat.append(l2[j])
        return lat, long
    def add_route_to_map(self, lat, long, color, label):
        self.route_map.add_trace(go.Scattermapbox(
            name = label,
            mode = "lines",
            lon = long,
            lat = lat,
            marker = {'size': 10},
            line = dict(width = 4.5, color = color)))
    def plot_map(self, lat_center, long_center, zoom):
        self.route_map.update_layout(mapbox_style="stamen-terrain",
            mapbox_center_lat = 30, mapbox_center_lon=-80)
        self.route_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                        mapbox = {
                            'center': {'lat': lat_center, 
                            'lon': long_center},
                            'zoom': zoom})
        self.route_map.show()

