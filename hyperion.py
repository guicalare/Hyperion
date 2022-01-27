import osmnx as ox
import networkx as nx
import plotly.graph_objects as go
import numpy as np
from geopy import distance
from pandas import DataFrame
import warnings
import requests
from requests.structures import CaseInsensitiveDict
import copy
import plotly.express as px
import json

warnings.filterwarnings("ignore")

class Hyperion():
    def __init__(self, area_name, type_search = "drive"):
        self.geo_data = ox.graph_from_place(area_name, network_type = type_search)
        self.route_map = go.Figure()
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
    def add_point_map(self, lat, long, color, label, size):
         self.route_map.add_trace(go.Scattermapbox(
            name = label,
            mode = "markers",
            lon = [long],
            lat = [lat],
            marker = {'size':size, 'color':color}))
    def plot_map(self, lat_center, long_center, zoom):
        self.route_map.update_layout(mapbox_style="open-street-map",
            mapbox_center_lat = 30, mapbox_center_lon=-80)
        self.route_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                        mapbox = {
                            'center': {'lat': lat_center, 
                            'lon': long_center},
                            'zoom': zoom})
        self.route_map.update_layout(legend_title='<b> Rutas </b>')
        self.route_map.show()
    def cross_distances_to_network(self, data):
        node_1, node_2, distances = [], [], []
        for city1, cords1 in data.items():
            for city2, cords2 in cords.items():
                if city1 != city2:
                    node_1.append(city1)
                    node_2.append(city2)
                    distances.append(distance.distance(cords1, cords2).km)
        return DataFrame(list(zip(node_1, node_2, distances)), columns=["Node_1", "Node_2", "weight"])
    def cross_distances_dict_to_network(self, data):
        temp = self.cross_distances_to_network(data)
        return nx.from_pandas_edgelist(temp, source="Node_1", target="Node_2", edge_attr="weight")
    def minimal_tree(self, data):
        temp = self.cross_distances_dict_to_network(data)
        return nx.minimum_spanning_tree(temp).edges(data=True)
    def optimal_map(self, data, lat_center, long_center, zoom):
        minimal_path = self.minimal_tree(data)
        for path in minimal_path:
            route = self.get_node_route(data[path[0]], data[path[1]])
            self.add_point_map(data[path[0]][0], data[path[0]][1], "red", "Inicio " + path[0], 12)
            self.add_point_map(data[path[1]][0], data[path[1]][1], "red", "Fin " + path[1], 12)
            lat, long = self.node_list_path_to_lat_lon(route)
            self.add_route_to_map(lat, long, "blue", path[0] + " - " + path[1])
        self.plot_map(lat_center, long_center, zoom)
        self.route_map = go.Figure()
    def open_elevation_data(self, server_url, chunk_size = 2000):
        url = f"{server_url}/api/v1/lookup"
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "application/json"
        coordenadas = {'locations':[]}
        responses = []
        for node in range(len(self.geo_data)):
            node_id = list(self.geo_data.nodes)[node]
            y = self.geo_data.nodes[node_id]["y"]
            x = self.geo_data.nodes[node_id]["x"]
            coordenadas['locations'].append({'latitude':y, 'longitude':x})
        split_requests = [coordenadas["locations"][i:i+chunk_size] for i in range(0, len(coordenadas["locations"]), chunk_size)]
        for data_chunck in split_requests:
            r = requests.post(url, headers=headers, data=json.dumps({"locations":data_chunck})).json()
            responses = responses + r["results"]
        for node in range(len(self.geo_data)):
            node_id = list(self.geo_data.nodes)[node]
            self.geo_data.nodes[node_id]["elevation"] = responses[node]["elevation"]
    def elevation_map(self, url):
        self.open_elevation_data(url)
        lat, long, ele = [], [], []
        df = DataFrame()
        for node in range(len(self.geo_data)):
            node_id = list(self.geo_data.nodes)[node]
            lat.append(self.geo_data.nodes[node_id]["y"])
            long.append(self.geo_data.nodes[node_id]["x"])
            ele.append(self.geo_data.nodes[node_id]["elevation"])
        df["lat"] = lat
        df["lon"] = long
        df["elevation"] = ele 
        fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_data=["elevation"],
                                color="elevation", zoom=11)
        fig.update_layout(
            mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.show()
