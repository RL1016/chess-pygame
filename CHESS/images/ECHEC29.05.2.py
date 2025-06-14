import sys
import pygame as pg

#Global Var
SCREEN_WIDTH = 612
SCREEN_HEIGHT = 612

Playing = True

#coordonées de chaques pièces blanches
pionB = {1 : (45, 435), 2 : (110, 435), 3 : (175, 435), 4 : (240, 435), 5 : (305, 435), 6 : (370, 435), 7 : (435, 435), 8 : (500, 435)}
tourB = {1 : (45, 500), 2 : (500, 500)}
cavalierB = {1 : (110, 500), 2 : (435, 500)}
fouB = {1 : (175, 500), 2 : (370, 500)}
dameB = {1 : (305, 500)}
roiB = {1 : (240, 500)}

#coordonées de chaques pièces noires
pionN = {1 : (45, 110), 2 : (110, 110), 3 : (175, 110), 4 : (240, 110), 5 : (305, 110), 6 : (370, 110), 7 : (435, 110), 8 : (500, 110) }
tourN = {1 : (45, 45), 2 : (500, 45)}
cavalierN = {1 : (110, 45), 2 : (435, 45)}
fouN = {1 : (175, 45), 2 : (370, 45)}
dameN = {1 : (305, 45)}
roiN = {1 : (240, 45)}

pièces = [pionB, tourB, cavalierB, fouB, dameB, roiB, pionN, tourN, cavalierN, fouN, dameN, roiN]

#importation images
chessboard = pg.image.load("chessboard.jpg")
point = pg.image.load("images/point.xcf")
#pièces blanches
pionBlancImage = pg.image.load("Bureau/images/pionB.xcf")
cavalierBlancImage = pg.image.load("images/cavalierB.xcf")
fouBlancImage = pg.image.load("images/fouB.xcf")
tourBlancImage = pg.image.load("images/tourB.xcf")
roiBlancImage = pg.image.load("images/roiB.xcf")
dameBlancImage = pg.image.load("images/dameB.xcf")
#pièces noires
pionNoirImage = pg.image.load("images/pionN.xcf")
cavalierNoirImage = pg.image.load("images/cavalierN.xcf")
fouNoirImage = pg.image.load("images/fouN.xcf")
tourNoirImage = pg.image.load("images/tourN.xcf")
roiNoirImage = pg.image.load("images/roiN.xcf")
dameNoirImage = pg.image.load("images/dameN.xcf")


#Window init
pg.init()

#Créer le display et lui donne un nom
screen = pg.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )
pg.display.set_caption("chess")



#fonctions
def affichage_pièces() :
    for p in range(1, 9) :
        screen.blit(pionBlancImage, pionB[p])
        screen.blit(pionNoirImage, pionN[p])
    for idx in range(1, 3) :
        screen.blit(cavalierBlancImage, cavalierB[idx])
        screen.blit(cavalierNoirImage, cavalierN[idx])
        screen.blit(fouBlancImage, fouB[idx])
        screen.blit(fouNoirImage, fouN[idx])       
        screen.blit(tourBlancImage, tourB[idx])
        screen.blit(tourNoirImage, tourN[idx])
    screen.blit(roiBlancImage, roiB[1])
    screen.blit(roiNoirImage, roiN[1])
    screen.blit(dameBlancImage, dameB[1])
    screen.blit(dameNoirImage, dameN[1])
    
def coordonee_case(ligne:int, colone:int) :
    for i in range(9) :
        if colone == i :
            x = 45 + i*65
        if ligne == i :
            y = 45 + i*65
    return (x, y)



def trouver_pièce_sellectioner() :
    #trouver coordonées de la case sur laquelle a cliqué le joueur 
        x, y = pg.mouse.get_pos()
        ligne = (y-45) // 65 
        colone = (x-45) // 65
        cooCase = coordonee_case(ligne, colone)
        #grâce au coordonées de la case, déterminer quelle pièce s'y trouve
        for dico in pièces :
                for key, values in dico.items() :
                    if values == cooCase :
                        return (dico,key) 
        else :
            return None

def trouver_case_ou_déplacer() :
    x, y = pg.mouse.get_pos()
    ligne = (y-45) // 65 
    colone = (x-45) // 65
    return coordonee_case(ligne, colone)


def tour_joueur() :
    clique = 0
    while clique < 2 :
        Player = True
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 :
                pièce = trouver_pièce_sellectioner()
                if pièce != None :
                    clique += 1
                    nouvelle_case = trouver_case_ou_déplacer()
                    clique += 1 
                    pièce[0][pièce[1]] = nouvelle_case


#Boucle de jeu
while Playing :
    clique = 0 
    screen.blit(chessboard, (0,0) )
    affichage_pièces()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            Playing = False
            pg.quit()
            sys.exit()
        tour_joueur()
            
                
            
    pg.display.flip()

