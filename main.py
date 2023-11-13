import pygame as pg
import numpy as np
from numba import njit

def main():
    # Inicialización de Pygame y configuración de la ventana
    pg.init()
     # Parámetros y variables del juego
    screen = pg.display.set_mode((800,600))
    running = True
    clock = pg.time.Clock()
    pg.mouse.set_visible(False)
    pg.event.set_grab(1)

    hres = 250 
    halfvres = int(hres*0.375)
    mod = hres/60

    size = 25
    nenemies = size*2
    posx, posy, rot, maph, mapc, exitx, exity = gen_map(size)
    
    frame = np.random.uniform(0,1, (hres, halfvres*2, 3))
    sky = pg.image.load('skybox2.jpg')
    sky = pg.surfarray.array3d(pg.transform.smoothscale(sky, (720, halfvres*2)))/255
    floor = pg.surfarray.array3d(pg.image.load('floor.jpg'))/255
    wall = pg.surfarray.array3d(pg.image.load('wall.jpg'))/255
    sprites, spsize, sword, swordsp = get_sprites(hres)

    playing = False 

    while running:
         # Parámetros y variables del juego
        ticks = pg.time.get_ticks()/200
        er = min(clock.tick()/500, 0.3)
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                playing = True
            if swordsp < 1 and event.type == pg.MOUSEBUTTONDOWN:
                swordsp = 1

        # Actualización del frame del juego    
        frame = new_frame(posx, posy, rot, frame, sky, floor, hres, halfvres, mod, maph, size,
                          wall, mapc, exitx, exity)

        # Creación de la superficie de Pygame a partir del frame
        surf = pg.surfarray.make_surface(frame*255)
        
        # Dibujar sprites en la superficie
        surf = draw_sprites(surf, sprites, spsize, hres, halfvres, ticks, sword, swordsp)
        
        # Escalar la superficie a la resolución de la ventana
        surf = pg.transform.scale(surf, (800, 600))
        
        if int(swordsp) > 0:
            swordsp = (swordsp + er*5)%4

        screen.blit(surf, (0,0))
        pg.display.update()
        fps = int(clock.get_fps())
        pg.display.set_caption("FPS: " + str(fps))
        posx, posy, rot = movement(pg.key.get_pressed(), posx, posy, rot, maph, er)

def movement(pressed_keys, posx, posy, rot, maph, et):
    # Manejo de eventos de movimiento (teclas y ratón)
    x, y, rot0, diag = posx, posy, rot, 0
    if pg.mouse.get_focused():
        p_mouse = pg.mouse.get_rel()
        rot = rot + np.clip((p_mouse[0])/200, -0.2, .2)

    if pressed_keys[pg.K_UP] or pressed_keys[ord('w')]:
        x, y, diag = x + et*np.cos(rot), y + et*np.sin(rot), 1

    elif pressed_keys[pg.K_DOWN] or pressed_keys[ord('s')]:
        x, y, diag = x - et*np.cos(rot), y - et*np.sin(rot), 1
        
    if pressed_keys[pg.K_LEFT] or pressed_keys[ord('a')]:
        et = et/(diag+1)
        x, y = x + et*np.sin(rot), y - et*np.cos(rot)
        
    elif pressed_keys[pg.K_RIGHT] or pressed_keys[ord('d')]:
        et = et/(diag+1)
        x, y = x - et*np.sin(rot), y + et*np.cos(rot)


    if not(maph[int(x-0.2)][int(y)] or maph[int(x+0.2)][int(y)] or
           maph[int(x)][int(y-0.2)] or maph[int(x)][int(y+0.2)]):
        posx, posy = x, y
        
    elif not(maph[int(posx-0.2)][int(y)] or maph[int(posx+0.2)][int(y)] or
             maph[int(posx)][int(y-0.2)] or maph[int(posx)][int(y+0.2)]):
        posy = y
        
    elif not(maph[int(x-0.2)][int(posy)] or maph[int(x+0.2)][int(posy)] or
             maph[int(x)][int(posy-0.2)] or maph[int(x)][int(posy+0.2)]):
        posx = x
        
    return posx, posy, rot

def gen_map(size):
    # Generación aleatoria del mapa y configuración inicial del jugador

    mapc = np.random.uniform(0,1, (size,size,3)) 
    maph = np.random.choice([0, 0, 0, 0, 1, 1], (size,size))
    maph[0,:], maph[size-1,:], maph[:,0], maph[:,size-1] = (1,1,1,1)

    posx, posy, rot = 1.5, np.random.randint(1, size -1)+.5, np.pi/4
    x, y = int(posx), int(posy)
    maph[x][y] = 0
    count = 0
    while True:
        testx, testy = (x, y)
        if np.random.uniform() > 0.5:
            testx = testx + np.random.choice([-1, 1])
        else:
            testy = testy + np.random.choice([-1, 1])
        if testx > 0 and testx < size -1 and testy > 0 and testy < size -1:
            if maph[testx][testy] == 0 or count > 5:
                count = 0
                x, y = (testx, testy)
                maph[x][y] = 0
                if x == size-2:
                    exitx, exity = (x, y)
                    break
            else:
                count = count+1
    return posx, posy, rot, maph, mapc, exitx, exity

@njit()
def new_frame(posx, posy, rot, frame, sky, floor, hres, halfvres, mod, maph, size, wall, mapc, exitx, exity):
    # Generación de un nuevo frame para la vista en primera persona
    for i in range(hres):
        rot_i = rot + np.deg2rad(i/mod - 30)
        sin, cos, cos2 = np.sin(rot_i), np.cos(rot_i), np.cos(np.deg2rad(i/mod - 30))
        frame[i][:] = sky[int(np.rad2deg(rot_i)*2%718)][:]

        x, y = posx, posy
        while maph[int(x)%(size-1)][int(y)%(size-1)] == 0:
            x, y = x +0.01*cos, y +0.01*sin

        n = np.sqrt((x-posx)**2+(y-posy)**2)
        h = int(halfvres/(n*cos2 + 0.001))

        xx = int(x*3%1*99)        
        if x%1 < 0.02 or x%1 > 0.98:
            xx = int(y*3%1*99)
        yy = np.linspace(0, 3, h*2)*99%99

        shade = 0.3 + 0.7*(h/halfvres)
        if shade > 1:
            shade = 1
            
        ash = 0 
        if maph[int(x-0.33)%(size-1)][int(y-0.33)%(size-1)]:
            ash = 1
            
        if maph[int(x-0.01)%(size-1)][int(y-0.01)%(size-1)]:
            shade, ash = shade*0.5, 0
            
        c = shade*mapc[int(x)%(size-1)][int(y)%(size-1)]
        for k in range(h*2):
            if halfvres - h +k >= 0 and halfvres - h +k < 2*halfvres:
                if ash and 1-k/(2*h) < 1-xx/99:
                    c, ash = 0.5*c, 0
                frame[i][halfvres - h +k] = c*wall[xx][int(yy[k])]
                if halfvres+3*h-k < halfvres*2:
                    frame[i][halfvres+3*h-k] = c*wall[xx][int(yy[k])]
                
        for j in range(halfvres -h): #floor
            n = (halfvres/(halfvres-j))/cos2
            x, y = posx + cos*n, posy + sin*n
            xx, yy = int(x*3%1*99), int(y*3%1*99)

            shade = 0.2 + 0.8*(1-j/halfvres)
            if maph[int(x-0.33)%(size-1)][int(y-0.33)%(size-1)]:
                shade = shade*0.5
            elif ((maph[int(x-0.33)%(size-1)][int(y)%(size-1)] and y%1>x%1)  or
                  (maph[int(x)%(size-1)][int(y-0.33)%(size-1)] and x%1>y%1)):
                shade = shade*0.5

            frame[i][halfvres*2-j-1] = shade*(floor[xx][yy]*2+frame[i][halfvres*2-j-1])/3
            
            if int(x) == exitx and int(y) == exity and (x%1-0.5)**2 + (y%1-0.5)**2 < 0.2:
                ee = j/(10*halfvres)
                frame[i][j:2*halfvres-j] = (ee*np.ones(3)+frame[i][j:2*halfvres-j])/(1+ee)

    return frame


def get_sprites(hres):
    # Carga y escala de sprites del jugador y la espada
    sheet = pg.image.load('zombie_n_skeleton4.png').convert_alpha()
    sprites = [[], []]
    swordsheet = pg.image.load('sword1.png').convert_alpha() 
    sword = []
    for i in range(3):
        subsword = pg.Surface.subsurface(swordsheet,(i*800,0,800,600))
        sword.append(pg.transform.smoothscale(subsword, (hres, int(hres*0.75))))
        xx = i*32
        sprites[0].append([])
        sprites[1].append([])
        for j in range(4):
            yy = j*100
            sprites[0][i].append(pg.Surface.subsurface(sheet,(xx,yy,32,100)))
            sprites[1][i].append(pg.Surface.subsurface(sheet,(xx+96,yy,32,100)))

    spsize = np.asarray(sprites[0][1][0].get_size())*hres/800

    sword.append(sword[1]) 
    swordsp = 0 
    
    return sprites, spsize, sword, swordsp

def draw_sprites(surf, sprites, spsize, hres, halfvres, ticks, sword, swordsp):
    # Dibujo de sprites en la superficie del juego
    cycle = int(ticks) % 3  
    types, dir2p = 0, 0  
    cos2 = np.cos(0)  
    scale = spsize * 5 / cos2  
    vert = halfvres + halfvres * 2 / cos2  
    hor = hres / 2 - hres * np.sin(0)  
    spsurf = pg.transform.scale(sprites[types][cycle][dir2p], scale)
    swordpos = (np.sin(ticks) * 10 * hres / 800, (np.cos(ticks) * 10 + 15) * hres / 800)  # shake de la espada
    surf.blit(spsurf, (hor, vert) - scale / 2)
    surf.blit(sword[int(swordsp)], swordpos)

    return surf


if __name__ == '__main__':
    main()
    pg.quit()
