from fileget import animallist, PATH
import os

for i in range(0,83):
    os.makedirs(PATH+str(animallist[i])+'\\normal')
