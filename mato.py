import sys, pygame, random
pygame.init()
clock = pygame.time.Clock()

koko = leveys, korkeus = 360, 240
musta = 0, 0, 0
vihreä = 190, 210, 0
palikka = 10
kikkare = palikka/3
fps = 15

ruutu = pygame.display.set_mode(koko)
pygame.display.set_caption("Matopeli")
fontti = pygame.font.SysFont (None, 16)
isofontti = pygame.font.SysFont(None, 50)

def aloitus():

    intro = True
    while intro:
        ruutu.fill(vihreä)
        teksti_ruudulle("MATOPELI", musta, isofontti, -50, 0)
        teksti_ruudulle("U = Uusi peli", musta, fontti, 0, 1)
        teksti_ruudulle("L = Lopeta", musta, fontti, 30, 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    pygame.quit()
                if event.key == pygame.K_u:
                    intro = False

        pygame.display.update()

def lopetus (ennätys, pisteet, gameExit, gameOver):
    ruutu.fill(vihreä)

    if ennätys > pisteet:
        teksti_ruudulle("Hävisit pelin.", musta, isofontti, -50, 0)

    elif ennätys <= pisteet:
        with open("pisteet.txt", "w") as f:
            f.write(str(pisteet))
        f.close()
        teksti_ruudulle("Teit ennätyksen!", musta, isofontti, -50, 0)

    teksti_ruudulle("U = Uusi peli", musta, fontti, 0, 1)
    teksti_ruudulle("L = Lopeta", musta, fontti, 30, 1)
    pygame.display.update()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                gameExit = True
                gameOver = False
            if event.key == pygame.K_u:
                main()

    return gameExit, gameOver

def pisteet_ruudulle(pisteet, ennätys):

    pojot = fontti.render("Pisteet: " + str(pisteet), True, musta)
    enkka = fontti.render("Ennätys: " + str(ennätys), True, musta)

    ruutu.blit(enkka, [leveys-80, 5])
    ruutu.blit(pojot, [10,5])


def teksti_ruudulle(viesti, väri, fontti, y_offset, raja):
    textSurf = fontti.render(viesti, True, väri)
    textRect = textSurf.get_rect()
    textRect.center = leveys/2, korkeus/2 + y_offset

    if raja == 1:
        rect = textRect.inflate(8,5)
        pygame.draw.rect(ruutu, musta, rect, 1)
    ruutu.blit (textSurf, textRect)


def mato (matolista, palikka):
    for XY in matolista:
        pygame.draw.rect(ruutu, musta, [XY[0], XY[1], palikka, palikka])

def rajat (x, y):
    if x == leveys-10:
        x = 10
    if x < 10:
        x = leveys-20
    if y == korkeus-10:
        y = 20
    if y < 20:
        y = korkeus-20

    return x, y

def liike(x_muutos, y_muutos, liikevuoro):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN and liikevuoro == False:
            liikevuoro = True
            if event.key == pygame.K_LEFT:
                if x_muutos != palikka:
                    y_muutos = 0
                    x_muutos = -palikka

            elif event.key == pygame.K_RIGHT:
                if x_muutos != -palikka:
                    y_muutos = 0
                    x_muutos = palikka

            elif event.key == pygame.K_UP:
                if y_muutos != palikka:
                    x_muutos = 0
                    y_muutos = -palikka

            elif event.key == pygame.K_DOWN:
                if y_muutos != -palikka:
                    x_muutos = 0
                    y_muutos = palikka

    return x_muutos, y_muutos, liikevuoro

def main ():

    gameExit = False
    gameOver = False
    x = 100
    y = 100
    x_muutos = palikka
    y_muutos = 0
    matolista = []
    randx = round(random.randrange(10, leveys - 20) / 10) * 10
    randy = round(random.randrange(20, korkeus - 20) / 10) * 10
    pituus = 1
    pisteet = 0

    with open("pisteet.txt", "r") as f:
        for line in f:
            ennätys = int(line)
    f.close()

    while gameExit == False:

        liikevuoro = False
        x_muutos, y_muutos, liikevuoro = liike(x_muutos, y_muutos, liikevuoro)
        x += x_muutos
        y += y_muutos

        ruutu.fill(vihreä)
        pygame.draw.rect(ruutu, musta, [10, 20, leveys-20, korkeus-30], 1)
        x, y = rajat(x, y)

        if x == randx and y == randy:
            randx = round(random.randrange(10, leveys - 20) / 10) * 10
            randy = round(random.randrange(20, korkeus - 20) / 10) * 10

            for XY in matolista:
                if XY[0] == randx and XY[1] == randy:
                    randx = round(random.randrange(10, leveys - 20) / 10) * 10
                    randy = round(random.randrange(20, korkeus - 20) / 10) * 10

            pituus += 1
            pisteet += 1

        matopää = []
        matopää.append(x)
        matopää.append(y)
        matolista.append(matopää)

        pygame.draw.rect(ruutu, musta, [randx + kikkare, randy, kikkare, kikkare])
        pygame.draw.rect(ruutu, musta, [randx, randy + kikkare, kikkare, kikkare])
        pygame.draw.rect(ruutu, musta, [randx + 2*kikkare, randy + kikkare, kikkare, kikkare])
        pygame.draw.rect(ruutu, musta, [randx + kikkare, randy + 2*kikkare, kikkare, kikkare])

        if len(matolista) > pituus:
            del matolista[0]

        for pala in matolista[:-1]:
            if pala == matopää:
                gameOver = True

        mato(matolista, palikka)
        pisteet_ruudulle(pisteet, ennätys)
        pygame.display.update()
        clock.tick(fps)

        while gameOver == True:
            gameExit, gameOver = lopetus(ennätys, pisteet, gameExit, gameOver)

aloitus()
main()
pygame.quit()