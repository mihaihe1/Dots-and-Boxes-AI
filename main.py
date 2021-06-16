import pygame
import sys
import copy
import time
import statistics

class Buton:
    def __init__(self, display=None, left=0, top=0, w=0, h=0,culoareFundal=(89,134,194), culoareFundalSel=(53,80,115), text="", font="arial", fontDimensiune=16, culoareText=(255,255,255), valoare=""):
        self.display=display
        self.culoareFundal=culoareFundal
        self.culoareFundalSel=culoareFundalSel
        self.text=text
        self.font=font
        self.w=w
        self.h=h
        self.selectat=False
        self.fontDimensiune=fontDimensiune
        self.culoareText=culoareText
        #creez obiectul font
        fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
        self.textRandat=fontObj.render(self.text, True , self.culoareText)
        self.dreptunghi=pygame.Rect(left, top, w, h)
        #aici centram textul
        self.dreptunghiText=self.textRandat.get_rect(center=self.dreptunghi.center)
        self.valoare=valoare

    def selecteaza(self,sel):
        self.selectat=sel
        self.deseneaza()

    def selecteazaDupacoord(self,coord):
        if self.dreptunghi.collidepoint(coord) and self.selectat == False:
            self.selecteaza(True)
            return True
        return False

    def updateDreptunghi(self):
        self.dreptunghi.left=self.left
        self.dreptunghi.top=self.top
        self.dreptunghiText=self.textRandat.get_rect(center=self.dreptunghi.center)

    def deseneaza(self):
        culoareF= self.culoareFundalSel if self.selectat else self.culoareFundal
        pygame.draw.rect(self.display, culoareF, self.dreptunghi)
        self.display.blit(self.textRandat ,self.dreptunghiText)

class GrupButoane:
    def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10,left=0, top=0):
        self.listaButoane=listaButoane
        self.indiceSelectat=indiceSelectat
        self.listaButoane[self.indiceSelectat].selectat=True
        self.top=top
        self.left=left
        leftCurent=self.left
        for b in self.listaButoane:
            b.top=self.top
            b.left=leftCurent
            b.updateDreptunghi()
            leftCurent+=(spatiuButoane+b.w)

    def selecteazaDupacoord(self,coord):
        for ib,b in enumerate(self.listaButoane):
            if b.selecteazaDupacoord(coord):
                self.listaButoane[self.indiceSelectat].selecteaza(False)
                self.indiceSelectat=ib
                return True
        return False

    def deseneaza(self):
        #atentie, nu face wrap
        for b in self.listaButoane:
            b.deseneaza()

    def getValoare(self):
        return self.listaButoane[self.indiceSelectat].valoare


def deseneaza_alegeri(display, tabla_curenta):
    #c1 - alegeri inceput joc
    btn_alg=GrupButoane(
        top=30,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="minimax", valoare="minimax"),
            Buton(display=display, w=90, h=30, text="alphabeta", valoare="alphabeta")
            ],
        indiceSelectat=1)

    btn_est=GrupButoane(
        top=100,
        left=30,
        listaButoane=[
            Buton(display=display, w=100, h=30, text="estimare_1", valoare="estimare_1"),
            Buton(display=display, w=100, h=30, text="estimare_2", valoare="estimare_2")
            ])

    btn_juc=GrupButoane(
        top=170,
        left=30,
        listaButoane=[
            Buton(display=display, w=35, h=30, text="x", valoare="x"),
            Buton(display=display, w=45, h=30, text="zero", valoare="0")
            ],
        indiceSelectat=0)
    #c2 - nivelul de dificultate
    btn_dif=GrupButoane(
        top=240,
        left=30,
        listaButoane=[
            Buton(display=display, w=60, h=30, text="usor", valoare="1"),
            Buton(display=display, w=60, h=30, text="mediu", valoare="2"),
            Buton(display=display, w=60, h=30, text="greu", valoare="3"),

            ],
        indiceSelectat=1)
    ok = Buton(display=display, top=310, left=30, w=40, h=30, text="ok", culoareFundal=(155, 0, 55))
    btn_alg.deseneaza()
    btn_juc.deseneaza()
    btn_dif.deseneaza()
    btn_est.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteazaDupacoord(pos):
                    if not btn_juc.selecteazaDupacoord(pos):
                        if not btn_dif.selecteazaDupacoord(pos):
                            if not btn_est.selecteazaDupacoord(pos):
                                if ok.selecteazaDupacoord(pos):
                                    # display.fill((0,0,0)) #stergere ecran
                                    # tabla_curenta.deseneazaEcranJoc(0, 0)
                                    return btn_alg.getValoare(), btn_est.getValoare(), btn_juc.getValoare(), int(btn_dif.getValoare())
        pygame.display.update()

class Celula:
    # coordonatele nodurilor ()
    grosimeZid = 7  # numar impar
    fundalCelula = (255, 255, 255)
    culoareLinii = (0, 0, 0)
    culoareX = (255, 0, 0)
    culoare0 = (0, 21, 255)
    afisImagini = True

    def __init__(self, left, top, w, h, lin, col, interfata, cod=0):
        self.dreptunghi = pygame.Rect(left, top, w, h)
        # self.display = display
        self.zid = [None, None, None, None]
        # zidurile vor fi pe pozitiile 0-sus, 1-dreapta, 2-jos, 3-stanga
        self.cod = 0
        #pentru fiecare celula se marcheaza cele 4 ziduri ale sale
        self.zid[0] = pygame.Rect(left, top - 1 - self.__class__.grosimeZid // 2, w, self.__class__.grosimeZid)
        self.zid[1] = pygame.Rect(left + w - self.__class__.grosimeZid // 2, top, self.__class__.grosimeZid, h)
        self.zid[2] = pygame.Rect(left, top + h - self.__class__.grosimeZid // 2, w, self.__class__.grosimeZid)
        self.zid[3] = pygame.Rect(left - 1 - self.__class__.grosimeZid // 2, top, self.__class__.grosimeZid, h)

    # print(self.zid)
    # 0001 zid doar sus
    # 0011 zid sus si dreapta etc
    def deseneaza(self):
        #desenarea celor 4 colturi ale celulei cu un cerc
        #c4 - desenare cercuri
        pygame.draw.circle(Interfata.ecr, self.__class__.culoareLinii, self.dreptunghi.topleft, 8)
        pygame.draw.circle(Interfata.ecr, self.__class__.culoareLinii, self.dreptunghi.topright, 8)
        pygame.draw.circle(Interfata.ecr, self.__class__.culoareLinii, self.dreptunghi.bottomleft, 8)
        pygame.draw.circle(Interfata.ecr, self.__class__.culoareLinii, self.dreptunghi.bottomright, 8)
        # masti=[1,2,4,8]
        masca = 1
        for i in range(4):
            if self.cod & masca:
                if self.zid[i]:
                    pygame.draw.rect(Interfata.ecr, self.__class__.culoareLinii, self.zid[i])
            masca *= 2


class Interfata:
    culoareEcran = (255, 255, 255)

    JMIN = None
    JMAX = None
    dimCelula = 50
    paddingCelula = 5
    dimImagine = dimCelula - 2 * paddingCelula
    ecr = pygame.display.set_mode(size=(400, 400))


    def __init__(self, matr, nrPlayer, nrComputer, nrLinii=7, nrColoane=10, ziduri_gasite=[]):
        self.nrLinii = nrLinii
        self.nrColoane = nrColoane
        self.nrPlayer = nrPlayer
        self.nrComputer = nrComputer
        if matr is None:
            self.matrCelule = [[Celula(left=col * (self.__class__.dimCelula + 1),
                                   top=lin * (self.__class__.dimCelula + 1), w=self.__class__.dimCelula,
                                   h=self.__class__.dimCelula, lin=lin, col=col, interfata=self) for col in
                            range(1, nrColoane)] for lin in range(1, nrLinii)]
        else:
            self.matrCelule = matr
        self.ziduri_gasite = ziduri_gasite

        #incarcarea si prelucrarea imaginilor pt jucatorul cu x si cel cu 0
        poza_x = pygame.image.load('poza_x.png')
        poza_0 = pygame.image.load('poza_0.png')
        poza_x_win = pygame.image.load('poza_x_win.png')
        poza_0_win = pygame.image.load('poza_0_win.png')
        self.poza_x = pygame.transform.scale(poza_x, (self.__class__.dimImagine, self.__class__.dimImagine))
        self.poza_0 = pygame.transform.scale(poza_0, (self.__class__.dimImagine, self.__class__.dimImagine))
        self.poza_x_win = pygame.transform.scale(poza_x_win, (self.__class__.dimImagine, self.__class__.dimImagine))
        self.poza_0_win = pygame.transform.scale(poza_0_win, (self.__class__.dimImagine, self.__class__.dimImagine))

    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def final(self):
        #verifica daca mai exista mutari posibile prin calcularea scorului total posibil
        #de asemenea, determina si castigatorul jocului
        #c7 - testare stare finala
        nrCelule = (self.nrLinii-1) * (self.nrColoane-1)
        if nrCelule == self.nrPlayer + self.nrComputer:
            if self.nrPlayer == self.nrComputer:
                return 'remiza'
            elif self.nrPlayer > self.nrComputer:
                return Interfata.JMIN
            else:
                return Interfata.JMAX
        return False

    def mutari(self, jucator):
        #se vor genera toate zidurile posibile si se vor pastra numai zidurile in care se poate muta
        #daca se inchide o celula va fi modificat scorul jucatorului curent si i se pastreaza dreptul de a muta
        #pentru zidurile generate se verifica si daca acestea sunt ziduri pentru alte celule
        #c5 - functia de generare a mutarilor
        l_mutari = []
        juc_opus = self.jucator_opus(jucator)
        for il, linie in enumerate(self.matrCelule):
            for ic, cel in enumerate(linie):
                for iz, zid in enumerate(cel.zid):
                    if zid and (il, ic, iz) not in self.ziduri_gasite:
                        matr_copie = copy.deepcopy(self.matrCelule)
                        ziduri_copie = copy.deepcopy(self.ziduri_gasite)
                        scor_player_copie = copy.deepcopy(self.nrPlayer)
                        scor_computer_copie = copy.deepcopy(self.nrComputer)
                        acelasi_jucator = False
                        matr_copie[il][ic].cod |= 2 ** iz
                        if il > 0 and iz == 0:
                            ziduri_copie.append((il-1, ic, 2))
                            matr_copie[il-1][ic].cod |= 2 ** 2
                            if matr_copie[il-1][ic].cod == 15:
                                if jucator == Interfata.JMIN:
                                    scor_player_copie += 1
                                if jucator == Interfata.JMAX:
                                    scor_computer_copie += 1
                                acelasi_jucator = True

                        if ic < self.nrColoane-2 and iz == 1:
                            ziduri_copie.append((il, ic+1, 3))
                            matr_copie[il][ic+1].cod |= 2 ** 3
                            if matr_copie[il][ic+1].cod == 15:
                                if jucator == Interfata.JMIN:
                                    scor_player_copie += 1
                                if jucator == Interfata.JMAX:
                                    scor_computer_copie += 1
                                acelasi_jucator = True


                        if il < self.nrLinii-2 and iz == 2:
                            ziduri_copie.append((il+1, ic, 0))
                            matr_copie[il+1][ic].cod |= 2 ** 0
                            if matr_copie[il+1][ic].cod == 15:
                                if jucator == Interfata.JMIN:
                                    scor_player_copie += 1
                                if jucator == Interfata.JMAX:
                                    scor_computer_copie += 1
                                acelasi_jucator = True

                        if ic > 0 and iz == 3:
                            ziduri_copie.append((il, ic-1, 1))
                            matr_copie[il][ic-1].cod |= 2 ** 1
                            if matr_copie[il][ic-1].cod == 15:
                                if jucator == Interfata.JMIN:
                                    scor_player_copie += 1
                                if jucator == Interfata.JMAX:
                                    scor_computer_copie += 1
                                acelasi_jucator = True

                        if matr_copie[il][ic].cod == 15:
                            if jucator == Interfata.JMIN:
                                scor_player_copie += 1
                            if jucator == Interfata.JMAX:
                                scor_computer_copie += 1
                            acelasi_jucator = True
                        ziduri_copie.append((il, ic, iz))
                        intf = Interfata(matr_copie, scor_player_copie, scor_computer_copie, self.nrLinii, self.nrColoane, ziduri_copie)
                        if acelasi_jucator:
                            l_mutari.append((intf, jucator))
                        else:
                            l_mutari.append((intf, juc_opus))

        return l_mutari

    def estimeaza_scor(self, adancime,tip_estimat="estimare_1"):
        #c8 - estimare scor
        t_final = self.final()

        # daca starea e finala, in functie de cine a castigat, returneaza un nr mare
        if t_final == self.__class__.JMAX:
            return (999 + adancime)
        elif t_final == self.__class__.JMIN:
            return (-999 - adancime)
        elif t_final == 'remiza':
            return 0
        else:
            #estimare 1: returneaza diferenta dintre scor calculator si scor jucator, iar cu cat e mai mare, starea e mai buna pt calculator
            if tip_estimat == "estimare_1":
                return self.nrComputer - self.nrPlayer

            #estimare 2: returneaza diferenta de la estimare 1 + nr de celule cu 3 ziduri
            #in plus fata de celulele capturate, va calcula si celulele pe care urmeaza sa le inchida
            if tip_estimat == 'estimare_2':

                nr_cel = 0
                for lin in self.matrCelule:
                    for cel in lin:
                        if cel.cod in [14, 13, 11, 7]:
                            nr_cel += 1
                return self.nrComputer - self.nrPlayer + nr_cel


    def deseneazaEcranJoc(self, scor_jucator, scor_computer):
        #c4 - desenarea tablei de joc
        self.ecr.fill(self.__class__.culoareEcran)
        for linie in self.matrCelule:
            for cel in linie:
                cel.deseneaza()

        pygame.display.update()

class Stare:

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile (tot de tip Stare) din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        # e de tip Stare (cel mai bun succesor)
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)  # lista de informatii din nodurile succesoare
        # juc_opus = Interfata.jucator_opus(self.j_curent)

        # mai jos calculam lista de noduri-fii (succesori)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for (mutare, juc_opus) in l_mutari]

        return l_stari_mutari


def min_max(stare, tip_estimat):
    global cnt
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime, tip_estimat)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(mutare, tip_estimat) for mutare in stare.mutari_posibile]
    # c9c nr noduri
    cnt += len(mutariCuEstimare)

    if stare.j_curent == Interfata.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)
    stare.estimare = stare.stare_aleasa.estimare
    return stare


def alpha_beta(alpha, beta, stare, tip_estimat):
    global cnt
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime, tip_estimat)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()
    #c9c nr noduri
    cnt += len(stare.mutari_posibile)
    if stare.j_curent == Interfata.JMAX:
        estimare_curenta = float('-inf')
        #c12 - ordonare succesori
        stare.mutari_posibile = sorted(stare.mutari_posibile, key=lambda x: x.tabla_joc.estimeaza_scor(stare.adancime), reverse=True)
        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare, tip_estimat)

            if (estimare_curenta < stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (alpha < stare_noua.estimare):
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Interfata.JMIN:
        estimare_curenta = float('inf')
        stare.mutari_posibile = sorted(stare.mutari_posibile, key=lambda x: x.tabla_joc.estimeaza_scor(stare.adancime))
        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare, tip_estimat)

            if (estimare_curenta > stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare

            if (beta > stare_noua.estimare):
                beta = stare_noua.estimare
                if alpha >= beta:
                    break
    stare.estimare = stare.stare_aleasa.estimare

    return stare


pygame.init()
#c4 - titlu fereastra
pygame.display.set_caption("Hernest Mihai - Dots and Boxes")

interf = Interfata(None, 0, 0, nrLinii=4, nrColoane=4)
# Interfata.JMIN, tip_algoritm = deseneaza_alegeri()
tip_algoritm, estimare, Interfata.JMIN, dificultate = deseneaza_alegeri(Interfata.ecr, interf)
if Interfata.JMIN == 'x':
    Interfata.JMAX = '0'
else:
    Interfata.JMAX = 'x'
# Interfata.ecr.blit(text, textRect)
interf.deseneazaEcranJoc(0, 0)
font = pygame.font.Font('freesansbold.ttf', 20)
text_jucator = font.render('Scor jucator: 0', True, (255, 255, 255), (0, 0, 0))
text_computer = font.render('Scor computer: 0', True, (255, 255, 255), (0, 0, 0))
text_final = font.render('Castigator: ', True, (255, 255, 255), (0, 0, 0))
textRect1 = text_jucator.get_rect()
textRect1.center = (100, 250)
textRect2 = text_computer.get_rect()
textRect2.center = (100, 300)
textRect4 = text_final.get_rect()
textRect4.center = (150, 150)

jucator = True
ultima_mutare = [None, None, None, None]
#c3 - generare stare initiala
stare_curenta = Stare(interf, 'x', dificultate)
text_mutare = font.render('Este randul jucatorului: x', True, (255, 255, 255), (0, 0, 0))
textRect3 = text_mutare.get_rect()
textRect3.center = (350, 100)
# Interfata.JMIN = 'x'
# Interfata.JMAX = '0'
scor_juc = 0
scor_comp = 0
celule_jucator = []
celule_calculator = []
timp_asteptare_calc = []
matr_debug = [ [ 0 for i in range(4) ] for j in range(4) ]
ok_juc = False

timp_start_joc = t_inainte = int(round(time.time() * 1000))
nr_mutari_juc = 0
nr_mutari_calc = 0
cnt = 0

noduri_generate = []

while True:
    text_jucator = font.render('Scor jucator: ' + str(scor_juc), True, (255, 255, 255), (0, 0, 0))
    text_computer = font.render('Scor computer: ' + str(scor_comp), True, (255, 255, 255), (0, 0, 0))
    Interfata.ecr.blit(text_jucator, textRect1)
    Interfata.ecr.blit(text_computer, textRect2)

    if stare_curenta.tabla_joc.final():
        timp_final_joc = int(round(time.time() * 1000))
        #c9d afisare timp final si nr mutari
        print("Jocul a durat: " + str(timp_final_joc-timp_start_joc) + " milisecunde")
        print("Numar mutari jucator: " + str(nr_mutari_juc))
        print("Numar mutari calculator: " + str(nr_mutari_calc))
        pygame.draw.rect(Interfata.ecr, Celula.culoareLinii, ultima_mutare)
        semn_castigator = stare_curenta.tabla_joc.final()
        #c7 - colorare configuratie castigatoare
        if semn_castigator == 'x':
            poza = stare_curenta.tabla_joc.poza_x_win
            if stare_curenta.tabla_joc.nrPlayer > stare_curenta.tabla_joc.nrComputer:
                for c in celule_jucator:
                    Interfata.ecr.blit(poza, (
                        c.dreptunghi.left + Interfata.paddingCelula,
                        c.dreptunghi.top + Interfata.paddingCelula))
            else:
                for c in celule_calculator:
                    Interfata.ecr.blit(poza, (
                        c.dreptunghi.left + Interfata.paddingCelula,
                        c.dreptunghi.top + Interfata.paddingCelula))
        elif semn_castigator == '0':
            poza = stare_curenta.tabla_joc.poza_0_win
            if stare_curenta.tabla_joc.nrPlayer > stare_curenta.tabla_joc.nrComputer:
                for c in celule_jucator:
                    Interfata.ecr.blit(poza, (
                        c.dreptunghi.left + Interfata.paddingCelula,
                        c.dreptunghi.top + Interfata.paddingCelula))
            else:
                for c in celule_calculator:
                    Interfata.ecr.blit(poza, (
                        c.dreptunghi.left + Interfata.paddingCelula,
                        c.dreptunghi.top + Interfata.paddingCelula))

        pygame.display.update()
        time.sleep(3)
        Interfata.ecr.fill((255, 255, 255))
        #c1 - afisare castigator
        if stare_curenta.tabla_joc.nrPlayer > stare_curenta.tabla_joc.nrComputer:
            text_final = font.render('Castigator: player', True, (255, 255, 255), (0, 0, 0))
            Interfata.ecr.blit(text_final, textRect4)
        elif stare_curenta.tabla_joc.nrPlayer < stare_curenta.tabla_joc.nrComputer:
            text_final = font.render('Castigator: computer', True, (255, 255, 255), (0, 0, 0))
            Interfata.ecr.blit(text_final, textRect4)
        else:
            text_final = font.render('Remiza', True, (255, 255, 255), (0, 0, 0))
            Interfata.ecr.blit(text_final, textRect4)
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        #c9a - min, max, mediu, mediana calculator
        print("Timpul minim de asteptare calculator: " + str(min(timp_asteptare_calc)))
        print("Timpul maxim de asteptare calculator: " + str(max(timp_asteptare_calc)))
        print("Timpul mediu de asteptare calculator: " + str(sum(timp_asteptare_calc) / len(timp_asteptare_calc)))
        print("Mediana timp: " + str(statistics.median(timp_asteptare_calc)))
        #c9c final nr noduri
        print("Nr minim noduri: " + str(min(noduri_generate)))
        print("Nr maxim noduri: " + str(max(noduri_generate)))
        print("Nr mediu noduri: " + str(sum(noduri_generate) / len(noduri_generate)))
        print("Mediana noduri: " + str(statistics.median(noduri_generate)))
        sys.exit()

    if stare_curenta.j_curent == Interfata.JMIN:
        text_mutare = font.render('Muta: ' + Interfata.JMIN, True, (255, 255, 255), (0, 0, 0))
        # print(Interfata.JMIN)
        Interfata.ecr.blit(text_mutare, textRect3)
        if not ok_juc:
            nr_mutari_juc += 1
            t_inainte = int(round(time.time() * 1000))
            ok_juc = True
            print("Scor:  Jucator "+str(stare_curenta.tabla_joc.nrPlayer)+ " - Calculator: " + str(stare_curenta.tabla_joc.nrComputer))
        for ev in pygame.event.get():
            # daca utilizatorul face click pe x-ul de inchidere a ferestrei
            if ev.type == pygame.QUIT:
                pygame.quit()
                timp_final_joc = int(round(time.time() * 1000))
                print("Jocul a durat: " + str(timp_final_joc - timp_start_joc) + " milisecunde")
                print("Numar mutari jucator: " + str(nr_mutari_juc))
                print("Numar mutari calculator: " + str(nr_mutari_calc))
                print("Timpul minim de asteptare calculator: " + str(min(timp_asteptare_calc)))
                print("Timpul maxim de asteptare calculator: " + str(max(timp_asteptare_calc)))
                print("Timpul mediu de asteptare calculator: " + str(sum(timp_asteptare_calc) / len(timp_asteptare_calc)))
                print("Mediana: " + str(statistics.median(timp_asteptare_calc)))
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_i:
                    Celula.afisImagini = not Celula.afisImagini
                    stare_curenta.tabla_joc.deseneazaEcranJoc(scor_juc, scor_comp)
            # daca utilizatorul a facut click
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                #c6 - click jucator
                pos = pygame.mouse.get_pos()
                zidGasit = []
                for il, linie in enumerate(stare_curenta.tabla_joc.matrCelule):
                    for ic, cel in enumerate(linie):
                        for iz, zid in enumerate(cel.zid):
                            if zid and zid.collidepoint(pos) and (il, ic, iz) not in stare_curenta.tabla_joc.ziduri_gasite:
                                t_dupa = int(round(time.time() * 1000))
                                print("Jucatorul a gandit timp de "+str(t_dupa-t_inainte)+" milisecunde.")
                                ok_juc = False
                                zidGasit.append((cel, iz, zid))
                                stare_curenta.tabla_joc.ziduri_gasite.append((il, ic, iz))

                celuleAfectate = []
                ok = False
                if 0 < len(zidGasit) <= 2:
                    if jucator:
                        culoare = Celula.culoareX
                    else:
                        culoare = Celula.culoare0
                    for (cel, iz, zid) in zidGasit:
                        if ultima_mutare != [None, None, None, None]:
                            #deseneaza cu negru ultima mutare la urmatoarea mutare
                            pygame.draw.rect(Interfata.ecr, Celula.culoareLinii, ultima_mutare)
                        pygame.draw.rect(Interfata.ecr, culoare, zid)
                        ultima_mutare = zid
                        cel.cod |= 2 ** iz
                        if cel.cod == 15:
                            ok = True
                        celuleAfectate.append(cel)

                    if not ok:
                        stare_curenta.j_curent = Interfata.JMAX
                        #c1 - afisarea a cui este randul jucator
                        text_mutare = font.render('Muta: ' + stare_curenta.j_curent, True, (255, 255, 255), (0, 0, 0))
                        # print(Interfata.JMIN)
                        Interfata.ecr.blit(text_mutare, textRect3)
                    print("\nMatrice interfata: JUCATOR")
                    #c4 - afisare tabla
                    for l in stare_curenta.tabla_joc.matrCelule:
                        for c in l:
                            print(c.cod, end=" ")
                        print()
                for celA in celuleAfectate:
                    if celA.cod == 15 and Celula.afisImagini:
                        celule_jucator.append(celA)
                        scor_juc += 1
                        #c9b scor jucator
                        text_jucator = font.render('Scor jucator: ' + str(scor_juc), True, (255, 255, 255), (0, 0, 0))
                        Interfata.ecr.blit(text_jucator, textRect1)
                        poza = stare_curenta.tabla_joc.poza_x if Interfata.JMIN == 'x' else stare_curenta.tabla_joc.poza_0
                        Interfata.ecr.blit(poza, (
                            celA.dreptunghi.left + Interfata.paddingCelula,
                            celA.dreptunghi.top + Interfata.paddingCelula))
                        # stare_curenta.tabla_joc.deseneazaImag(interf.furios, celA)
                        stare_curenta.tabla_joc.nrPlayer += 1

                pygame.display.update()
    else:
        if stare_curenta.j_curent == Interfata.JMAX:
            nr_mutari_calc += 1
            print("Scor:  Jucator " + str(stare_curenta.tabla_joc.nrPlayer) + " - Calculator: " + str(
                stare_curenta.tabla_joc.nrComputer))
            #c9a - incepe timer
            t_inainte = int(round(time.time() * 1000))
            text_mutare = font.render('Muta: ' + Interfata.JMAX, True, (255, 255, 255), (0, 0, 0))
            Interfata.ecr.blit(text_mutare, textRect3)

            for ev in pygame.event.get():
                # daca utilizatorul face click pe x-ul de inchidere a ferestrei
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    #c10 - jucatorul opreste jocul cand vrea
                    timp_final_joc = int(round(time.time() * 1000))
                    print("Jocul a durat: " + str(timp_final_joc - timp_start_joc) + " milisecunde")
                    print("Numar mutari jucator: " + str(nr_mutari_juc))
                    print("Numar mutari calculator: " + str(nr_mutari_calc))
                    print("Nr minim noduri: " + str(min(noduri_generate)))
                    print("Nr maxim noduri: " + str(max(noduri_generate)))
                    print("Nr mediu noduri: " + str(sum(noduri_generate) / len(noduri_generate)))
                    print("Mediana noduri: " + str(statistics.median(noduri_generate)))
                    sys.exit()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_i:
                        Celula.afisImagini = not Celula.afisImagini
                        interf.deseneazaEcranJoc(scor_juc, scor_comp)
            cnt = 0
            if tip_algoritm == 'minimax':
                stare_actualizata = min_max(stare_curenta, estimare)
            else:
                stare_actualizata = alpha_beta(-1000, 1000, stare_curenta, estimare)

            #c9a sfarsit timer
            t_dupa = int(round(time.time() * 1000))

            print("Calculatorul a gandit timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            #c9a lista timp asteptare calculator
            timp_asteptare_calc.append(t_dupa - t_inainte)
            #c9c nr noduri generate
            print("Noduri generate: " + str(cnt))
            noduri_generate.append(cnt)
            #c9b - estimare
            print("Estimare: " + str(stare_actualizata.estimare))
            zid_initial = []
            acelasi_juc = False
            for il, linie in enumerate(stare_actualizata.stare_aleasa.tabla_joc.matrCelule):
                for ic, cel in enumerate(linie):
                    if stare_actualizata.stare_aleasa.tabla_joc.matrCelule[il][ic].cod != stare_curenta.tabla_joc.matrCelule[il][ic].cod:
                        dif = stare_actualizata.stare_aleasa.tabla_joc.matrCelule[il][ic].cod - stare_curenta.tabla_joc.matrCelule[il][ic].cod
                        if stare_actualizata.stare_aleasa.tabla_joc.matrCelule[il][ic].cod == 15:
                            #c9b scor computer
                            text_computer = font.render('Scor computer: ' + str(scor_comp), True, (255, 255, 255),
                                                        (0, 0, 0))
                            Interfata.ecr.blit(text_computer, textRect2)
                            poza = stare_curenta.tabla_joc.poza_x if Interfata.JMAX == 'x' else stare_curenta.tabla_joc.poza_0
                            Interfata.ecr.blit(poza, (
                                cel.dreptunghi.left + Interfata.paddingCelula,
                                cel.dreptunghi.top + Interfata.paddingCelula))
                            scor_comp += 1
                            celule_calculator.append(cel)
                            acelasi_juc = True

                        for iz, zid in enumerate(cel.zid):
                            if 2**iz == dif:
                                if ultima_mutare != [None, None, None, None]:
                                    pygame.draw.rect(Interfata.ecr, Celula.culoareLinii, ultima_mutare)
                                pygame.draw.rect(Interfata.ecr, (200, 200, 200), zid)
                                ultima_mutare = zid
                                stare_actualizata.stare_aleasa.tabla_joc.ziduri_gasite.append((il, ic, iz))

            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("\nMatrice interfata: COMPUTER")
            for l in stare_curenta.tabla_joc.matrCelule:
                for c in l:
                    print(c.cod, end=" ")
                print()
            if not acelasi_juc:
                stare_curenta.j_curent = Interfata.JMIN
                # c1 - afisarea a cui este randul calculator
                text_mutare = font.render('Muta: ' + stare_curenta.j_curent, True, (255, 255, 255), (0, 0, 0))
                Interfata.ecr.blit(text_mutare, textRect3)

            pygame.display.update()