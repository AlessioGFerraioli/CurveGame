import pygame

pygame.init()


# create the canvas that represents the screen in which the game is
screen = pygame.display.set_mode((640,640))

#loading the images
spillo_img = pygame.image.load('spillo.png').convert() #images are stored as pygame.Surface object. il convert è perché usa diversi modi di trattare pixels e convert converte automaticamente a quello piu veloce
spillo_img = pygame.transform.scale(spillo_img,                      
                                    (spillo_img.get_width() * 0.2,
                                     spillo_img.get_height() * 0.2)
                                    )  # rimpicciolisco l'immagine
spillo_img.set_colorkey((245,240,245))   # setto il color key cioè il colore da ignorare

witch1_img = pygame.image.load('witch1.png').convert_alpha()   # questa immagine ha un'alpha channel (trasparenza) e quindi uso convert_alpha


delta_time = 0.1     # dato che ogni schermo può avere max framerate diversi, usiamo questa variabile ausiliaria per assicurarci che il movimento sia uguale su tutti gli schermi (vedi sotto come la usiamo)


font = pygame.font.Font(None, size=30)
# initializing the parameter at the start of the game
x = 0   # x of the iamge
clock = pygame.time.Clock()  # definiamo un nostro clock del gioco perché altrimenti andrà alla velocità massima possibile, non controllabile

# main loop of the game
running = True
while running: 

    screen.fill((0,0,0)) # set the color of the background any frame

    pygame.draw.circle(screen, "red", (x,500), 20)
    screen.blit(spillo_img, (x, 30)) #carica l'immagine a una certa posizione x,30
    screen.blit(witch1_img, (x*0.5, 200))
    x += 50 * delta_time   #aggiorna la x dell'immagine
    text = font.render("Hello!", True, (255,255,0))
    screen.blit(text, (300,100))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # check if premiamo la X per chiudere
            running = False

    pygame.display.flip()   # mostra tutto quello che c'è da mostarre

    delta_time = clock.tick(60)   # clock.tick(60) ritorna il tempo in ms che ci ha messo per fare 60 frame
    delta_time = max(0.001, min(0.1, delta_time))    # come sicurezza ulteriore, mi assicuro di prendere delta time a meno che sia compreso tra un tempo massimo e uno minimo, per non prendere valori di delta time troppo estremi 


pygame.quit()