import svgwrite
import random
import numpy as np

def bezier_point(t, P0 : np.array, P1 : np.array, P2 : np.array, P3 : np.array) -> np.array:
    return ((1 - t)**3 * P0 + 3 * (1 - t)**2 * t * P1 + 3 * (1 - t) * t**2 * P2 + t**3 * P3)

def bezier_tangent(t, P0 : np.array, P1 : np.array, P2 : np.array, P3 : np.array) -> np.array:
    v_tan = 3 * (1 - t)**2 * (P1 - P0) + 6 * (1 - t) * t * (P2 - P1) + 3 * t**2 * (P3 - P2)
    return np.arctan2(*v_tan)

def get_center_handles(E0:np.array, E1:np.array, alpha0:float, alpha1:float):
    u0 = np.array([np.sin(alpha0),np.cos(alpha0)])
    u1 = np.array([np.sin(alpha1),np.cos(alpha1)])

    c0 = E1[0] - E0[0]
    c1 = E1[1] - E0[1]
    c2 = u1[0] - u0[0]
    c3 = u1[1] - u0[1]

    d = (c2**2+c3**2-1)
    t1 = -(c0*c2+c1*c3)
    t2 = np.sqrt(c0**2+c1**2-(c0*c3-c1*c2)**2)
    l = min(t1+t2,t1-t2)/d

    I0 = E0 + u0 * l
    I1 = E1 + u1 * l

    return I0,I1

def create_coupling(P0:np.array,P1:np.array,alpha0:float,alpha1:float,direction:bool=True)->str:
    l = np.linalg.norm(P1-P0)
    if direction:
        alpha2,alpha3 = alpha0 + np.pi * 0.7, alpha1 - np.pi * 0.7
    else:
        alpha2,alpha3 = alpha0 - np.pi * 0.7, alpha1 + np.pi * 0.7
    P2 = P0 + l * 0.33 * np.array([np.sin(alpha0),np.cos(alpha0)])
    P3 = P1 + l * 0.33 * np.array([np.sin(alpha1),np.cos(alpha1)])
    P4 = P2 + l * 0.42 * np.array([np.sin(alpha2),np.cos(alpha2)])
    P5 = P3 + l * 0.42 * np.array([np.sin(alpha3),np.cos(alpha3)])
    P6 = P4 + l * np.array([np.sin(alpha2),np.cos(alpha2)])
    P7 = P5 + l * np.array([np.sin(alpha3),np.cos(alpha3)])

    path = f'M{P0[0]},{P0[1]}'
    path += f'Q{P2[0]} {P2[1]}, {P4[0]} {P4[1]}'
    path += f'C{P6[0]} {P6[1]}, {P7[0]} {P7[1]}, {P5[0]} {P5[1]}'
    path += f'Q{P3[0]} {P3[1]}, {P1[0]} {P1[1]}'

    return path

def lerp(P0:np.array,P1:np.array,t:float)->np.array:
    return (1-t)*P0+t*P1

def split_cubic_bezier(P0:np.array,P1:np.array,P2:np.array,P3:np.array,t_end:float)->list[:np.array]:
    P0_1 = lerp(P0,P1,t_end)
    P1_1 = lerp(P1,P2,t_end)
    P2_1 = lerp(P2,P3,t_end)

    P0_2 = lerp(P0_1,P1_1,t_end)
    P1_2 = lerp(P1_1,P2_1,t_end)

    P0_3 = lerp(P0_2,P1_2,t_end)

    return [P0,P0_1,P0_2,P0_3]

# ==== PARAMETROS DE ROMPECABEZAS - se pueden modificar ====

ncols = 20
nrows = 15
width = 300
height = 250

err_max_h = 0.125 # como porcentaje del ancho de una celda
err_max_v = 0.125 # como porcentaje del alto de una celda

coupling_width = 0.28 # como porcentaje del largo de un lado

# ==== A PARTIR DE ACA NO TOCAR

t_begin = .5 - coupling_width / 2
t_end = .5 + coupling_width / 2

col_width = width/ncols
row_height = height/nrows

deltas_h = np.linspace(-col_width*err_max_h, col_width*err_max_h, (ncols - 1) * (nrows - 1)).tolist()
deltas_v = np.linspace(-row_height*err_max_v, row_height*err_max_v, (ncols - 1) * (nrows - 1)).tolist()
random.shuffle(deltas_h)
random.shuffle(deltas_v)

vert_matrix = []
for ncol in range(ncols + 1):
    col = []
    for nrow in range(nrows + 1):
        x = ncol * col_width
        y = nrow * row_height
        if ncol != 0 and ncol != ncols and nrow != 0 and nrow != nrows:
            x += deltas_h.pop(0)
            y += deltas_v.pop(0)
        col.append(np.array([x,y]))
        
    vert_matrix.append(col)

# ==== angulos tangentes de bordes en vertices ====

tg_matrix = []
for ncol in range(ncols + 1):
    col = []
    for nrow in range(nrows + 1):
        dot = vert_matrix[ncol][nrow]

        if ncol == 0 or ncol == ncols:
            alpha_h = np.pi / 2
        else:
            next_xdot = vert_matrix[ncol + 1][nrow]
            prev_xdot = vert_matrix[ncol - 1][nrow]
            alpha_h = np.arctan2(*(next_xdot - prev_xdot))

        if nrow == 0 or nrow == nrows:
            alpha_v = 0
        else:
            next_ydot = vert_matrix[ncol][nrow + 1]
            prev_ydot = vert_matrix[ncol][nrow - 1]
            alpha_v = np.arctan2(*(next_ydot - prev_ydot))

        col.append([alpha_h, alpha_v])
    tg_matrix.append(col)

dwg = svgwrite.Drawing(
    filename = f"PUZZLE.svg",
    size = (width, height),
    profile = "tiny"
)

for ncol in range(1,ncols,1):
    vpath = dwg.path().stroke('black',width=0.5).fill('none')

    for nrow in range(nrows):
        E0 = vert_matrix[ncol][nrow]
        E1 = vert_matrix[ncol][nrow + 1]
        a0 = tg_matrix[ncol][nrow][1]
        a1 = tg_matrix[ncol][nrow+1][1] + np.pi
        I0, I1 = get_center_handles(E0,E1,a0,a1)

        P0 = bezier_point(t_begin, E0,I0,I1,E1)
        P1 = bezier_point(t_end, E0,I0,I1,E1)
        b0 = bezier_tangent(t_begin,E0,I0,I1,E1)
        b1 = bezier_tangent(t_end,E0,I0,I1,E1) + np.pi

        E0_1,I0_1,I1_1,E1_1 = split_cubic_bezier(E0,I0,I1,E1,t_begin)
        E1_2,I1_2,I0_2,E0_2 = split_cubic_bezier(E1,I1,I0,E0,1-t_end)

        vpath.push(
            f'M{E0_1[0]},{E0_1[1]} C{I0_1[0]} {I0_1[1]},{I1_1[0]} {I1_1[1]},{E1_1[0]} {E1_1[1]}'
        )
        vpath.push(create_coupling(P0,P1,b0,b1,random.randint(0,1)))
        vpath.push(
            f'M{E1_2[0]},{E1_2[1]} C{I1_2[0]} {I1_2[1]},{I0_2[0]} {I0_2[1]},{E0_2[0]} {E0_2[1]}'
        )
    
    dwg.add(vpath)

for nrow in range(1,nrows,1):
    hpath = dwg.path().stroke('black',width=0.5).fill('none')

    for ncol in range(ncols):
        E0 = vert_matrix[ncol][nrow]
        E1 = vert_matrix[ncol + 1][nrow]
        a0 = tg_matrix[ncol][nrow][0]
        a1 = tg_matrix[ncol + 1][nrow][0] + np.pi
        I0, I1 = get_center_handles(E0,E1,a0,a1)

        P0 = bezier_point(t_begin, E0,I0,I1,E1)
        P1 = bezier_point(t_end, E0,I0,I1,E1)
        b0 = bezier_tangent(t_begin,E0,I0,I1,E1)
        b1 = bezier_tangent(t_end,E0,I0,I1,E1) + np.pi

        E0_1,I0_1,I1_1,E1_1 = split_cubic_bezier(E0,I0,I1,E1,t_begin)
        E1_2,I1_2,I0_2,E0_2 = split_cubic_bezier(E1,I1,I0,E0,1-t_end)

        hpath.push(
            f'M{E0_1[0]},{E0_1[1]} C{I0_1[0]} {I0_1[1]},{I1_1[0]} {I1_1[1]},{E1_1[0]} {E1_1[1]}'
        )
        hpath.push(create_coupling(P0,P1,b0,b1,random.randint(0,1)))
        hpath.push(
            f'M{E1_2[0]},{E1_2[1]} C{I1_2[0]} {I1_2[1]},{I0_2[0]} {I0_2[1]},{E0_2[0]} {E0_2[1]}'
        )
    
    dwg.add(hpath)
    
border = dwg.path().stroke('black',width=0.5).fill('none')
border.push(f'M0,0 H{width} V{height}')
border.push(f'M0,0 V{height} H{width}')
dwg.add(border)

dwg.save()