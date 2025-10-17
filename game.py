import pygame
import math
import random

pygame.init()

def distance(x1, y1, x2, y2):
    '''euclidean distance between (x1,y1) and (x2,y2)'''
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def norm(x, y): 
    '''
    calcola norma di due componenti
    '''
    return math.sqrt(x**2 + y**2)

def normalizza(x, y):
    '''
    normalizza una coppia di componenti per avere norma 1
    '''
    return x/norm(x, y), y/norm(x, y) 

def trova_altra_componente(x, modulo=1):
    '''
    serve per trovare y avendo la x (o viceversa) intese come coordinate di un versore
    '''
    return math.sqrt(modulo - x**2)

def spostamento(s, nx, ny, x, y):
    '''
    prende coordinate in ingresso e restituisce posizione aggiornata in base a uno spostamento di modulo s e versori nx ny

    INPUT
        s: il modulo dello spostamento
        nx e ny: sono i versori x e y
                hanno valore che va da 0 a 1
                e nx^2 + ny^2 = 1
        x e y: posizione iniziale
    OUTPUT:
        x e y : posizione finale        
    '''  
    assert  not (nx > 1 or nx < -1 or ny > 1 or ny < -1)

    norma = norm(nx, ny)
    x += nx*s
    y += ny*s
    return x, y
    
def ruota_versore(theta, nx0, ny0):
    '''
    funzione per ruotare i versori

    prende input versori iniziale nx0 ny0
    li normalizza per sicurezza
    poi li ruota semplicemente aumentando uno e diminuendo l'altro in base a angolo theta con la classica  matrice di rotazione (consideriamo theta positivo rotazione antitoraria)
    li rinormlaizza per sicurezza 
    restituisce i versori aggiornati nx e ny

    INPUT
        theta: angolo in gradi
        nx0, ny0: versori iniziali
    OOUTPUT: 
        nx ny : versori ruotati
    '''
    theta = math.radians(theta)
    nx = nx0 * math.cos(theta) - ny0 * math.sin(theta)
    ny = nx0 * math.sin(theta) + ny0 * math.cos(theta)
    #the norm is 1 entro un errore di calcolo numerico
    error = 1e-5
    assert abs(norm(nx,ny) - 1) < error
    return nx, ny

def disegna_versore(screen, x, y, nx, ny, lunghezza=40, colore=(255,0,0)):
    '''
    disegna freccia che rappresenta il versore'''
    nx, ny = normalizza(nx, ny) # normalizzo per sicurezza

    x_punta = x + nx * lunghezza
    y_punta = y + ny * lunghezza

    #linea della freccia
    pygame.draw.line(screen, colore, (x, y), (x_punta, y_punta), width=2)
    # punta della freccia fatta con due linee
    angolo = math.atan2(ny, nx)
    punta_angolo = math.radians(30)
    punta_lunghezza = 10

    sinistra_x = x_punta - punta_lunghezza * math.cos(angolo - punta_angolo)
    sinistra_y = y_punta - punta_lunghezza * math.sin(angolo - punta_angolo)
    destra_x = x_punta - punta_lunghezza * math.cos(angolo + punta_angolo)
    destra_y = y_punta - punta_lunghezza * math.sin(angolo + punta_angolo)

    pygame.draw.line(screen, colore, (x_punta, y_punta), (sinistra_x, sinistra_y), 2)
    pygame.draw.line(screen, colore, (x_punta, y_punta), (destra_x, destra_y), 2)

def tocca_bordo(screen, x, y, r):
    '''
    controlla se l'oggetto tocca il bordo
    o meglio lo considera come un cerchio centrato in x y e di raggio r
    per un cerchio come in questo gioco va bene, per figure piu complesse le includi in un cerchio - in altri casi potrebbe servire una funzione che usa rettangolo o figure piu complesse
    '''
    return x - r <= 0 or x + r >= screen.get_width() or y - r <= 0 or y + r >= screen.get_height()

def tocca_traccia(screen, player_x, player_y, raggio_player, traccia, raggio_traccia):
    #if distanza tra xy player e xy traccia < raggio_player - raggio traccia
    for point in traccia:
        point_x, point_y = point
        if distance(player_x, player_y, point_x, point_y) <= raggio_player - raggio_traccia:
            return True
    return False

def game_over(screen, x, y, velocita, coordinate_traccia):
    text = font.render("YOU LOSE", True, (255,255,0))
    screen.blit(text, (300,100))
    # DEVE SCOMPARIRE IL CERCHIO
    velocita = 0 # nonsi muove piu
    # lo spostiamo fuori dalle palle
    x = -100
    y = -100
    # scompare anche la traccia
    coordinate_traccia = []
    return x, y, velocita, coordinate_traccia  


screen = pygame.display.set_mode((640,640)) # create the canvas 

delta_time = 0.1     

font = pygame.font.Font(None, size=30)

# initializing the parameters 

# bounding lo uso per non  far partire la palla troppo vicvina al bordo
bounding = screen.get_width()*0.05
# starting position and direction of the ball
x = random.uniform(bounding, screen.get_width() - bounding)
y = random.uniform(bounding, screen.get_height() - bounding)
nx = random.uniform(-1, 1)  # versori direzione del moviemnto
ny = trova_altra_componente(nx)
# aspetto della palla
player_radius = 20
# movimento della palla
velocita = 20
rotazione = 2


raggio_traccia = 3
tempo_traccia_on = 3000 # millisecondi
tempo_traccia_off = 800
intervallo_traccia = tempo_traccia_on    # intervallo è quello che uso per confrontarlo col tempo corrente- partiamo con on cioè la traccia inizia immediatamente quando inizia il gioco

clock = pygame.time.Clock()  

turn_left = False    
turn_right = False

disegna_traccia = True   #per segnalare se dobbiamo disegnare la traccia [parte la traccia dall'inizio del gioco]

coordinate_traccia = []

# main loop of the game
running = True
ultimo_toggle = pygame.time.get_ticks()  #salvo l'ultimo toggle

while running: 
    print(ultimo_toggle)
    screen.fill((0,0,0)) # color the background

    pygame.draw.circle(screen, "red", (x,y), player_radius)
    disegna_versore(screen, x, y, nx, ny)

    target = pygame.Rect(300, 0, 160, 290)

    # fai ruotare se premuto tasto d o a 
    if turn_left: 
        nx, ny = ruota_versore(rotazione, nx, ny) 
    if turn_right: 
        nx, ny = ruota_versore(-rotazione, nx, ny) 

    x, y =  spostamento(velocita * delta_time, nx, ny, x, y)   #aggiorna la posizione del cerchio

    if disegna_traccia:
        coordinate_traccia.append((x - nx * player_radius, y - ny * player_radius))

    for coordinate in coordinate_traccia:     # disegna la traccia
        pygame.draw.circle(screen, "red", coordinate, raggio_traccia)
    

    if tocca_bordo(screen, x, y, player_radius) or tocca_traccia(screen, x, y, player_radius, coordinate_traccia, raggio_traccia):
        x, y, velocita, coordinate_traccia = game_over(screen, x, y, velocita, coordinate_traccia)

    tempo_attuale = pygame.time.get_ticks()
    if tempo_attuale - ultimo_toggle >= intervallo_traccia:
        if disegna_traccia:
            intervallo_traccia = tempo_traccia_off
        else:
            intervallo_traccia = tempo_traccia_on
        disegna_traccia = not disegna_traccia
        ultimo_toggle = tempo_attuale


    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_d: #se premuto tasto "d"
                turn_right = True       
            if event.key == pygame.K_a: # se premuto tasto "a"
                turn_left = True        
        if event.type == pygame.KEYUP:   
            if event.key == pygame.K_d: # se rilasciato tasto "d"
                turn_right = False  
            if event.key == pygame.K_a: # se rilasciato tasto "a"
                turn_left = False   

            


    pygame.display.flip()   # mostra tutto quello che c'è da mostarre

    delta_time = clock.tick(60)   
    delta_time = max(0.001, min(0.1, delta_time))    # come sicurezza ulteriore, mi assicuro di prendere delta time a meno che sia compreso tra un tempo massimo e uno minimo, per non prendere valori di delta time troppo estremi 


pygame.quit()