import pygame
import math

pygame.init()


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
    if nx > 1 or nx < -1 or ny > 1 or ny < -1:
        print("versori non tra -1 e 1!")
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
    nx, ny = normalizza(nx0, ny0)   #normalizzo per sicurezza
    nx = nx0 * math.cos(theta) - ny0 * math.sin(theta)
    ny = nx0 * math.sin(theta) - ny0 * math.cos(theta)
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


screen = pygame.display.set_mode((640,640)) # create the canvas 

delta_time = 0.1     

font = pygame.font.Font(None, size=30)

# initializing the parameter 
x = 0  
y = 30 
nx = 0.5  # versori direzione del moviemnto
ny = 0.5

clock = pygame.time.Clock()  

turn_left = False    
turn_right = False


# main loop of the game
running = True
while running: 

    screen.fill((0,0,0)) # color the background

    pygame.draw.circle(screen, "red", (x,y), 20)
    disegna_versore(screen, x, y, nx, ny)

    target = pygame.Rect(300, 0, 160, 290)


    # fai ruotare se premuto tasto d o a 
    if turn_left: 
        nx, ny = ruota_versore(10, nx, ny) 

    x, y =  spostamento(10 * delta_time, nx, ny, x, y)   #aggiorna la posizione del cerchio

    print(f"nx: {nx}, ny: {ny}")
    text = font.render("Hello!", True, (255,255,0))

    screen.blit(text, (300,100))


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