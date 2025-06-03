"""We show here how to set up a drop down list (list of predefined choices that the user can click)"""

import pygame, thorpy as tp, numpy as np
from os import listdir
from os.path import isfile,join
from read import read_dat, read_np

#get all files from ../data
data_files = [f for f in listdir("../data") if isfile(join("../data", f))]
print(data_files)

#filter by usefulness if they are in ../interesting_mes.txt
interesting_mes = []
with open("../interesting_mes.txt") as f:
    interesting_mes = f.readlines()
    interesting_mes = [x.strip() for x in interesting_mes]

data_files = [f for f in data_files if f.split(".")[0] in interesting_mes]
data_files.sort()
print(data_files)

pygame.init()

W, H = 1200, 700
screen = pygame.display.set_mode((W,H))
theme = tp.theme_classic

tp.init(screen, theme) #bind screen to gui elements and set theme

bck = pygame.image.load(tp.fn("data/bck.jpg")) #load some background pic for testing
bck = pygame.transform.smoothscale(bck, (W,H))
# def before_gui(): #add here the things to do each frame before blitting gui elements
#     screen.blit(bck, (0,0)) #blit background pic
# tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.

ddl1 = tp.DropDownListButton(["None"] + data_files)
ddl1_labelled = tp.Labelled("Fichier Source", ddl1)

prevname = None
signal = None
def update_sig():
    global signal, time_max, time_min, val_max, val_min, prevname, markers
    name = ddl1.get_value()
    print("Update sig received")
    if name is None or name == prevname:
        return
    if name == "None":
        signal = None
        prevname = None
        return
    print("Name:",name)
    prevname = name
    signal = read_np(name, "../data")[:,:2]
    print(signal[0])
    time_max = signal[:,0].max()
    time_min = signal[:,0].min()
    val_max = signal[:,1].max()
    val_min = signal[:,1].min()
    markers = []

def time_volt_to_rel(val_min, val_max, time_min, time_max, val, time):
    relx = (time-time_min)/(time_max-time_min)-0.5
    rely = (val-val_min)/(val_max-val_min)-0.5
    return relx, rely

def rel_to_time_volt(relx,rely):
    time = (relx+0.5)*(time_max-time_min)+time_min
    val = (rely+0.5)*(val_max-val_min)+val_min
    return time,val

def rel_to_screen(x,y):
    sx = PW*(x*plot_scale+0.5)+PX-plot_loc[0]*plot_scale
    sy = PH*(-y*plot_scale+0.5)+PY-plot_loc[1]*plot_scale
    return sx,sy

def screen_to_rel(sx,sy):#seems ok assuming rel_to_screen
    relx = ((sx-PX+plot_loc[0]*plot_scale)/PW-0.5)/plot_scale
    rely = -((sy-PY+plot_loc[1]*plot_scale)/PH-0.5)/plot_scale
    return relx,rely

def time_volt_to_screen(val_min, val_max, time_min, time_max, val, time):
    relx,rely = time_volt_to_rel(val_min, val_max, time_min, time_max, val, time)
    return rel_to_screen(relx,rely)

def screen_to_time_volt(x, y):
    relx, rely = screen_to_rel(x, y)
    return rel_to_time_volt(relx, rely)

ddl1.at_change = update_sig

def save_labels():
    if prevname is None:
        return
    print("Saving labels")
    
    #save labels in a file
    with open("../labels/"+prevname.split(".")[0]+".txt", "w") as f:
        e=np.searchsorted(signal[:,0], [i[0] for i in markers] )
        print(e)

        for marker, index in sorted(zip(markers,e), key=lambda x: x[1]):
            f.write(",".join(list(map(str, marker+(index,))))+"\n")
    print("Labels saved")

def load_labels():
    global markers
    if prevname is None:
        return
    print("Loading labels")
    try:
        with open("../labels/" + prevname.split(".")[0] + ".txt", "r") as f:
            markers = []
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 2:
                    time, value = map(float, parts[:2])
                    markers.append((time, value))
        print("Labels loaded:", markers)
    except FileNotFoundError:
        print("No labels file found for", prevname)

ddl3 = tp.Button(text="Load_Labels")
ddl3.at_unclick = load_labels

ddl1.at_unclick = update_sig

ddl2 = tp.Button(text="Save_Labels")
ddl2.at_unclick = save_labels

#to get the value of any my_ddl, just call my_ddl.get_value()

group = tp.Box([ddl1_labelled, ddl2, ddl3])
group.sort_children("h")
# group.set_size((1200, 100))
group.set_topleft(0,0)

def blit_be4_gui():
    screen.fill((255,255,255))

font = pygame.font.Font(None, 24)

plot_zone = PX, PY, PW, PH = (0,100,1200,600)
plot_loc = [0,0]
scale_opt = [0.5,1,1.5,2,3,4,5,8,10]
DEFAULT_SCALE_IDX = 1
scale_index = DEFAULT_SCALE_IDX
plot_scale = scale_opt[DEFAULT_SCALE_IDX]

updater = group.get_updater()
clock = pygame.time.Clock()
playing = True
while updater.playing:
    clock.tick(60)
    events = pygame.event.get()
    pressed = pygame.key.get_pressed()
    mouse_rel = pygame.mouse.get_rel()
    for e in events:
        if e.type == pygame.QUIT:
            playing = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_HOME:
                plot_scale = 1
                scale_index = DEFAULT_SCALE_IDX
                plot_loc = [0,0]
            if e.key == pygame.K_UP:
                scale_index +=1
                if scale_index >= len(scale_opt):
                    scale_index = len(scale_opt)-1
                plot_scale = scale_opt[scale_index]
            if e.key == pygame.K_DOWN:
                scale_index -=1
                if scale_index < 0:
                    scale_index = 0
                
                plot_scale = scale_opt[scale_index]

                print("Scale:",plot_scale, "Index:",scale_index, "Loc:",plot_loc)
            if e.key == pygame.K_LEFT:
                if pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]:
                    plot_loc[0] -= 40
                else:
                    plot_loc[0] -= 400
            if e.key == pygame.K_RIGHT:
                if pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]:
                    plot_loc[0] += 40
                else:
                    plot_loc[0] += 400
        if e.type == pygame.MOUSEBUTTONUP:
            print("Mouse up")
            #get location of mouse within the plot_zone
            x,y = pygame.mouse.get_pos()
            if (prevname is not None) and (PX<=x<=PX+PW and PY<=y<=PY+PH):
                print("Mouse up in plot_zone")
                #convert to time and value
                time,value = screen_to_time_volt(x,y)
                print("Time:",time)
                print("Value:",value)
                #add/remove a marker
                existing = False
                for marker in markers:
                    #convert marker to screen coords
                    mx,my = marker
                    sx,sy = time_volt_to_screen(val_min, val_max, time_min, time_max, my, mx)
                    if (sx-x)**2+(sy-y)**2 <= 40:
                        markers.remove(marker)
                        existing = True
                        break
                if not existing:
                    markers.append((time,value))
            

    
    

    screen.fill((255,255,255))
    group.set_topleft(0,0)
    updater.update(blit_be4_gui, events=events, mouse_rel=mouse_rel)

    #display the time data within the plot_zone using max and min values
    if prevname is not None:
        #show markers
        for marker in markers:
            mx,my = marker
            sx,sy = time_volt_to_screen(val_min, val_max, time_min, time_max, my, mx)
            pygame.draw.circle(screen, (10,10,10), (int(sx),int(sy)), 5)

        # Draw scale to the left, accounting for zoom and offset, use time_volt_to_screen and pass dummy time arguments not to be used like 0
        for i in range(11):  # Divide the scale into 10 parts
            value = val_min + i * (val_max - val_min) / 10
            _, y = time_volt_to_screen(val_min, val_max, time_min, time_max, value, 0)  # Use dummy time argument
            pygame.draw.line(screen, (0, 0, 0), (PX - 10, y), (PX, y), 2)
            label = font.render(str(round(value, 2)), True, (0, 0, 0))
            screen.blit(label, (PX +20, y - 10))

        # Do the same scale but horizontally
        for i in range(8*2+1):  # Divide the scale into 10 parts
            time = time_min + i * (time_max - time_min) / 16
            x, _ = time_volt_to_screen(val_min, val_max, time_min, time_max, 0, time)  # Use dummy value argument
            pygame.draw.line(screen, (0, 0, 0), (x, PY + PH), (x, PY + PH - 2), 2)
            label = font.render(str(round(time, 2)), True, (0, 0, 0))
            screen.blit(label, (x , PY + PH -20))



        #showsignal
        newsig = np.copy(signal)
        ampx = PW/(time_max-time_min)
        ampy = PH/(val_max-val_min)

        newsig[:,0], newsig[:,1] = time_volt_to_screen(val_min, val_max, time_min, time_max, newsig[:,1], newsig[:,0])

        # newsig[:,0] = (((signal[:,0]-time_min)*ampx-PW/2)*plot_scale + PW/2)+PX-plot_loc[0]*plot_scale
        # newsig[:,1] = (PH/2-(signal[:,1]-val_min)*ampy)*plot_scale+PH/2+PY-plot_loc[1]*plot_scale
        pygame.draw.aalines(screen, (0,0,0), False, tuple(newsig), 2)
    

    pygame.display.update()
pygame.quit()
