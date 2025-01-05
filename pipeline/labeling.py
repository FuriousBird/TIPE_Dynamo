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

alert = tp.Alert("Congratulations", "That was a nice click.\nNo, really, you performed well.")

prevname = None
signal = None
def update_sig():
    global signal, time_max, time_min, val_max, val_min, prevname, markers
    name = ddl1.get_value()
    print("Update sig received")
    if name is None or name == prevname:
        return
    if name == "None":
        print("ALERT!!!")
        prevname = None
        alert.launch_alone(click_outside_cancel=True) #tune some options if you like
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

ddl1.at_unclick = update_sig

ddl2 = tp.Button(text="Save_Labels")
ddl2.at_unclick = save_labels

#to get the value of any my_ddl, just call my_ddl.get_value()

group = tp.Box([ddl1_labelled, ddl2])
group.sort_children("h")
# group.set_size((1200, 100))
group.set_topleft(0,0)

def blit_be4_gui():
    screen.fill((255,255,255))

plot_zone = PX, PY, PW, PH = (0,100,1200,600)
plot_scale = 1

updater = group.get_updater()
clock = pygame.time.Clock()
playing = True
while updater.playing:
    clock.tick(60)
    events = pygame.event.get()
    mouse_rel = pygame.mouse.get_rel()
    for e in events:
        if e.type == pygame.QUIT:
            playing = False
        if e.type == pygame.MOUSEBUTTONUP:
            print("Mouse up")
            #get location of mouse within the plot_zone
            x,y = pygame.mouse.get_pos()
            if (prevname is not None) and (PX<=x<=PX+PW and PY<=y<=PY+PH):
                print("Mouse up in plot_zone")
                #convert to time and value
                time = (x-PX)/(PW/(time_max-time_min))+time_min
                value = val_max-(y-PY)/(PH/(val_max-val_min))
                print("Time:",time)
                print("Value:",value)
                #add/remove a marker
                existing = False
                for marker in markers:
                    #convert marker to screen coords
                    mx,my = marker
                    mx = (mx-time_min)/(time_max-time_min)*PW+PX
                    my = PH-(my-val_min)/(val_max-val_min)*PH+PY
                    if (mx-x)**2+(my-y)**2 <= 40:
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
            mx = (mx-time_min)/(time_max-time_min)*PW+PX
            my = PH-(my-val_min)/(val_max-val_min)*PH+PY
            pygame.draw.circle(screen, (10,10,10), (int(mx),int(my)), 5)
        #showsignal
        newsig = np.copy(signal)
        ampx = PW/(time_max-time_min)
        ampy = PH/(val_max-val_min)
        newsig[:,0] = (signal[:,0]-time_min)*ampx+PX
        newsig[:,1] = PH-(signal[:,1]-val_min)*ampy+PY
        pygame.draw.aalines(screen, (0,0,0), False, tuple(newsig), 2)
    

    pygame.display.update()
pygame.quit()
