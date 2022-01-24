# Hyperion
Optimizador de rutas geograficas 

# Creacion de mapas automatico

```python
datos = Hyperion("<NOMBRE DE UNA ZONA GEOGRAFICA>")
ruta = datos.get_node_route((LATITUD_ORIGEN, LONGITUD_ORIGEN), (LATITUD_DESTINO, LONGITUD_DESTINO))
lat, long = datos.node_list_path_to_lat_lon(ruta)
datos.add_route_to_map(lat, long, "red", "ruta 1")
ruta = datos.get_node_route((LATITUD_ORIGEN_2, LONGITUD_ORIGEN_2), (LATITUD_DESTINO_2, LONGITUD_DESTINO_2))
lat, long = datos.node_list_path_to_lat_lon(ruta)
datos.add_route_to_map(lat, long, "green", "ruta 2")
...
ruta = datos.get_node_route((LATITUD_ORIGEN_N, LONGITUD_ORIGEN_N), (LATITUD_DESTINO_N, LONGITUD_DESTINO_N))
lat, long = datos.node_list_path_to_lat_lon(ruta)
datos.add_route_to_map(lat, long, "blue", "ruta N")
datos.plot_map(LATITUD_VISTA_CENTRADA,, LONGITUD_VISTA_CENTRADA, ZOOM_NUMERICO)
```
