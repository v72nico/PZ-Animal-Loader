import glob2
import os

animallist = ['Aardvark', 'African Buffalo', 'African Elephant', 'African Wild Dog', 'Aldabra Giant Tortoise', 'Amazonian Giant Centipede', 'American Bison', 'Arctic Wolf', 'Bactrian Camel', 'Bairds Tapir',\
 'Bengal Tiger', 'Black Wildebeest', 'Boa Constrictor', 'Bongo', 'Bonobo', 'Bornean Orangutan', 'Brazilian Salmon Pink Tarantula', 'Brazilian Wandering Spider', 'Cheetah', 'Colombian White-Faced Capuchin Monkey', 'Chinese Pangolin',\
 'Common Death Adder', 'Common Ostrich', 'Common Warthog', 'Dall Sheep', 'Eastern Brown Snake', 'Formosan Black Bear', 'Galapagos Giant Tortoise', 'Gemsbok', 'Gharial', 'Giant Anteater', 'Giant Burrowing Cockroach',\
 'Giant Desert Hairy Scorpion', 'Giant Forest Scorpion', 'Giant Panda', 'Giant Tiger Land Snail', 'Gila Monster', 'Golden Poison Frog', 'Goliath Beetle', 'Goliath Birdeater', 'Goliath Frog',\
 'Greater Flamingo', 'Green Iguana', 'Grizzly Bear', 'Himalayan Brown Bear', 'Hippopotamus', 'Indian Elephant', 'Indian Peafowl', 'Indian Rhinoceros', 'Jaguar', 'Japanese Macaque', 'Komodo Dragon',\
 'Lehmanns Poison Frog', 'Lesser Antillean Iguana', 'Llama', 'Mandrill', 'Mexican Redknee Tarantula', 'Nile Monitor', 'Nyala', 'Okapi', 'Plains Zebra', 'Polar Bear', 'Pronghorn Antelope', 'Puff Adder', 'Pygmy Hippo', 'Red Panda', 'Red Ruffed Lemur', 'Red-Eyed Tree Frog',\
 'Reindeer', 'Reticulated Giraffe', 'Ring Tailed Lemur', 'Sable Antelope', 'Saltwater Crocodile', 'Siberian Tiger', 'Snow Leopard', 'Spotted Hyena', 'Springbok', 'Thomsons Gazelle', 'Timber Wolf', 'Titan Beetle',\
 'West African Lion', 'Western Chimpanzee', 'Western Diamondback Rattlesnake', 'Western Lowland Gorilla', 'Yellow Anaconda', 'Main']


PATH = os.path.dirname(os.path.realpath(__file__))+'\\mods'

a=len(animallist)
b=len(animallist)-1

def fileget():
    modfolders = []
    for i in range(0,a):
        modfolders.append(glob2.glob(PATH+'\\'+str(animallist[i])+'\\*\\'))
    return modfolders
	
def filegetzoo():
    modfolders = []
    for i in range(0,b):
        modfolders.append(glob2.glob(PATH+'\\Zoopedia\\'+str(animallist[i])+'\\*\\'))
    return modfolders
    
def foldersget(modfolders):
    allfolder = []
    for i in range(0,a):
        foldo = []
        for k in range(0,len(modfolders[i])):
            foldo.append(os.path.basename(os.path.normpath(modfolders[i][k])))
        allfolder.append(foldo)
    return allfolder
    
def whatempty(modfolders):
    inuse = []
    for i in range(0,a):
        for k in range(0,len(modfolders[i])):
            if not os.listdir(modfolders[i][k]):
                inuse.append(modfolders[i][k])
    return inuse
    
def whatemptylst(modfolders):
    inuseall = []
    for i in range(0,a):
        for k in range(0,len(modfolders[i])):
            if not os.listdir(modfolders[i][k]):
                for z in (z for z,x in enumerate(modfolders[i]) if x == modfolders[i][k]):
                    inuseall.append(z)
    return inuseall


