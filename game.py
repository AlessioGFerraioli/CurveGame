import pygame
import math
import random

pygame.init()



#########################
        #       UTILITY MATH FUNCTIONS
##############################

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


    
class Player():
    '''
    class for the player object, represented by a circle
    '''

    def __init__(self, x, y, radius, nx, ny, velocita, rotazione, turn_right_key=pygame.K_d, turn_left_key=pygame.K_a):
        '''
        x, y : posizione
        radius : raggio del cerchio
        nx, ny : versori direzione movimento
        velocita : velocita del movimento
        rotazione : angolo di rotazione (velocita di rotazione)
        turn_right_key, turn_left_key : tasti usati per girare (default D e A)        
        '''
        # posizione iniziale
        self.x = x
        self.y = y
        # raggio della sfera
        self.radius = radius
        # direzione iniziale (versori)
        self.nx = nx
        self.ny = ny
        # parametri del movimento
        self.velocita = velocita
        self.rotazione = rotazione       
        self.turn_right = False
        self.turn_left = False
        # tasti usati per girare a destra e sinistra
        self.turn_right_key = turn_right_key
        self.turn_left_key = turn_left_key
        # parametri traccia
        self.coordinate_traccia = []

        
    def vanish(self):
        # DEVE SCOMPARIRE IL CERCHIO
        self.velocita = 0 # nonsi muove piu
        # lo spostiamo fuori dalle palle
        self.x = -100
        self.y = -100

    def spostamento(self, delta_time):
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
        assert  not (self.nx > 1 or self.nx < -1 or self.ny > 1 or self.ny < -1)

        s = self.velocita * delta_time
        self.x += self.nx*s
        self.y += self.ny*s
           

    def ruota_versore(self, counter_clockwise=True):
        '''
        funzione per ruotare i versori

        salva versori iniziale nx0 ny0
        li ruota con matrice di rotazione di angolo determinato da self.rotazione (in gradi) 
        la rotazione è antioraria o oraria determinata da counter_clockwise
        controlla che la loro norma sia 1 entro un errore numerico 
        aggiorna i versori self.nx e self.ny
        '''

        theta = math.radians(self.rotazione)
        if not counter_clockwise:
            theta = - theta
        # salvo i versori iniziali
        nx0 = self.nx
        ny0 = self.ny
        
        self.nx = nx0 * math.cos(theta) - ny0 * math.sin(theta)
        self.ny = nx0 * math.sin(theta) + ny0 * math.cos(theta)
        #the norm is 1 entro un errore di calcolo numerico
        error = 1e-5
        assert abs(norm(self.nx,self.ny) - 1) < error
        
    def disegna_versore(self, screen, lunghezza=40, colore=(255,0,0)):
        '''
        disegna freccia che rappresenta il versore'''
        self.nx, self.ny = normalizza(self.nx, self.ny) # normalizzo per sicurezza

        x_punta = self.x + self.nx * lunghezza
        y_punta = self.y + self.ny * lunghezza

        #linea della freccia
        pygame.draw.line(screen, colore, (self.x, self.y), (x_punta, y_punta), width=2)
        # punta della freccia fatta con due linee
        angolo = math.atan2(self.ny, self.nx)
        punta_angolo = math.radians(30)
        punta_lunghezza = 10

        sinistra_x = x_punta - punta_lunghezza * math.cos(angolo - punta_angolo)
        sinistra_y = y_punta - punta_lunghezza * math.sin(angolo - punta_angolo)
        destra_x = x_punta - punta_lunghezza * math.cos(angolo + punta_angolo)
        destra_y = y_punta - punta_lunghezza * math.sin(angolo + punta_angolo)

        pygame.draw.line(screen, colore, (x_punta, y_punta), (sinistra_x, sinistra_y), 2)
        pygame.draw.line(screen, colore, (x_punta, y_punta), (destra_x, destra_y), 2)

    def tocca_bordo(self, screen):
        '''
        controlla se l'oggetto tocca il bordo
        o meglio lo considera come un cerchio centrato in x y e di raggio r
        per un cerchio come in questo gioco va bene, per figure piu complesse le includi in un cerchio - in altri casi potrebbe servire una funzione che usa rettangolo o figure piu complesse
        '''
        return self.x - self.radius <= 0 or self.x + self.radius >= screen.get_width() or self.y - self.radius <= 0 or self.y + self.radius >= screen.get_height()
    

    def tocca_traccia(self,  coordinate_traccia, raggio_traccia):
        #if distanza tra xy player e xy traccia < raggio_player - raggio traccia
        for point in coordinate_traccia:

            point_x, point_y = point
            if distance(self.x, self.y, point_x, point_y) <= self.radius - raggio_traccia:
                return True
        return False


class Game():
    '''
    class for the game 
    '''

    def __init__(self, screen_width=640, screen_height=640, delta_time=0.1):
        # size of the screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bounding = self.screen_width*0.05
        # to control the speed of fps
        self.delta_time = delta_time
        self.clock = pygame.time.Clock()  

        #parametri players (comuni a tutti i players)
        n_players = 1
        # aspetto della palla
        self.player_radius = 20
        # movimento della palla
        self.velocita = 20
        self.rotazione = 2
        # parametri traccia
        self.raggio_traccia = 3
        self.tempo_traccia_on = 3000 # millisecondi
        self.tempo_traccia_off = 800
        self.intervallo_traccia = self.tempo_traccia_on    # intervallo è quello che uso per confrontarlo col tempo corrente- partiamo con on cioè la traccia inizia immediatamente quando inizia il gioco

        self.players = []
        # creo i player
        for i in range(n_players):
            # random starting parameter of each player
            x0 = random.uniform(self.bounding, screen_width - self.bounding)
            y0 = random.uniform(self.bounding, screen_height - self.bounding)
            nx0 = random.uniform(-1, 1)  
            ny0 = trova_altra_componente(nx0)
            self.players.append(Player(x0, y0, self.player_radius, nx0, ny0, self.velocita, self.rotazione))
    
  
    def game_over(self):
        text = self.font.render("YOU LOSE", True, (255,255,0))
        self.screen.blit(text, (300,100))
        # scompare anche la traccia
        self.coordinate_traccia = []
        


    def play(self):
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height)) # create the canvas 

        # inizializzo font
        self.font = pygame.font.Font(None, size=30)

        #parametri all'inizio del gioco        
        self.turn_left = False    
        self.turn_right = False
        self.disegna_traccia = True   #per segnalare se dobbiamo disegnare la traccia [parte la traccia dall'inizio del gioco]

        self.coordinate_traccia = []

        # main loop of the game
        self.running = True
        self.ultimo_toggle = pygame.time.get_ticks()  #salvo l'ultimo toggle

                
        while self.running: 
            self.screen.fill((0,0,0)) # color the background

            for player in self.players:
                # tutto quello che viene a partire da qui sarà da mettere in un for per tutti i player
                pygame.draw.circle(self.screen, "red", (player.x, player.y), player.radius)
                player.disegna_versore(self.screen)

                # fai ruotare se premuto tasto d o a 
                if player.turn_left: 
                    player.ruota_versore(counter_clockwise=True) 
                if player.turn_right: 
                    player.ruota_versore(counter_clockwise=False) 
    
                player.spostamento(self.delta_time)   #aggiorna la posizione del cerchio

                if self.disegna_traccia:
                    self.coordinate_traccia.append((player.x - player.nx * player.radius, player.y - player.ny * player.radius))

                for coordinate in self.coordinate_traccia:     # disegna la traccia
                    pygame.draw.circle(self.screen, "red", coordinate, self.raggio_traccia)
                

                if player.tocca_bordo(self.screen) or player.tocca_traccia(self.coordinate_traccia, self.raggio_traccia):
                    player.vanish()
                    self.game_over()
                    


                self.tempo_attuale = pygame.time.get_ticks()
                if self.tempo_attuale - self.ultimo_toggle >= self.intervallo_traccia:
                    if self.disegna_traccia:
                        self.intervallo_traccia = self.tempo_traccia_off
                    else:
                        self.intervallo_traccia = self.tempo_traccia_on
                    self.disegna_traccia = not self.disegna_traccia
                    self.ultimo_toggle = self.tempo_attuale


                for event in pygame.event.get():
                    if event.type == pygame.QUIT: 
                        self.running = False
                    if event.type == pygame.KEYDOWN:  
                        if event.key == player.turn_right_key: #se premuto tasto "d"
                            player.turn_right = True       
                        if event.key == player.turn_left_key: # se premuto tasto "a"
                            player.turn_left = True        
                    if event.type == pygame.KEYUP:   
                        if event.key == player.turn_right_key: # se rilasciato tasto "d"
                            player.turn_right = False  
                        if event.key == player.turn_left_key: # se rilasciato tasto "a"
                            player.turn_left = False   

                        
                pygame.display.flip()   # mostra tutto quello che c'è da mostarre

                self.delta_time = self.clock.tick(60)   
                self.delta_time = max(0.001, min(0.1, self.delta_time))    # come sicurezza ulteriore, mi assicuro di prendere delta time a meno che sia compreso tra un tempo massimo e uno minimo, per non prendere valori di delta time troppo estremi 


        pygame.quit()





# esecuzione del gioco
gioco = Game()
gioco.play()
