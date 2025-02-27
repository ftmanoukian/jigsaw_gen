# Generador de rompecabezas

## Cómo utilizarlo

1. Instalar las dependencias:
    
       pip install numpy svgwrite

2. En el archivo ```PUZZLE.py```, configurar los [parámetros](#parámetros) (líneas 5-21).
3. Correr ```PUZZLE.py``` y revisar ```PUZZLE.svg```, verificando que no haya acoples y/o bordes superpuestos.

## Versión actual

El script ```PUZZLE.py``` genera un archivo ```PUZZLE.svg``` con líneas de corte.

Los parámetros de momento se ajustan dentro del script, por lo que hay que ajustarlos antes de correrlo.

![Ejemplo](readme/example.svg)

## Parámetros

* ```filename```: nombre de archivo a exportar (debe tener la extensión ```.svg```).
* ```ncols```: cantidad de columnas.
* ```nrows```: cantidad de filas.
* ```width```: ancho (sin unidad).
* ```height```: alto (sin unidad).
* ```err_max_h```,```err_max_v```: máximo desplazamiento de los vértices desde su posición original, tanto vertical como horizontal (como fracción del ancho de columna o alto de fila).
* ```alter_edge_outer_dimensions```:
  * ```False```: La arista externa de las piezas exteriores respeta la dimensión de la grilla (```col_width``` o ```row_height```).
  * ```True```: La arista externa de las piezas exteriores tiene una dimensión aleatoria, al igual que en el resto de las piezas.
* ```coupling_width```: ancho del acople relativo al ancho de las aristas.
* ```coupling_slope_disp_factor```: factor de desplazamiento del acople según la pendiente de la arista.

### Bugs
Valores muy altos de ```err_max_h``` o ```err_max_v``` pueden hacer que los vértices terminen fuera de la cuadrícula, por lo que se dispara un error.

### Importante!
Ajustar ```coupling_slope_disp_factor``` para evitar que los acoples queden muy juntos con aristas inclinadas y las piezas resulten frágiles.

![Piezas frágiles](readme/weakpiece.png)

### Todo
- [ ] Cargar y/o almacenar los parámetros aleatorios generados para el rompecabezas actual.

- [ ] Convertir el script en clase.

- [x] Mejorar la generación de acoples para no producir piezas frágiles.
    
    - Los acoples se desplazan sobre la arista de acuerdo a la pendiente de la misma. Pasos aplicados:
        
        $t$: ubicación del centro del acople

        $k$: ```coupling_slope_disp_factor```

        $m$: pendiente de la recta entre vértices
        
        $\Delta t = (m · k)^{1/3} · \left(1 - \frac{\text{coupling width}}{2}\right)$