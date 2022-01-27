# Hyperion
Optimizador de rutas geograficas 

# Creacion de mapas automatico (MANUAL)

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
# Creacion de mapas automatico "OPTIMO"

```python
cords = {
        "Punto 1":[lat_1, long_1],
        "Punto 2":[lat_2, long_2],
        ...,
        "Punto n":[lat_n, long_n]
}

data = Hyperion("<NOMBRE DE UNA ZONA GEOGRAFICA>")
data.optimal_map(cords, lat_central, long_central, nivel_zoom)
```
# Creacion de mapas de elevaciones REQUIERE OPEN ELEVATION

[Añadir documentacion y demas]

```python
datos = Hyperion("<NOMBRE DE UNA ZONA GEOGRAFICA>")
datos.open_elevation_data("http://192.168.xxx.xxx")
datos.elevation_map("http://192.168.xxx.xxx")
```
