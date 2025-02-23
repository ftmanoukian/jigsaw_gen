# Generador de rompecabezas

## Versión actual

El script ```PUZZLE.py``` genera un archivo ```PUZZLE.svg``` con líneas de corte.

Los parámetros de momento se ajustan dentro del script, por lo que hay que ajustarlos antes de correrlo.

![Ejemplo](readme/example.svg)

### Parámetros

* ```ncols```: cantidad de columnas.
* ```nrows```: cantidad de filas.
* ```width```: ancho (sin unidad).
* ```height```: alto (sin unidad).
* ```err_max_h```,```err_max_v```: máximo desplazamiento de los vértices desde su posición original, tanto vertical como horizontal.
* ```coupling_width```: ancho del acople relativo al ancho de las aristas.

### Bugs
Valores muy altos de ```err_max_h``` o ```err_max_v``` pueden hacer que los vértices terminen fuera de la cuadrícula, por lo que se dispara un error.

Por otro lado, los mismos en conjunto con ```coupling_width``` pueden producir piezas frágiles o incluso bordes superpuestos. Se debe revisar el diseño minuciosamente antes de cortarlo.

![Piezas frágiles](readme/weakpiece.png)

### Todo
- [ ] Cargar y/o almacenar los parámetros aleatorios generados para el rompecabezas actual.

- [ ] Mejorar la generación de acoples para no producir piezas frágiles.