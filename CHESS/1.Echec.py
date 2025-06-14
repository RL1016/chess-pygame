import sys
import pygame as pg
import os
import socket
import threading

#Global Var
SCREEN_WIDTH = 612
SCREEN_HEIGHT = 612

chossen_time = None
WHITE_TIME = 600
BLACK_TIME = 600
WHITE_TIME_LEFT = 600 
BLACK_TIME_LEFT = 600  

Playing = True

first_player_name = ""
second_player_name = ""

number_of_moves = 0
fifty_move_counter = 0

position_history = []

chosen_mode = None

#coordonées de chaques pièces blanches
pionB = {1 : (45, 435), 2 : (110, 435), 3 : (175, 435), 4 : (240, 435), 5 : (305, 435), 6 : (370, 435), 7 : (435, 435), 8 : (500, 435)}
tourB = {1 : (45, 500), 2 : (500, 500)}
cavalierB = {1 : (110, 500), 2 : (435, 500)}
fouB = {1 : (175, 500), 2 : (370, 500)}
dameB = {1 : (240, 500)}
roiB = {1 : (305, 500)}

#coordonées de chaques pièces noires
pionN = {1 : (45, 110), 2 : (110, 110), 3 : (175, 110), 4 : (240, 110), 5 : (305, 110), 6 : (370, 110), 7 : (435, 110), 8 : (500, 110) }
tourN = {1 : (45, 45), 2 : (500, 45)}
cavalierN = {1 : (110, 45), 2 : (435, 45)}
fouN = {1 : (175, 45), 2 : (370, 45)}
dameN = {1 : (240, 45)}
roiN = {1 : (305, 45)}


pieces = [pionB, tourB, cavalierB, fouB, dameB, roiB, pionN, tourN, cavalierN, fouN, dameN, roiN]
white = [pionB, cavalierB, fouB, tourB, dameB, roiB]
black = [pionN, cavalierN, fouN, tourN, dameN, roiN]
#pour le roque, il faut savoir si roi et tour on bougé ou non
roiB_has_moved = False
roiN_has_moved = False
tourB1_has_moved = False  
tourB2_has_moved = False  
tourN1_has_moved = False  
tourN2_has_moved = False  

#variable pour la prise ne passant 
en_passant_square = None

#variable pour gérer le système de tour
curent_turn = "white"

#Chemin des images
IMG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
chessboard = pg.image.load(os.path.join(IMG_PATH, "chessboard2.jpg"))
point = pg.image.load(os.path.join(IMG_PATH, "point.xcf"))
# pièces blanches  
pionBlancImage = pg.image.load(os.path.join(IMG_PATH, "pionB.xcf"))
cavalierBlancImage = pg.image.load(os.path.join(IMG_PATH, "cavalierB.xcf"))
fouBlancImage = pg.image.load(os.path.join(IMG_PATH, "fouB.xcf"))
tourBlancImage = pg.image.load(os.path.join(IMG_PATH, "tourB.xcf"))
roiBlancImage = pg.image.load(os.path.join(IMG_PATH, "roiB.xcf"))
dameBlancImage = pg.image.load(os.path.join(IMG_PATH, "dameB.xcf"))
# pièces noires
pionNoirImage = pg.image.load(os.path.join(IMG_PATH, "pionN.xcf"))
cavalierNoirImage = pg.image.load(os.path.join(IMG_PATH, "cavalierN.xcf"))
fouNoirImage = pg.image.load(os.path.join(IMG_PATH, "fouN.xcf"))
tourNoirImage = pg.image.load(os.path.join(IMG_PATH, "tourN.xcf"))
roiNoirImage = pg.image.load(os.path.join(IMG_PATH, "roiN.xcf"))
dameNoirImage = pg.image.load(os.path.join(IMG_PATH, "dameN.xcf"))

#Window init
pg.init()

#Créer le display et lui donne un nom
screen = pg.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )
pg.display.set_caption("chess")

# fonctions d'affichage --------------------------------------------------------------------------

def ask_players_name() :
    #demander aux joueurs de saisir leurs noms ainsi que choisir leur cadance
    #possibilité également de jouer en ligne
    global first_player_name, second_player_name
    global chosen_time
    font = pg.font.SysFont(None, 40)
    input_box_white = pg.Rect(180, 200, 250, 50)
    input_box_black = pg.Rect (180, 300, 250, 50)
    color_inactive = pg.Color("white")
    color_active = pg.Color("grey")
    color_white = color_inactive
    color_black = color_inactive
    
    active_white = False
    active_black = False
    text_white = ''
    text_black = ''
    done = False
    selected_time = False

    small_font = pg.font.SysFont(None, 36)

    # bouton pour jouer en ligne
    # bouton pour créé une partie en ligne
    create_button_text = small_font.render("Créé partie", True, (255, 255, 255))
    create_button_rect = pg.Rect(0, 0, 200, 50)
    create_button_rect.center = (105, 30)
    #bouton pour rejoindre une partie en ligne
    join_button_texte = small_font.render("Rejoindre partie", True, (255, 255, 255))
    join_button_rect = pg.Rect(0, 0, 200, 50)
    join_button_rect.center = (SCREEN_WIDTH - 105, 30)

    # Bouton pour choisir la cadence de jeu
    # 10 minutes
    ten_button_text = small_font.render("10 min", True, (255, 255, 255))
    ten_button_rect = pg.Rect(0, 0, 180, 50)
    ten_button_rect.center = (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 100)
    # 5 minutes
    five_button_text = small_font.render("5 min", True, (255, 255, 255))
    five_button_rect = pg.Rect(0, 0, 180, 50)
    five_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
    # 3 minutes
    three_button_text = small_font.render("3 min", True, (255, 255, 255))
    three_button_rect = pg.Rect(0, 0, 180, 50)
    three_button_rect.center = (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 + 100)

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                '''
                if create_button_rect.collidepoint(event.pos) :
                    chosen_mode = 
                elif join_button_rect.collidepoint(event.pos) :
                    '''
                # Si clic sur une box, active la saisie
                if input_box_white.collidepoint(event.pos) :
                    color_white = color_active
                    active_white = True
                    active_black = False
                elif input_box_black.collidepoint(event.pos) :
                    color_black = color_active
                    active_black = True
                    active_white = False
                else:
                    active_white = False
                    active_black = False
                if text_white and text_black :
                    if ten_button_rect.collidepoint(event.pos) :
                        chosen_time = 600
                        selected_time = 600
                        done = True
                    elif five_button_rect.collidepoint(event.pos) :
                        chosen_time = 300
                        selected_time = 300
                        done = True
                    elif three_button_rect.collidepoint(event.pos) :
                        chosen_time = 180
                        selected_time = 180
                        done = True
            if event.type == pg.KEYDOWN:
                if active_white:
                    if event.key == pg.K_RETURN:
                        active_white = False
                    elif event.key == pg.K_BACKSPACE:
                        text_white = text_white[:-1]
                    else:
                        if len(text_white) < 15:
                            text_white += event.unicode
                elif active_black:
                    if event.key == pg.K_RETURN:
                        active_black = False
                    elif event.key == pg.K_BACKSPACE:
                        text_black = text_black[:-1]
                    else:
                        if len(text_black) < 15:
                            text_black += event.unicode

        screen.fill((23, 66, 102))
        title = font.render("Entrez le nom des joueurs", True, (255, 255, 255))
        screen.blit(title, (120, 100))
        txt_surface_white = font.render(text_white or "Nom des blancs", True, (255, 255, 255))
        txt_surface_black = font.render(text_black or "Nom des noirs", True, (255, 255, 255))
        pg.draw.rect(screen, color_white if active_white else color_inactive, input_box_white, 2)
        pg.draw.rect(screen, color_black if active_black else color_inactive, input_box_black, 2)
        screen.blit(txt_surface_white, (input_box_white.x+5, input_box_white.y+10))
        screen.blit(txt_surface_black, (input_box_black.x+5, input_box_black.y+10))
        pg.draw.rect(screen, (10, 44, 81), ten_button_rect, border_radius=10)
        screen.blit(ten_button_text, ten_button_text.get_rect(center=ten_button_rect.center))
        pg.draw.rect(screen, (10, 44, 81), five_button_rect, border_radius=10)
        screen.blit(five_button_text, five_button_text.get_rect(center=five_button_rect.center))
        pg.draw.rect(screen, (10, 44, 81), three_button_rect, border_radius=10)
        screen.blit(three_button_text, three_button_text.get_rect(center=three_button_rect.center))
        pg.draw.rect(screen, (10, 44, 81), create_button_rect, border_radius=10)
        screen.blit(create_button_text, create_button_text.get_rect(center=create_button_rect.center))
        pg.draw.rect(screen, (10, 44, 81), join_button_rect, border_radius=10)
        screen.blit(join_button_texte, join_button_texte.get_rect(center=join_button_rect.center))
        pg.display.flip()

    first_player_name = text_white
    second_player_name = text_black 
    WHITE_TIME, BLACK_TIME = selected_time, selected_time
    WHITE_TIME_LEFT, BLACK_TIME_LEFT = selected_time, selected_time

def print_pieces() :
    # affiche les pièces  
    for p in (pionB.keys()) :
        screen.blit(pionBlancImage, pionB[p])
    for p in (pionN.keys()) :
        screen.blit(pionNoirImage, pionN[p])
    for idx in (tourB.keys()) :
        screen.blit(tourBlancImage, tourB[idx])
    for idx in (tourN.keys()) :
        screen.blit(tourNoirImage, tourN[idx])
    for idx in (cavalierB.keys()) :
        screen.blit(cavalierBlancImage, cavalierB[idx])
    for idx in (cavalierN.keys()) :
        screen.blit(cavalierNoirImage, cavalierN[idx])
    for idx in (fouB.keys()) :
        screen.blit(fouBlancImage, fouB[idx])
    for idx in (fouN.keys()) :
        screen.blit(fouNoirImage, fouN[idx])
    for idx in (roiB.keys()) :
        screen.blit(roiBlancImage, roiB[idx])
    for idx in (roiN.keys()) :
        screen.blit(roiNoirImage, roiN[idx])
    for idx in (dameB.keys()) :
        screen.blit(dameBlancImage, dameB[idx])
    for idx in (dameN.keys()) :
        screen.blit(dameNoirImage, dameN[idx])   

def endgame_print(winner: str):
    #affichage de fin de partie en cas d'echec et mat
    global Playing, number_of_moves
    global first_player_name, second_player_name 
    global WHITE_TIME_LEFT, BLACK_TIME_LEFT
    global curent_turn

    font = pg.font.SysFont(None, 48)
    small_font = pg.font.SysFont(None, 36)
    if winner == "white_on_time" :
        message = f"Plus de temps ! {first_player_name} a gagné!"
        message2 = f"Félicitations {first_player_name} !"
    elif winner == "white" :
        message = f"Plus de temps ! {first_player_name} a gagné!"
        message2 = f"Félicitations {first_player_name} !"
    elif winner == "black_on_time" and WHITE_TIME_LEFT <= 0 :
        message = f"Échec et mat ! {first_player_name} a gagné!"
        message2 = f"Félicitations {first_player_name} !"
    elif winner == "black" :
        message = f"Échec et mat ! {second_player_name} a gagné !"
        message2 = f"Félicitations {second_player_name}"
    elif winner == "white_path" :
        message = "Match nul par Path."
        message2 = f"{first_player_name} ne peut plus bouger"
    elif winner == "black_path" :
        message = "Match nul par Path."
        message2 = f"{second_player_name} ne peut plus bouger"
    elif winner == "material" :
        message = "Math nul par manque de matériel"
        message2 = "Vous ne pouvez pas faire echec et mat"
    elif winner == "fifty" :
        message = "Match nul d'après la règle des 50 coups"
        message2 = "Plus de 50 coups dans capture ou pion bougé"
    elif winner == "three" :
        message = "Match nul par répétition" 
        message2 = "Il y a eu 3 fois la même position"
    
    if curent_turn == "white" :
        move_message = f"Vous avez joué {int((number_of_moves) // 2)} coups dans la partie"
    else :
        move_message = f"Vous avez joué {int((number_of_moves + 1.5) // 2)} coups dans la partie"
    text = font.render(message, True, (255, 0, 0))
    text2 = font.render(message2, True, (255, 0, 0))
    text_moves = small_font.render(move_message, True, (0, 0, 0))
    rect_message = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2  - 40))
    rect_message2 = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    rect_move_message = text_moves.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
    
    # Bouton rejouer
    replay_button_text = small_font.render("Rejouer", True, (255, 255, 255))
    replay_button_rect = pg.Rect(0, 0, 180, 50)
    replay_button_rect.center = (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 80)

    # Bouton quitter
    leave_button_text = small_font.render("Quitter", True, (255, 255, 255))
    leave_button_rect = pg.Rect(0, 0, 180, 50)
    leave_button_rect.center = (SCREEN_WIDTH // 2 + 120, SCREEN_HEIGHT // 2 + 80)

    while True:
        screen.fill((23, 66, 102))
        screen.blit(text, rect_message)
        screen.blit(text2, rect_message2)
        screen.blit(text_moves, rect_move_message)

        pg.draw.rect(screen, (10, 44, 81), replay_button_rect, border_radius=10)
        screen.blit(replay_button_text, replay_button_text.get_rect(center=replay_button_rect.center))
        pg.draw.rect(screen, (10, 44, 81), leave_button_rect, border_radius=10)
        screen.blit(leave_button_text, leave_button_text.get_rect(center=leave_button_rect.center))
        pg.display.flip()
        for event in pg.event.get() :
            if event.type == pg.QUIT :
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 :
                if replay_button_rect.collidepoint(event.pos) :
                    reset_game()
                    Playing = True
                    return
                elif leave_button_rect.collidepoint(event.pos) :
                    Playing = False
                    pg.quit()
                    sys.exit()
                
def chrono_print() :
    #affichage du chrono des deux joueurs 
    global first_player_name, second_player_name

    font = pg.font.SysFont(None, 32)
    
    white_min, white_sec = divmod(WHITE_TIME_LEFT, 60)
    black_min, black_sec = divmod(BLACK_TIME_LEFT, 60)

    pg.draw.rect(screen, (0, 0, 0), (0, 0, SCREEN_WIDTH, 40))  # bande en haut pour afficher chrono
    white_text = font.render(f"{first_player_name} : {white_min:02} : {white_sec:02}", True, (255, 255, 255) )
    black_text = font.render(f"{second_player_name} : {black_min:02} : {black_sec:02}", True, (255, 255, 255) )
    
    screen.blit(white_text, (5, 10))
    screen.blit(black_text, (320, 10))

# fonctions utilitaires ------------------------------------------------------------   
        
def coordonee_case(line:int, column:int) :
    #donne les coordonée d'une case grâce à sa colone et sa ligne 
    x = 45 + column * 65
    y = 45 + line * 65
    return (x, y)

def find_selected_piece() :
    #trouver coordonées de la case sur laquelle a cliqué le joueur 
        x, y = pg.mouse.get_pos()
        ligne = (y-45) // 65 
        colone = (x-45) // 65
        cooCase = coordonee_case(ligne, colone)
        #grâce au coordonées de la case, déterminer quelle pièce s'y trouve
        for dico in pieces :
                for key, values in dico.items() :
                    if values == cooCase :
                        return (dico,key) 
        else :
            return None

def find_case_where_to_move() :
    #trouver les coordonées de la case sur laquelle le joueur veut déplacer la pièce
    x, y = pg.mouse.get_pos()
    ligne = (y-45) // 65 
    colone = (x-45) // 65
    return coordonee_case(ligne, colone)

def check_case(coordonee:tuple) :
    #vérifier si la case est vide
    for dico in pieces :
        for key, values in dico.items() :
            if values == coordonee :
                return False
    return True

def remove_pieces(coordonee:tuple) :
    #supprimer la pièce de son dictionnaire
    for dico in pieces :
        for key, values in list(dico.items()) :
            if values == coordonee :
                del dico[key]
                return
            
def is_check(king_color:str) :
    #vérifier si le roi est en echec 
    if king_color == "white" :
        if 1 not in roiB :
            return False
        king_coo = roiB[1]
        enemy_pieces = [pionN, cavalierN, fouN, tourN, dameN]
        enemy_color = "black"
    else :
        if 1 not in roiN :
            return False
        king_coo = roiN[1]
        enemy_pieces = [pionB, cavalierB, fouB, tourB, dameB]
        enemy_color = "white"
    
    for dico in enemy_pieces :
        for key, coo in list(dico.items()) :
            if dico is pionB or dico is pionN :
                if check_pon_move(coo, king_coo, enemy_color) :
                    return True
            elif dico is cavalierB or dico is cavalierN :
                if check_knight_move(coo, king_coo, enemy_color) :
                    return True 
            elif dico is fouB or dico is fouN :
                if check_bishop_move(coo, king_coo, enemy_color) :
                    return True 
            elif dico is tourB or dico is tourN :
                if check_tower_move(coo, king_coo, enemy_color) :
                    return True
            elif dico is dameB or dico is dameN :
                if check_queen_move(coo, king_coo, enemy_color) :
                    return True

    return False 

def is_square_attacked(square_coo:tuple, color:str) :
    #vérification si une case de coordonée (x, y) est attaqué par une pièce ennemie
    if color == "white" :
         enemy_piece = [pionN, cavalierN, fouN, tourN, dameN, roiN]
         enemy_color = "black"
    else :
        enemy_piece = [pionB, cavalierB, fouB, tourB, dameB]
        enemy_color = "white"
    #on cherche si une piece ennemie peut venir sur la case == elle attaque la case 
    for dico in enemy_piece :
        for key, values in list(dico.items()) :
            if dico is pionB or dico is pionN :
                if check_pon_move(values, square_coo, color) :
                    return True
            elif dico is cavalierB or dico is cavalierN :
                if check_king_move(values, square_coo, color) :
                    return True
            elif dico is fouB or dico is fouN :
                if check_bishop_move(values, square_coo, color) :
                    return True
            elif dico is tourB or dico is tourN :
                if check_tower_move(values, square_coo, color) :
                    return True
            elif dico is dameB or dico is dameN :
                if check_queen_move(values, square_coo, color) :
                    return True
            elif dico is roiB or dico is roiN :
                if check_king_move(values, square_coo, color) :
                    return True
    return False 
            
def is_opponent_king_near(new_king_coo:tuple, color:str) :
    #vérifier si les deux rois sont l'un a coté de l'autre == illégale
    if color == "white" :
        opponent_king_coo = roiN[1]
    else :
        opponent_king_coo = roiB[1]
    
    distance_x, distance_y = abs(new_king_coo[0] - opponent_king_coo[0]), abs(new_king_coo[1] - opponent_king_coo[1])
    if distance_x <= 65 and distance_y <= 65 and opponent_king_coo == new_king_coo :
        return True
    return False 

def all_board_square() :
    #parcour toutes les cases du plateau 
    squares = []
    for x in range(45, 501, 65) : 
        for y in range(45, 501, 65) :
            squares.append((x, y))
    return squares

def is_checkmate(color:str) :
    #vérifier si il y a echec et mat
    piece_actual_coo = None
    removed_piece = None
    #si roi pas en echec, y a pas echec et mat donc return False 
    if not is_check(color) :
        return False 
    #vérifier si un coup peut sauver le roi de l'echec
    if color == "white" :
        for dico in white:
            for key, values in list(dico.items()):
                for squares in all_board_square():
                    if key not in list(dico.keys()):
                        continue
                    removed_piece = None
                    piece_actual_coo = dico[key]
                    if dico is pionB and not check_pon_move(piece_actual_coo, squares, color):
                        continue
                    if dico is cavalierB and not check_knight_move(piece_actual_coo, squares, color):
                        continue
                    if dico is fouB and not check_bishop_move(piece_actual_coo, squares, color):
                        continue
                    if dico is tourB and not check_tower_move(piece_actual_coo, squares, color):
                        continue
                    if dico is dameB and not check_queen_move(piece_actual_coo, squares, color):
                        continue
                    if dico is roiB and not check_king_move(piece_actual_coo, squares, color):
                        continue
                    if check_case(squares) == False:
                        for d in pieces:
                            for k, v in list(d.items()):
                                if v == squares:
                                    removed_piece = (d, k, v)
                                del d[k]
                    if key not in dico.keys():
                        if removed_piece:
                            removed_piece[0][removed_piece[1]] = removed_piece[2]
                            continue
                        dico[key] = squares
                        if not is_check(color):
                            dico[key] = piece_actual_coo
                            if removed_piece:
                                removed_piece[0][removed_piece[1]] = removed_piece[2]
                            return False
                        dico[key] = piece_actual_coo
                        if removed_piece:
                            removed_piece[0][removed_piece[1]] = removed_piece[2]
                    
        return True
    else:
        for dico in black:
            for key, values in list(dico.items()):
                for squares in all_board_square():
                    if key not in list(dico.keys()):
                        continue
                    removed_piece = None
                    piece_actual_coo = dico[key]
                    if dico is pionN and not check_pon_move(piece_actual_coo, squares, color):
                        continue
                    if dico is cavalierN and not check_knight_move(piece_actual_coo, squares, color):
                        continue
                    if dico is fouN and not check_bishop_move(piece_actual_coo, squares, color):
                        continue
                    if dico is tourN and not check_tower_move(piece_actual_coo, squares, color):
                        continue
                    if dico is dameN and not check_queen_move(piece_actual_coo, squares, color):
                        continue
                    if dico is roiN and not check_king_move(piece_actual_coo, squares, color):
                        continue
                    if check_case(squares) == False:
                        for d in pieces:
                            for k, v in list(d.items()):
                                if v == squares:
                                    removed_piece = (d, k, v)
                                    del d[k]
                        if key not in dico.keys():
                            if removed_piece:
                                removed_piece[0][removed_piece[1]] = removed_piece[2]
                            continue
                        dico[key] = squares
                    if not is_check(color):
                        dico[key] = piece_actual_coo
                        if removed_piece:
                            removed_piece[0][removed_piece[1]] = removed_piece[2]
                        return False
                    dico[key] = piece_actual_coo
                    if removed_piece:
                        removed_piece[0][removed_piece[1]] = removed_piece[2]
        print("il y a mat")
        return True 

def is_path(color:str) :
    #vérfier si il path
    square = all_board_square()

    #vérif si le joueur a un coup légal et qu'il n'est pas en echec
    if is_check(color) :
        return False
    if color == "white" :
        for dico in white :
            for key, values in dico.items() :
                for sq in square :
                    if dico is pionB :
                        if check_pon_move(dico[key], sq, color) :
                            return False 
                    elif dico is cavalierB :
                        if check_king_move(dico[key], sq, color) :
                            return False 
                    elif dico is fouB :
                        if check_bishop_move(dico[key], sq, color) :
                            return False 
                    elif dico is tourB :
                        if check_tower_move :
                            if check_tower_move(dico[key], sq, color) :
                                return False 
                    elif dico is dameB :
                        if check_queen_move(dico[key], sq, color) :
                            return False 
                    elif dico is roiB :
                        if check_king_move(dico[key], sq, color) :
                            return False 
    if color == "black" :
        for dico in black :
            for key, values in dico.items() :
                for sq in square :
                    if dico is pionN :
                        if check_pon_move(dico[key], sq, color) :
                            return False 
                    elif dico is cavalierN :
                        if check_king_move(dico[key], sq, color) :
                            return False 
                    elif dico is fouN :
                        if check_bishop_move(dico[key], sq, color) :
                            return False 
                    elif dico is tourN :
                        if check_tower_move :
                            if check_tower_move(dico[key], sq, color) :
                                return False 
                    elif dico is dameN :
                        if check_queen_move(dico[key], sq, color) :
                            return False 
                    elif dico is roiN :
                        if check_king_move(dico[key], sq, color) :
                            return False
    return True
                
def is_not_enough_material() :
    #vérifier si les joueurs ont assez de matériels pour arriver a un echec et mat
    wpon_number = len(pionB)
    wknight_number = len(cavalierB)
    wbishop_number = len(fouB)
    wtower_number = len(tourB)
    wqueen_number = len(dameB)

    bpon_number = len(pionN)
    bknight_number = len(cavalierN)
    bbishop_number = len(fouN)
    btower_number = len(tourN)
    bqueen_number = len(dameN)

    #cas roi seul vs roi seul
    if wpon_number + wknight_number + wbishop_number + wtower_number + wqueen_number == 0 and bpon_number + bknight_number + bbishop_number + btower_number + bqueen_number == 0 :
        return True
            
    #cas roi seul vs roi + fou ou roi + cavalier
    if wpon_number + wtower_number + wqueen_number == 0 and bpon_number + btower_number + bqueen_number == 0 :
        if (wknight_number + wbishop_number <= 1 and bknight_number + bbishop_number == 0 ) or (wknight_number + wbishop_number == 0 and bknight_number + bbishop_number <= 1 ) :
            return True
    
    #cas roi + fou vs roi + fou avec des fous de mêmes couleurs 
    if wpon_number + wknight_number + wtower_number + wqueen_number == 0 and bpon_number + bknight_number + btower_number + bqueen_number == 0 and wbishop_number == 1 and bbishop_number == 1 :
        white_bishop_coo = list(fouB.values())[0]
        black_bishop_coo = list(fouN.values())[0]
        # x // 65 = numéro de la colone entre 0-7 et y // 65 = numéro ligne entre 0-7
        #si x // 65 + y // 65 est pair, alors case blanche, sinon case noir 
        #(x//65, y//65)%2 donne 1 si case noire, 0 si case blanche
        white_color = ((white_bishop_coo[0] // 65) + (white_bishop_coo[1] // 65)) % 2 
        black_color = ((black_bishop_coo[0] // 65) + (black_bishop_coo[1] // 65)) % 2

        if white_color == black_color :
            return True
    return False 

def is_fifty_move_rule():
    #vérifie si il y a eu +50 coups joué depuis denière pris ou dernier mouvement de pion == nul 
    global fifty_move_counter
    if fifty_move_counter >= 100 :
        return  True
    return False

def get_position_signature() :
    #empreinte de la position
    global curent_turn
    global en_passant_square

    piece_str = ""
    for dico in pieces :
        for key, values in sorted(dico.items()) :
            piece_str += f"{id(dico)}{key}:{values};"
    turn = curent_turn
    roque = f"{roiB_has_moved}{roiN_has_moved}{tourB1_has_moved}{tourB2_has_moved}{tourN1_has_moved}{tourN2_has_moved}"
    en_passant = str(en_passant_square)
    return f"{piece_str}|{turn}|{roque}|{en_passant}"

def is_threefold_position() :
    global position_history
    if not position_history :
        return False 
    curent = position_history[-1]
    return position_history.count(curent) >= 3 

def is_draw() :
    if is_path("black") :
        return "black_path"
    elif is_path("white") :
        return "white_path"
    elif is_not_enough_material() :
        return "material" 
    elif is_fifty_move_rule() :
        return "fifty"
    elif is_threefold_position() :
        return "three"
    else :
        return False 
    
def reset_game():
    #reccomencer une partie

    #on réinitialise toutes les variables et coordonées de pièces
    global pionB, tourB, cavalierB, fouB, dameB, roiB
    global pionN, tourN, cavalierN, fouN, dameN, roiN
    global roiB_has_moved, roiN_has_moved, tourB1_has_moved, tourB2_has_moved, tourN1_has_moved, tourN2_has_moved
    global en_passant_square, curent_turn, Playing
    global pieces, white, black
    global WHITE_TIME_LEFT, BLACK_TIME_LEFT, used_time_to_play
    global number_of_moves
    global first_player_name, second_player_name
    global chosen_time

    WHITE_TIME_LEFT = chosen_time
    BLACK_TIME_LEFT = chosen_time
    used_time_to_play = pg.time.get_ticks()

    pionB = {1: (45, 435), 2: (110, 435), 3: (175, 435), 4: (240, 435), 5: (305, 435), 6: (370, 435), 7: (435, 435), 8: (500, 435)}
    tourB = {1: (45, 500), 2: (500, 500)}
    cavalierB = {1: (110, 500), 2: (435, 500)}
    fouB = {1: (175, 500), 2: (370, 500)}
    dameB = {1: (240, 500)}
    roiB = {1: (305, 500)}

    pionN = {1: (45, 110), 2: (110, 110), 3: (175, 110), 4: (240, 110), 5: (305, 110), 6: (370, 110), 7: (435, 110), 8: (500, 110)}
    tourN = {1: (45, 45), 2: (500, 45)}
    cavalierN = {1: (110, 45), 2: (435, 45)}
    fouN = {1: (175, 45), 2: (370, 45)}
    dameN = {1: (240, 45)}
    roiN = {1: (305, 45)}

    pieces = [pionB, tourB, cavalierB, fouB, dameB, roiB, pionN, tourN, cavalierN, fouN, dameN, roiN]
    white = [pionB, cavalierB, fouB, tourB, dameB, roiB]
    black = [pionN, cavalierN, fouN, tourN, dameN, roiN]

    number_of_moves = 0

    roiB_has_moved = False
    roiN_has_moved = False
    tourB1_has_moved = False
    tourB2_has_moved = False
    tourN1_has_moved = False
    tourN2_has_moved = False
    en_passant_square = None
    curent_turn = "white"
    Playing = True

    # Echanger les couleurs des jouers 
    first_player_name, second_player_name = second_player_name, first_player_name

# fonctions déplacement des pièces -------------------------------------------------

def is_on_board(coordonee:tuple) :
    x = coordonee[0]
    y = coordonee[1]
    return 45 <= x <= 500 and 45 <= y <= 500

def check_pon_move(actual_pon_coo:tuple, new_pon_coo:tuple, color:str) :
    #vérifier si quand le joueur déplace le pion il fait un coup légale
    white = [pionB, cavalierB, fouB, tourB, dameB, roiB]
    black = [pionN, cavalierN, fouN, tourN, dameN, roiN]
    global en_passant_square

    #vérification que le joueur a bien bougé la pièce
    if actual_pon_coo == new_pon_coo:
        return False
    #vérification de la couleur de la pièce de la case d'arrivé, même couleur = coup illégal
    if color == "white" :
        for dico in white :
            for key, values in dico.items() :
                if values == new_pon_coo :
                    return False 
    else :
        for dico in black :
            for key, values in dico.items() :
                if values == new_pon_coo :
                    return False
    #vérif si le coup est la prise "en passant"
    if new_pon_coo == en_passant_square :
        return True
    #si pièce devant et que joueur veut aller devant, alors c'est pas possible
    if color == "white" :
        if check_case((actual_pon_coo[0], actual_pon_coo[1] - 65)) == False and new_pon_coo == (actual_pon_coo[0], actual_pon_coo[1] - 65) :
            return False
    else :
        if check_case((actual_pon_coo[0], actual_pon_coo[1] + 65)) == False and new_pon_coo == (actual_pon_coo[0], actual_pon_coo[1] + 65) :
            return False 
    #définition des coups légaux vers l'avant en fonction de la couleur, et gestion du double pas initial
    if color == "white" :
        case_top_left = (actual_pon_coo[0] - 65, actual_pon_coo[1] - 65)
        case_top_right = (actual_pon_coo[0] + 65, actual_pon_coo[1] - 65)
        check_top_left = check_case(case_top_left)
        check_top_right = check_case(case_top_right)
        if actual_pon_coo[1] == 435 and check_case((actual_pon_coo[0], actual_pon_coo[1] - 130)) == True :
            legal_move = [(actual_pon_coo[0], actual_pon_coo[1] - 65), (actual_pon_coo[0], actual_pon_coo[1] - 130)]
        else :
            legal_move = [(actual_pon_coo[0], actual_pon_coo[1] - 65)]
    else :
        case_top_left = (actual_pon_coo[0] + 65, actual_pon_coo[1] + 65)
        case_top_right = (actual_pon_coo[0] - 65, actual_pon_coo[1] + 65)
        check_top_left = check_case(case_top_left)
        check_top_right = check_case(case_top_right)
        if actual_pon_coo[1] == 110 and check_case((actual_pon_coo[0], actual_pon_coo[1] + 130)) == True:
            legal_move = [(actual_pon_coo[0], actual_pon_coo[1] + 65), (actual_pon_coo[0], actual_pon_coo[1] + 130)]
        else :
            legal_move = [(actual_pon_coo[0], actual_pon_coo[1] + 65)]

    color_piece_top_left = None
    color_piece_top_right = None
    if check_top_left == False : #si il y a une pièce sur la case en haut à gauche, on cherche sa couleur
        for dico in pieces :
            for keys, values in dico.items() :
                if values == case_top_left :
                    piece = dico
                    if dico == pionB or dico == tourB or dico == fouB or dico == cavalierB or dico == dameB or dico == roiB :
                        color_piece_top_left = "White" 
                    else :
                        color_piece_top_left = "Black"


    if check_top_right == False : #si il y a une pièce sur la case en haut à droite, on cherche sa couleur
        for dico in pieces :
            for keys, values in dico.items() :
                if values == case_top_right :
                    piece = dico
                    if dico == pionB or dico == tourB or dico == fouB or dico == cavalierB or dico == dameB or dico == roiB :
                        color_piece_top_right = "White"
                    else :
                        color_piece_top_right = "Black"
    #si pièce séléctionné par joueur n'est pas même couleur que pièce en haut a gauche alors ajouter action d'aller en haut à liste des mouves légaux
    if color != color_piece_top_left and color_piece_top_left != None:  
        legal_move.append(case_top_left) 
    #pareil mais a droite
    if color != color_piece_top_right and color_piece_top_right != None: #pareil
        legal_move.append(case_top_right)
    
    if new_pon_coo in legal_move and is_on_board(new_pon_coo) == True :
        return True
    else :
        return False

def ask_promotion_choice(color: str):
    # Affiche les 4 pièces et attend le clic du joueur
    font = pg.font.SysFont(None, 36)
    if color == "white":
        y = 45  # tout en haut
        images = [dameBlancImage, tourBlancImage, fouBlancImage, cavalierBlancImage]
    else:
        y = 500  # tout en bas
        images = [dameNoirImage, tourNoirImage, fouNoirImage, cavalierNoirImage]
    x_start = 120
    rects = []
    for i, img in enumerate(images):
        rect = pg.Rect(x_start + i*90, y, 65, 65)
        rects.append(rect)
        screen.blit(img, (rect.x, rect.y))
        pg.draw.rect(screen, (0, 255, 0), rect, 2)
    txt = font.render("Choisissez la pièce de promotion", True, (0,0,0))
    screen.blit(txt, (100, y-40 if color=="white" else y+70))
    pg.display.flip()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(rects):
                    if rect.collidepoint(event.pos):
                        return ["dame", "tour", "fou", "cavalier"][i]
    
def check_tower_move(actual_tower_coo:tuple, new_tower_coo:tuple, color:str) :
    white = [pionB, cavalierB, fouB, tourB, dameB, roiB]
    black = [pionN, cavalierN, fouN, tourN, dameN, roiN]
    x_actual, y_actual = actual_tower_coo
    x_new, y_new = new_tower_coo
    
    #vérification que le joueur a bien bougé la pièce
    if actual_tower_coo == new_tower_coo:
        return False
    # Vérifie si la case d'arrivée contient une pièce alliée
    if check_case(new_tower_coo) == False:
        if color == "white":
            for dico in white:
                for key, values in dico.items():
                    if values == new_tower_coo:
                        return False
        else:
            for dico in black:
                for key, values in dico.items():
                    if values == new_tower_coo:
                        return False
    # Mouvement vertical
    if x_actual == x_new:
        step = 65 if y_new > y_actual else -65
        for y in range(y_actual + step, y_new, step):
            if check_case((x_actual, y)) == False:
                return False
        return is_on_board(new_tower_coo)
    # Mouvement horizontal
    if y_actual == y_new:
        step = 65 if x_new > x_actual else -65
        for x in range(x_actual + step, x_new, step):
            if check_case((x, y_actual)) == False:
                return False
        return is_on_board(new_tower_coo)

    return False
                    
def check_knight_move(actual_knight_coo:tuple, new_knight_coo:tuple, color:str) :
    #vérifier si quand le joueur déplace un cavalier il fait un coup légal 
    white = [pionB, cavalierB, fouB, tourB, dameB, roiB]
    black = [pionN, tourN, cavalierN, fouN, dameN, roiN]
    x_actual, y_actual = actual_knight_coo[0], actual_knight_coo[1]
    x_new, y_new = new_knight_coo[0], new_knight_coo[1]
    legal_move = [(x_actual-65, y_actual-130), (x_actual+65, y_actual-130), (x_actual+130, y_actual-65), (x_actual+130, y_actual+65), (x_actual+65, y_actual+130), (x_actual-65, y_actual+130), (x_actual-130, y_actual+65), (x_actual-130, y_actual-65)]

    #vérification que le joueur a bougé son cavalier en L
    if new_knight_coo not in legal_move :
        return False 
    #vérif si la case d'arrivé est bien sur le plateau
    if not is_on_board(new_knight_coo) :
        return False
    #vérif si sur case d'arriver il y a déja une pièce de la même couleur = coup illégal
    if not check_case(new_knight_coo) :
        if color == "white" :
            for dico in white :
                for key, values in dico.items() :
                    if values == new_knight_coo :
                        return False 
        else :
            for dico in black :
                for key, values in dico.items() :
                    if values == new_knight_coo :
                        return False 
    return True
    
    
def check_bishop_move(actual_bishop_coo:tuple, new_bishop_coo:tuple, color:str) :
    #vérifier si quand le joueur déplace un fou il fait un coup légale
    white = [pionB, tourB, cavalierB, fouB, dameB, roiB]
    black = [pionN, tourN, cavalierN, fouN, dameN, roiN]
    x_actual, y_actual = actual_bishop_coo[0], actual_bishop_coo[1]
    x_new, y_new = new_bishop_coo[0], new_bishop_coo[1]
    case = actual_bishop_coo

    #vérification que le joueur a bien bougé la pièce
    if actual_bishop_coo == new_bishop_coo :
        return False
    #vérif que la case d'arrivé est bien sur le plateau 
    if is_on_board(new_bishop_coo) == False :
        return False
    #vérif si sur case d'arriver il y a déja une pièce de la même couleur = coup illégal
    new_case = check_case(new_bishop_coo) 
    if new_case == False :
        if color == "white" :
            for dico in white :
                for key, values in dico.items() :
                    if values == new_bishop_coo :
                        return False 
        else :
            for dico in black :
                for key, values in dico.items() :
                    if values == new_bishop_coo :
                        return False 
    #vérifie que le mouvement est diagonale
    if abs(x_new - x_actual) != abs(y_new - y_actual):
        return False
    if y_actual > y_new and x_actual < x_new : #diagonale vers le haut vers la droite
        while case != (new_bishop_coo[0] - 65, new_bishop_coo[1] + 65)  : 
            case = (case[0] + 65, case[1] - 65)
            if check_case(case) == False :
                return False 
        return True
    elif y_actual < y_new and x_actual < x_new : #diagonale vers le bas vers la droite
        while case != (new_bishop_coo[0] - 65, new_bishop_coo[1] - 65) :
            case = (case[0] + 65, case[1] + 65)
            if check_case(case) == False :
                return False 
        return True
    elif y_actual > y_new and x_actual > x_new : #diagonale vers haut vers la gauche 
        while case != (new_bishop_coo[0] + 65, new_bishop_coo[1] + 65) :
            case = (case[0] - 65, case[1] - 65)
            if check_case(case) == False :
                return False 
        return True
    elif y_actual < y_new and x_actual > x_new : #diagonale vers le bas vers la gauche 
        while case != (new_bishop_coo[0] + 65, new_bishop_coo[1] - 65) :
            case = (case[0] - 65, case[1] + 65)
            if check_case(case) == False :
                return False 
        return True
    return False 

def check_queen_move(actual_queen_coo:tuple, new_queen_coo:tuple, color:str) :
    #vérifier si quand le joueur déplace une dame il fait un coup légale
    #la dame peut se déplacer comme fou e tour donc on utilise les fonctions précédente
    if check_bishop_move(actual_queen_coo, new_queen_coo, color) == True or check_tower_move(actual_queen_coo, new_queen_coo, color) == True :
        return True    

def check_king_move(actual_king_coo:tuple, new_king_coo:tuple, color:str) :
    #vérif si quand le joueur déplace son roi il fait un coup légale
    white = [pionB, cavalierB, fouB, tourB, dameB, roiB]
    black = [pionN, cavalierN, fouN, tourN, dameN, roiN]
    x_actual, y_actual = actual_king_coo[0], actual_king_coo[1]
    x_new, y_new = new_king_coo[0], new_king_coo[1]

    #vérif que le joueur a bien bougé la pièce
    if actual_king_coo == new_king_coo :
        return False
    #vérif que le joueur a bougé le roi que d'une case
    if (abs(x_new - x_actual) > 65) or (abs(y_new - y_actual) > 65) or (x_new == x_actual and y_new == y_actual) :        
        return False
    #vérif si sur case d'arriver il y a déja une pièce de la même couleur = coup illégal 
    if check_case(new_king_coo) == False :
        if color == "white" :
            for dico in white :
                for key, values in dico.items() :
                    if values == new_king_coo :
                        return False 
        elif color == "black" :
            for dico in black :
                for key, values in dico.items() :
                    if values == new_king_coo :
                        return False 
    #vérif que le roi ne bouge pas a coté de l'autre roi
    if color == "white" :
        opponent_king_coo = roiN[1]
    else :
        opponent_king_coo = roiB[1]
    dx = abs(new_king_coo[0] - opponent_king_coo[0])
    dy = abs(new_king_coo[1] - opponent_king_coo[1])
    if dx <= 65 and dy <= 65 and new_king_coo != opponent_king_coo:
        return False
    #vérif que la case sur laquelle le joueur a bougé son roi n'est pas en echec
    if color == "white" :
        roiB[1] = new_king_coo
    elif color == "black" :
        roiN[1] = new_king_coo
    if is_check(color) :
        if color == "white" :
            roiB[1] = actual_king_coo
            return False 
        elif color == "black" :
            roiN[1] = actual_king_coo
            return False 
    
     
    return True 

def can_castle(actual_king_coo:tuple, actual_tower_coo:tuple, color:str) :
    #vérifier si le joueur peut roquer
    #vérif que roi et tour n'ont jamais bougés
    if color == "white" :
        if roiB_has_moved :
            return False
        for idx in range(1, len(tourB)) :
            if tourB[idx] == actual_tower_coo and idx == 1 :
                if tourB1_has_moved :
                    return False 
            elif tourB[idx] == actual_tower_coo and idx == 2 :
                if tourB2_has_moved :
                    return False 
    else :
        if roiN_has_moved :
            return False 
        for idx in range(1, len(tourN)) :
            if tourN[idx] == actual_tower_coo and idx == 1 :
                if tourN1_has_moved :
                    return False 
            elif tourN[idx] == actual_tower_coo and idx == 2 :
                if tourN2_has_moved :
                    return False
    #vérif qu'il n'y a pas de pièce entre roi et tour
    if color == "white" :
        if actual_tower_coo == tourB[1] :
            for idx in range(1, 4):
                if check_case((actual_king_coo[0] - idx*65, actual_king_coo[1])) == False :
                    return False 
        elif actual_king_coo == tourB[2] :
            for idc in range(1, 3) :
                if check_case((actual_king_coo[0] + idx*65, actual_king_coo)) == False :
                    return False 
    else :
        if actual_tower_coo == tourN[1] :
            for idx in range(1, 4) :
                if check_case((actual_king_coo[0] - idx*65, actual_king_coo[1])) == False :
                    return False 
        elif actual_king_coo == tourN[2] :
            for idc in range(1, 3) :
                if check_case((actual_king_coo[0] + idx*65, actual_king_coo)) == False :
                    return False 
    #vérif que le roi n'est pas en echec
    if is_check(color) :
        return False 
    #vérif que les cases entre roi et tour ne sont pas en echec
    if color == "white" :
        if actual_tower_coo == tourB[1] :
            for idx in range(1, 4) :
                roiB[1] = (actual_king_coo[0] - idx*65, actual_king_coo[1])
                if is_check("white") :
                    roiB[1] = actual_king_coo
                    return False 
            roiB[1] = actual_king_coo
        elif actual_tower_coo == tourB[2] :
            for idx in range(1, 3) :
                roiB[1] = (actual_king_coo[0] + idx*65, actual_king_coo[1])
                if is_check("white") :
                    roiB[1] = actual_king_coo
                    return False
            roiB[1] = actual_king_coo 
    else :
        if actual_tower_coo == tourN[1] :
            for idx in range(1, 4) :
                roiN[1] = (actual_king_coo[0] - idx*65, actual_king_coo[1])
                if is_check("black") :
                    roiN[1] = actual_king_coo
                    return False 
            roiN[1] = actual_king_coo
        elif actual_tower_coo == tourN[2] :
            for idx in range(1, 3) :
                roiN[1] = (actual_king_coo[0] + idx*65, actual_king_coo[1])
                if is_check("black") :
                    roiN[1] = actual_king_coo
                    return False
            roiN[1] = actual_king_coo

    return True

def castle(king_dict:dict, tower_dict:dict, tower_key:int) :
    #effectuer le roque
    #déterminer sens du roque
    castle = None
    if tower_key == 2 :
        castle = "queen_side"
    elif tower_key == 1 :
        castle = "king_side"   
    #déplacer roi de 2 cases vers la tour, et déplacer la tour de l'autre coté du roi
    if castle == "king_side" :
        king_dict[1] = (king_dict[1][0] - 130, king_dict[1][1])
        tower_dict[tower_key] = (tower_dict[tower_key][0] + 195, tower_dict[tower_key][1])
    elif castle == "queen_side" :
        king_dict[1] = (king_dict[1][0] + 130, king_dict[1][1])
        tower_dict[tower_key] = (tower_dict[tower_key][0] - 130, tower_dict[tower_key][1])
    #mise a jour des variable de mouvement des rois
    #(On met a jour que celle des rois car si celle du roi vaut True, alors roquer n'est plus possible)
    global roiB_has_moved, roiN_has_moved
    if king_dict == roiB :
        roiB_has_moved = True
    elif king_dict == roiN :
        roiN_has_moved = True

def is_move_legal(selected_piece:dict, new_piece_coo:tuple) :
    #vérifier si le coup qua jouer le joueur est légal 
    global fifty_move_counter
    white = [pionB, cavalierB, fouB, tourB, dameB, roiB]
    black = [pionN, cavalierN, fouN, tourN, dameN, roiN]
    dico, key = selected_piece[0], selected_piece[1]
    piece = dico
    actual_piece_coo = dico[key]
    if dico in white :
        color = "white"
    else :
        color = "black"
    # PION
    global en_passant_square
    if piece is pionB or piece is pionN :
        if check_pon_move(actual_piece_coo, new_piece_coo, color) :
            if new_piece_coo == en_passant_square :
                if piece is pionB :
                    remove_pieces((new_piece_coo[0], new_piece_coo[1] + 65))
                else :
                    remove_pieces((new_piece_coo[0], new_piece_coo[1] - 65))
            elif check_case(new_piece_coo) == False:
                remove_pieces(new_piece_coo)
            piece[key] = new_piece_coo
            if is_check(color):
                piece[key] = actual_piece_coo
                return False
            if piece is pionB and new_piece_coo[1] == 45 :
                choice = ask_promotion_choice("white") 
                del pionB[key]
                if choice == "dame" :
                    dameB[len(dameB) + 1] = new_piece_coo
                elif choice == "tour" :
                    tourB[len(tourB) + 1] = new_piece_coo
                elif choice == "cavalier" :
                    cavalierB[len(cavalierB) + 1] = new_piece_coo
                elif choice == "fou" :
                    fouB[len(fouB) + 1] = new_piece_coo
            elif piece is pionN and new_piece_coo[1] == 500 :
                del pionN[key]
                if choice == "dame" :
                    dameN[len(dameN) + 1] = new_piece_coo
                elif choice == "tour" :
                    tourN[len(tourN) + 1] = new_piece_coo
                elif choice == "cavalier" :
                    cavalierN[len(cavalierN) + 1] = new_piece_coo
                elif choice == "fou" :
                    fouN[len(fouN) + 1] = new_piece_coo 


            if piece is pionB and (actual_piece_coo[0], actual_piece_coo[1] - 130) == new_piece_coo : 
                en_passant_square = (actual_piece_coo[0], actual_piece_coo[1] - 65)
            elif piece is pionN and (actual_piece_coo[0], actual_piece_coo[1] + 130) == new_piece_coo :
                en_passant_square = (actual_piece_coo[0], actual_piece_coo[1] + 65)
            else :
                en_passant_square = None
            fifty_move_counter = 0
            return True
    # CAVALIER
    if piece is cavalierB or piece is cavalierN :
        if check_knight_move(actual_piece_coo, new_piece_coo, color) :
            if check_case(new_piece_coo) :
                fifty_move_counter += 1
            elif check_case(new_piece_coo) == False:
                remove_pieces(new_piece_coo)
                fifty_move_counter = 0
            piece[key] = new_piece_coo
            if is_check(color):
                piece[key] = actual_piece_coo
                return False
            en_passant_square = None
            return True
    # FOU
    if piece is fouB or piece is fouN :
        if check_bishop_move(actual_piece_coo, new_piece_coo, color) :
            if check_case(new_piece_coo) :
                fifty_move_counter += 1
            elif check_case(new_piece_coo) == False:
                remove_pieces(new_piece_coo)
                fifty_move_counter = 0
            piece[key] = new_piece_coo
            if is_check(color):
                piece[key] = actual_piece_coo
                return False
            en_passant_square = None
            return True
    # TOUR
    if piece is tourB or piece is tourN :
        if check_tower_move(actual_piece_coo, new_piece_coo, color) :
            if check_case(new_piece_coo) :
                fifty_move_counter += 1
            elif check_case(new_piece_coo) == False:
                remove_pieces(new_piece_coo)
                fifty_move_counter = 0
            piece[key] = new_piece_coo
            if is_check(color):
                piece[key] = actual_piece_coo
                return False
            global tourB1_has_moved, tourB2_has_moved, tourN1_has_moved, tourN2_has_moved
            if piece is tourB :
                if key == 1 :
                    tourB1_has_moved = True
                elif key == 2 :
                    tourB2_has_moved = True
            else :
                if key == 1 :
                    tourN1_has_moved = True
                elif key == 2 :
                    tourN2_has_moved = True
            en_passant_square = None
            return True
    # DAME
    if piece is dameB or piece is dameN :
        if check_queen_move(actual_piece_coo, new_piece_coo, color) :
            if check_case(new_piece_coo) :
                fifty_move_counter += 1
            elif check_case(new_piece_coo) == False:
                remove_pieces(new_piece_coo)
                fifty_move_counter = 0
            piece[key] = new_piece_coo
            if is_check(color):
                piece[key] = actual_piece_coo
                return False
            en_passant_square = None
            return True
    # ROI
    if piece is roiB or piece is roiN:
        # Détermine la couleur
        if piece is roiB:
            king_color = "white"
            opponent_king_coo = roiN[1]
            tour_dict = tourB
            roi_dict = roiB
            enemy_list = black
        else:
            king_color = "black"
            opponent_king_coo = roiB[1]
            tour_dict = tourN
            roi_dict = roiN
            enemy_list = white

        # Vérifie le roque
        if abs(new_piece_coo[0] - actual_piece_coo[0]) == 130 and new_piece_coo[1] == actual_piece_coo[1]:
            if new_piece_coo[0] > actual_piece_coo[0]:
                if 2 in tour_dict and can_castle(actual_piece_coo, tour_dict[2], king_color):
                    castle(roi_dict, tour_dict, 2)
                    return True
            elif new_piece_coo[0] < actual_piece_coo[0]:
                if 1 in tour_dict and can_castle(actual_piece_coo, tour_dict[1], king_color):
                    castle(roi_dict, tour_dict, 1)
                    return True
        # Déplacement normal du roi
        if check_king_move(actual_piece_coo, new_piece_coo, king_color):
            # Interdit d'être adjacent à l'autre roi
            dx = abs(new_piece_coo[0] - opponent_king_coo[0])
            dy = abs(new_piece_coo[1] - opponent_king_coo[1])
            if dx <= 65 and dy <= 65 and (dx != 0 or dy != 0):
                return False

            # Capture d'une pièce ennemie si présente
            captured_piece = None
            for dico in enemy_list :
                for k, v in dico.items() :
                    if v == new_piece_coo :
                        captured_piece = (dico, k, v)
                        break
                if captured_piece :
                    break
            if captured_piece :
                del captured_piece[0][captured_piece[1]]
                fifty_move_counter = 0
            else :
                fifty_move_counter += 1
            
            roi_dict[1] = new_piece_coo
                
            # Vérifie si le roi se met en échec
            if is_check(king_color):
                roi_dict[1] = actual_piece_coo
                # Restaure la pièce capturée si besoin
                if captured_piece:
                    captured_piece[0][captured_piece[1]] = captured_piece[2]
                return False

            # Mise à jour des variables de mouvement
            global roiB_has_moved, roiN_has_moved
            if piece is roiB:
                roiB_has_moved = True
            else:
                roiN_has_moved = True
            en_passant_square = None
            return True

    return False
        

# Boucle de jeu -----------------------------------------------------------------

selected_piece = None
ask_players_name()
WHITE_TIME = chosen_time
BLACK_TIME = chosen_time
WHITE_TIME_LEFT = chosen_time 
BLACK_TIME_LEFT = chosen_time 
used_time_to_play = pg.time.get_ticks()
while True :
    if not Playing :
        pg.time.wait(100)
        continue
    screen.blit(chessboard, (0, 0) )
    print_pieces()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            Playing = False
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if selected_piece is None : #1er clic
                selected_piece = find_selected_piece()
                continue
            if selected_piece is not None : #2ème clic
                if curent_turn == "white" and selected_piece[0] not in white :
                    selected_piece = None
                    continue
                elif curent_turn == "black" and selected_piece[0] not in black :
                    selected_piece = None
                    continue
                case = find_case_where_to_move()
                #vérifier si coup légale 
                if not is_move_legal(selected_piece, case) :
                    selected_piece = None 
                    continue
                
                position_history.append(get_position_signature())
                draw_reason = is_draw()
                if draw_reason :
                    Playing = False 
                    endgame_print(draw_reason)

                if curent_turn == "white" :
                    curent_turn = "black" 
                    number_of_moves += 1
                elif curent_turn == "black" :
                    curent_turn = "white"
                    number_of_moves += 1

                if is_checkmate(curent_turn) :
                    Playing = False 
                    if curent_turn == "white" :
                        endgame_print("black")
                    else :
                        endgame_print("white")

                selected_piece = None
    now = pg.time.get_ticks()
    elapsed = (now - used_time_to_play) // 1000
    if elapsed > 0 :
        if curent_turn == "white" :
            WHITE_TIME_LEFT = max(0, WHITE_TIME_LEFT - elapsed)
        else :
            BLACK_TIME_LEFT = max(0, BLACK_TIME_LEFT - elapsed)
        used_time_to_play = now
    chrono_print()
    if WHITE_TIME_LEFT <= 0:
        if is_not_enough_material():
            Playing = False
            endgame_print("material")
        else:
            Playing = False
            endgame_print("black_on_time")
    elif BLACK_TIME_LEFT <= 0 :
        if is_not_enough_material() :
            Playing = False
            endgame_print("material")
        else:
            Playing = False
            endgame_print("white_on_time")
            
    pg.display.flip()