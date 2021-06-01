import pygame
import sys
import copy

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
        # if lin > 0:
        self.zid[0] = pygame.Rect(left, top - 1 - self.__class__.grosimeZid // 2, w, self.__class__.grosimeZid)
        self.zid[1] = pygame.Rect(left + w - self.__class__.grosimeZid // 2, top, self.__class__.grosimeZid, h)
        self.zid[2] = pygame.Rect(left, top + h - self.__class__.grosimeZid // 2, w, self.__class__.grosimeZid)
        self.zid[3] = pygame.Rect(left - 1 - self.__class__.grosimeZid // 2, top, self.__class__.grosimeZid, h)

    # print(self.zid)
    # 0001 zid doar sus
    # 0011 zid sus si dreapta etc
    def deseneaza(self):
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
        # self.ecran = ecran
        self.nrPlayer = nrPlayer
        self.nrComputer = nrComputer
        # self.lista_player = copy.deepcopy(lis)
        if matr is None:
            self.matrCelule = [[Celula(left=col * (self.__class__.dimCelula + 1),
                                   top=lin * (self.__class__.dimCelula + 1), w=self.__class__.dimCelula,
                                   h=self.__class__.dimCelula, lin=lin, col=col, interfata=self) for col in
                            range(1, nrColoane)] for lin in range(1, nrLinii)]
        else:
            self.matrCelule = matr
        self.ziduri_gasite = ziduri_gasite


        furios = pygame.image.load('foarte_furioasa_m.png')

        self.furios = pygame.transform.scale(furios, (self.__class__.dimImagine, self.__class__.dimImagine))
        vesel = pygame.image.load('smiley_galben_vesel.png')

        self.vesel = pygame.transform.scale(vesel, (self.__class__.dimImagine, self.__class__.dimImagine))

    @classmethod
    def jucator_opus(cls, jucator):
        # val_true if conditie else val_false
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def final(self):
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
        t_final = self.final()

        # daca starea e finala, in functie de cine a castigat, returneaza un nr ft mare
        if t_final == self.__class__.JMAX:
            return (999 + adancime)
        elif t_final == self.__class__.JMIN:
            return (-999 - adancime)
        elif t_final == 'remiza':
            return 0
        else:
            if tip_estimat == "estimare_1":
                # Estimarea 1: Nr patratele capturate calculator - nr patratele calculate player = > cu cat nr e mai mare cu atat starea e mai buna pentru MAX
                return self.nrComputer - self.nrPlayer

    def deseneazaImag(self, imag, cel):
        pass
        # self.ecran.blit(imag, (
        # cel.dreptunghi.left + self.__class__.paddingCelula, cel.dreptunghi.top + self.__class__.paddingCelula))

    def deseneazaEcranJoc(self, scor_jucator, scor_computer):
        self.ecr.fill(self.__class__.culoareEcran)
        # font = pygame.font.Font('freesansbold.ttf', 26)
        # text_jucator = font.render('Scor jucator: ' + str(scor_jucator), True, (255, 255, 255), (0, 0, 0))
        # text_computer = font.render('Scor computer: ' + str(scor_computer), True, (255, 255, 255), (0, 0, 0))
        # textRect1 = text_jucator.get_rect()
        # textRect1.center = (100, 250)
        # textRect2 = text_computer.get_rect()
        # textRect2.center = (100, 300)
        # self.ecr.blit(text_jucator, textRect1)
        # self.ecr.blit(text_computer, textRect2)
        for linie in self.matrCelule:
            for cel in linie:
                cel.deseneaza()
                # if Celula.afisImagini:
                #     imag = self.vesel if cel.cod != 15 else self.furios
                #     self.deseneazaImag(imag, cel)
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


def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(mutare) for mutare in stare.mutari_posibile]
    print("MCE")
    print(len(mutariCuEstimare))
    print()
    if stare.j_curent == Interfata.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)
    stare.estimare = stare.stare_aleasa.estimare
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Interfata.JMAX:
        estimare_curenta = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta < stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (alpha < stare_noua.estimare):
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Interfata.JMIN:
        estimare_curenta = float('inf')

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

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

interf = Interfata(None, 0, 0, nrLinii=4, nrColoane=4)
# Interfata.JMIN, tip_algoritm = deseneaza_alegeri()
tip_algoritm, estimare, Interfata.JMIN, dificultate = deseneaza_alegeri(Interfata.ecr, interf)
if Interfata.JMIN == 'x':
    Interfata.JMAX = '0'
else:
    Interfata.JMAX = 'x'
# Interfata.ecr.blit(text, textRect)
interf.deseneazaEcranJoc(0, 0)
# bucla jocului care imi permite sa tot fac mutari
font = pygame.font.Font('freesansbold.ttf', 20)
text_jucator = font.render('Scor jucator: 0', True, (255, 255, 255), (0, 0, 0))
text_computer = font.render('Scor computer: 0', True, (255, 255, 255), (0, 0, 0))
textRect1 = text_jucator.get_rect()
textRect1.center = (100, 250)
textRect2 = text_computer.get_rect()
textRect2.center = (100, 300)
Interfata.ecr.blit(text_jucator, textRect1)
Interfata.ecr.blit(text_computer, textRect2)

jucator = True
ultima_mutare = [None, None, None, None]
stare_curenta = Stare(interf, 'x', dificultate)
# Interfata.JMIN = 'x'
# Interfata.JMAX = '0'
scor_juc = 0
scor_comp = 0

while True:
    font = pygame.font.Font('freesansbold.ttf', 20)
    text_jucator = font.render('Scor jucator: ' + str(scor_juc), True, (255, 255, 255), (0, 0, 0))
    text_computer = font.render('Scor computer: ' + str(scor_comp), True, (255, 255, 255), (0, 0, 0))
    textRect1 = text_jucator.get_rect()
    textRect1.center = (100, 250)
    textRect2 = text_computer.get_rect()
    textRect2.center = (100, 300)
    Interfata.ecr.blit(text_jucator, textRect1)
    Interfata.ecr.blit(text_computer, textRect2)
    cnt = 0
    for l in stare_curenta.tabla_joc.matrCelule:
        for c in l:
            if c.cod == 15:
                cnt += 1
    # if cnt == (interf.nrLinii-1) * (interf.nrColoane-1):
    #     pygame.quit()
    #     sys.exit()
    if stare_curenta.j_curent == Interfata.JMIN:
        for ev in pygame.event.get():
            # daca utilizatorul face click pe x-ul de inchidere a ferestrei
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_i:
                    Celula.afisImagini = not Celula.afisImagini
                    stare_curenta.tabla_joc.deseneazaEcranJoc(scor_juc, scor_comp)
            # daca utilizatorul a facut click
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                zidGasit = []
                for il, linie in enumerate(stare_curenta.tabla_joc.matrCelule):
                    for ic, cel in enumerate(linie):
                        for iz, zid in enumerate(cel.zid):
                            if zid and zid.collidepoint(pos):
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
                            pygame.draw.rect(Interfata.ecr, Celula.culoareLinii, ultima_mutare)
                        pygame.draw.rect(Interfata.ecr, culoare, zid)
                        ultima_mutare = zid
                        cel.cod |= 2 ** iz
                        if cel.cod == 15:
                            ok = True
                        celuleAfectate.append(cel)

                    if not ok:
                        stare_curenta.j_curent = Interfata.JMAX
                    print("\nMatrice interfata: JUCATOR")
                    for l in stare_curenta.tabla_joc.matrCelule:
                        for c in l:
                            print(c.cod, end=" ")
                        print()
                for celA in celuleAfectate:
                    if celA.cod == 15 and Celula.afisImagini:
                        scor_juc += 1
                        stare_curenta.tabla_joc.deseneazaImag(interf.furios, celA)
                        stare_curenta.tabla_joc.nrPlayer += 1

                pygame.display.update()
    else:
        if stare_curenta.j_curent == Interfata.JMAX:
            for ev in pygame.event.get():
                # daca utilizatorul face click pe x-ul de inchidere a ferestrei
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_i:
                        Celula.afisImagini = not Celula.afisImagini
                        interf.deseneazaEcranJoc(scor_juc, scor_comp)

            if tip_algoritm == 'minimax':
                stare_actualizata = min_max(stare_curenta)
            else:
                stare_actualizata = alpha_beta(-1000, 1000, stare_curenta)

            zid_initial = []
            acelasi_juc = False
            for il, linie in enumerate(stare_actualizata.stare_aleasa.tabla_joc.matrCelule):
                for ic, cel in enumerate(linie):
                    if stare_actualizata.stare_aleasa.tabla_joc.matrCelule[il][ic].cod != stare_curenta.tabla_joc.matrCelule[il][ic].cod:
                        dif = stare_actualizata.stare_aleasa.tabla_joc.matrCelule[il][ic].cod - stare_curenta.tabla_joc.matrCelule[il][ic].cod
                        if stare_actualizata.stare_aleasa.tabla_joc.matrCelule[il][ic].cod == 15:
                            scor_comp += 1
                            acelasi_juc = True
                        for iz, zid in enumerate(cel.zid):
                            if 2**iz == dif:
                                pygame.draw.rect(Interfata.ecr, (200, 200, 200), zid)
                                stare_curenta.tabla_joc.ziduri_gasite.append((il, ic, iz))

            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("\nMatrice interfata: COMPUTER")
            for l in stare_curenta.tabla_joc.matrCelule:
                for c in l:
                    print(c.cod, end=" ")
                print()
            if not acelasi_juc:
                stare_curenta.j_curent = Interfata.JMIN

            pygame.display.update()