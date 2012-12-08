#
# Odskocna deska za resevanje prve seminarske raziskovalne naloge
#
# (postopek predvideva, da ste nastavili delovno mapo s podanimi datotekami o tekmah in statistikah)
#
#

# branje podatkov o tekmah

wl2012 <- read.table("fivb_world_league_2012.txt", na.strings = c("NA"), header = T)
wl2011 <- read.table("fivb_world_league_2011.txt", na.strings = c("NA"), header = T)
wl2010 <- read.table("fivb_world_league_2010.txt", na.strings = c("NA"), header = T)
wch2010 <- read.table("fivb_world_championship_2010.txt", na.strings = c("NA"), header = T)
wc2011 <- read.table("fivb_world_cup_2011.txt", na.strings = c("NA"), header = T)



# najprej bomo popravili zapis datuma v bolj primerno obliko

popraviEnDatum <- function(datum)
{
    meseci <- c("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

    string <- as.character(datum)

    komponente <- strsplit(string, "-")
    komponente <- unlist(komponente)

    leto <- as.numeric(komponente[3])
    mesec <- which(meseci == komponente[2])
    dan <- as.numeric(komponente[1])

    sprintf("%d%02d%02d", leto, mesec, dan) 
}

popraviDatume <- function(podatki)
{
    podatki$Date <- sapply(podatki$Date, popraviEnDatum)
    podatki
}


wl2012 <- popraviDatume(wl2012)
wl2011 <- popraviDatume(wl2011)
wl2010 <- popraviDatume(wl2010)
wch2010 <- popraviDatume(wch2010)
wc2011 <- popraviDatume(wc2011)


# dodali bomo stolpec z imenom tekmovanja (za poznejso rabo)
wl2012$Tournament <- "WL"
wl2011$Tournament <- "WL"
wl2010$Tournament <- "WL"
wch2010$Tournament <- "WCH"
wc2011$Tournament <- "WC"

# zdruzimo vse zapise o tekmah v en podatkovni okvir
tekme <- rbind(wl2012,wl2011,wl2010,wch2010,wc2011)

# uredimo tekme po datumu
tekme <- tekme[order(tekme$Date),]
tekme




# preberemo podatke o rangih
wrankoct2011 <- read.table("fivb_world_ranking_02-Oct-2011.txt", header = T)
wrankjan2012 <- read.table("fivb_world_ranking_04-Jan-2012.txt", header = T)
wrankjan2010 <- read.table("fivb_world_ranking_15-Jan-2010.txt", header = T)
wrankjan2011 <- read.table("fivb_world_ranking_15-Jan-2011.txt", header = T)
wrankjul2010 <- read.table("fivb_world_ranking_27-Jul-2010.txt", header = T)

# dodajmo jim datume
wrankoct2011$Date <- "20111002"
wrankjan2012$Date <- "20120104"
wrankjan2010$Date <- "20100115"
wrankjan2011$Date <- "20110115"
wrankjul2010$Date <- "20100727"

# zdruzimo podatke o rangih
rank <- rbind(wrankoct2011, wrankjan2012, wrankjan2010, wrankjan2011, wrankjul2010)

# uredimo podatke po datumu
rank <- rank[order(rank$Date),]
rank 


# branje podanih datotek s statistikami...

wlstand <- read.table("fivb_world_league_standings.txt", na.strings = c("-"), header = T)
wcstand <- read.table("fivb_world_cup_standings.txt", na.strings = c("-"), header = T)
wchstand <- read.table("fivb_world_championship_standings.txt", na.strings = c("-"), header = T)

wlh2hjun2010 <- read.table("fivb_world_league_head_to_head_03-Jun-2010.txt", header = T, na.strings=c("-"))
wlh2hmay2012 <- read.table("fivb_world_league_head_to_head_16-May-2012.txt", header = T, na.strings=c("-"))
wlh2hmay2011 <- read.table("fivb_world_league_head_to_head_27-May-2011.txt", header = T, na.strings=c("-"))

wch2hoct2011 <- read.table("fivb_world_cup_head_to_head_21-Oct-2011.txt", header = T, na.strings=c("-"))

wlstat2010 <- read.table("fivb_world_league_statistics_03-Jun-2010.txt", header = T, na.strings=c("-"))
wlstat2011 <- read.table("fivb_world_league_statistics_27-May-2011.txt", header = T, na.strings=c("-"))
wlstat2012 <- read.table("fivb_world_league_statistics_16-May-2012.txt", header = T, na.strings=c("-"))




#############################################################################################
#
# Oblikujmo ucno mnozico
#
#############################################################################################

poisciRangirneTocke <- function(Drzava, Datum, RankPodatki)
{
    # poisci vse vrstice, ki ustrezajo izbrani drzavi in so starejsi od podanega datuma
    izbira <- which(RankPodatki$Country == Drzava & RankPodatki$Date < Datum)

    # zanima nas "najnovejsi" podatek izmed izbranih vrstic
    najnovejsi <- izbira[length(izbira)]

    # vrni rang ekipe (stevilo tock)
    RankPodatki$Points[najnovejsi] 
}


oblikujUcnoVrstico <- function(tekma, rankPodatki)
{
    ekipi <- strsplit(as.character(tekma["Teams"]), "-")
    ekipi <- unlist(ekipi)

    rezultat <- strsplit(as.character(tekma["Result"]), "-")
    rezultat <- unlist(rezultat)

    rang.tockeA <- poisciRangirneTocke(ekipi[1], tekma["Date"], rankPodatki)
    rang.tockeB <- poisciRangirneTocke(ekipi[2], tekma["Date"], rankPodatki)
    
    if (rezultat[1] > rezultat[2])
        zmagovalec <- "A"
    else
        zmagovalec <- "B"

    c(tekma["Tournament"],tekma["Date"], rang.tockeA, rang.tockeB, zmagovalec)
} 

oblikujUcnoMnozico <- function(tekme, rank)
{
    ucna <- apply(tekme, 1, oblikujUcnoVrstico, rank)
    ucna <- t(ucna)
    ucna <- as.data.frame(ucna)

    names(ucna) <- c("Tournament", "Date", "RankPtsA", "RankPtsB", "Winner")

    ucna$Tournament <- as.factor(ucna$Tournament)
    ucna$Date <- as.character(ucna$Date)
    ucna$RankPtsA <- as.numeric(as.character(ucna$RankPtsA))
    ucna$RankPtsB <- as.numeric(as.character(ucna$RankPtsB))
    ucna$Winner <- as.factor(ucna$Winner)

    ucna
}

ucna <- oblikujUcnoMnozico(tekme, rank)
ucna
summary(ucna)




#########################################################################################################
#
# Bolj prakticen nacin oblikovanja ucne mnozice (sicer ni najbolj v duhu programiranja v Rju, toda...)
#
#########################################################################################################

vrniEkipe <- function(tekme, vrniEkipoA)
{
    ekipe <- vector()

    for (i in 1:nrow(tekme))
    {
        par <- as.character(tekme$Teams[i])
        par <- strsplit(par, "-")
        par <- unlist(par)

        if (vrniEkipoA)
            ekipe[i] <- par[1]
        else
            ekipe[i] <- par[2]
    }

    ekipe
}

vrniRangirneTocke <- function(ekipe, datumi, rangPodatki)
{
    tocke <- vector()

    for (i in 1:length(ekipe))
        tocke[i] <- poisciRangirneTocke(ekipe[i], datumi[i], rangPodatki)

    tocke
}

vrniZmagovalce <- function(tekme)
{
    zmagovalci <- vector()

    for (i in 1:nrow(tekme))
    {
        rezultat <- as.character(tekme$Result[i])
        rezultat <- strsplit(rezultat, "-")
        rezultat <- unlist(rezultat)

        if (rezultat[1] > rezultat[2])
            zmagovalci[i] <- "A"
        else
            zmagovalci[i] <- "B"
    }

    zmagovalci
}

turnirji <- tekme$Tournament
datumi <- tekme$Date

ekipeA <- vrniEkipe(tekme, T)
ekipeB <- vrniEkipe(tekme, F)

rangTockeA <- vrniRangirneTocke(ekipeA, datumi, rank)
rangTockeB <- vrniRangirneTocke(ekipeB, datumi, rank)

zmagovalci <- vrniZmagovalce(tekme)

ucna <- data.frame(Tournament = turnirji, Date=datumi, RankPtsA = rangTockeA, RankPtsB = rangTockeB, Winner = zmagovalci)
ucna$Date <- as.character(ucna$Date)
ucna
summary(ucna)


# ucno mnozico lahko shranimo v datoteko (za poznejso rabo)
write.table(ucna, "tekme.klas.dat", col.names=T, row.names = F)




#############################################################################################################
#
# Zdaj, ko imamo ucno mnozico, lahko zacnemo z ucenjem modela za napovedovanje zmagovalca pred zacetkom tekme 
#
#############################################################################################################


ucna <- read.table("tekme.klas.dat", header = T)
summary(ucna)



# lahko zgradimo odlocitveno drevo
library(CORElearn)
dt <- CoreModel(Winner ~ RankPtsA + RankPtsB, ucna, model = "tree")
plot(dt, ucna)



# kako bomo testirali model?

#
# Za vsak datum:
#    - zgradimo model na podlagi tekem, ki so odigrane pred tem datumom
#    - testiramo model na tekmah, ki so odigrane na ta datum
#

# zgradimo vektor z datumi (brez ponavljanja)
datumi <- unique(ucna$Date)
datumi

testiranje <- function(formula, podatki, model = "tree", skip = 5)
{
    # preberimo ime odvisne spremenljivke iz formule
    razred <- all.vars(formula)[1]

    praviClass <- vector()
    napovediClass <- vector()
    napovediProb <- vector()
    

    # zgradimo vektor z datumi (brez ponavljanja)
    datumi <- unique(podatki$Date)

    # prvih nekaj datumov spustimo, da bi se na zacetku ucili iz vsaj nekaj primerov
    for (i in (skip+1):length(datumi))
    {
        dejanska.ucna <- podatki[podatki$Date < datumi[i],]
        dejanska.testna <- podatki[podatki$Date == datumi[i],]

        cm <- CoreModel(formula, dejanska.ucna, model = model)
        
        praviClass <- c(praviClass, dejanska.testna[,razred])
        napovediClass <- c(napovediClass, predict(cm, dejanska.testna, type = "class"))
        napovediProb <- rbind(napovediProb, predict(cm, dejanska.testna, type = "prob"))
    }

    res <- list(Pravi = praviClass, Napovedi = napovediClass, Verjetnosti = napovediProb)
    res
}

# pri ucenju ne potrebujemo atributov "Tournament" in "Date"
rezultat <- testiranje(Winner ~ RankPtsA + RankPtsB, ucna, model="tree")
rezultat


t <- table(rezultat$Pravi, rezultat$Napovedi)
t

# klasifikacijska tocnost
KlasifikacijskaTocnost <- function(Rezultat)
{
    t <- table(Rezultat$Pravi, Rezultat$Napovedi)
    sum(diag(t))/sum(t)
}

KlasifikacijskaTocnost(rezultat)

#tocnost vecinskega razreda
pravi.t <- table(rezultat$Pravi)
max(pravi.t)/sum(pravi.t)


# OK, nas model se je nekaj ze naucil!


# pri napovedovanju sportnih tekmah je Brier score pomembnejsa mera od tocnosti
BrierjevaMera <- function(Rezultat)
{
    praveVerjetnosti <- cbind(as.numeric(Rezultat$Pravi == 1), as.numeric(Rezultat$Pravi == 2))
    sum((praveVerjetnosti - Rezultat$Verjetnosti)^2)/nrow(praveVerjetnosti) 
}

# vrednost Brierjeve mere
BrierjevaMera(rezultat)





# poskusimo s naivnim Bayesom
rezultat <- testiranje(Winner ~ RankPtsA + RankPtsB, ucna, model="bayes")
KlasifikacijskaTocnost(rezultat)
BrierjevaMera(rezultat)




# sprostimo pomnilnik...
destroyModels()








#
# Dodali bomo atribut: zmagovalec prejsnje tekme istih tekmecev (ne glede na turnir)
# 

vrniPrejsnjeZamgovalce <- function(Tekme)
{
    ekipeA <- vrniEkipe(Tekme, T)
    ekipeB <- vrniEkipe(Tekme, F)
    
    zmagovalci <- vrniZmagovalce(Tekme)
    
    prejsnjiZmagovalci <- vector()

    for (i in 1:length(ekipeA))
    {
        # poiscemo vse tekme oblike A-B ali B-A, ki so odigrane pred opazovano tekmo
        izbira <- which(((ekipeA == ekipeA[i] & ekipeB == ekipeB[i]) | (ekipeA == ekipeB[i] & ekipeB == ekipeA[i])) & Tekme$Date < Tekme$Date[i])   

        if (length(izbira) > 0)
            prejsnjiZmagovalci <- c(prejsnjiZmagovalci, zmagovalci[izbira[length(izbira)]])
        else
            prejsnjiZmagovalci <- c(prejsnjiZmagovalci, "N")
    }

    prejsnjiZmagovalci
}


prejsnjiZmagovalci <- vrniPrejsnjeZamgovalce(tekme)

# dodajmo novi stolpec
ucna <- cbind(ucna, PrevWinner = prejsnjiZmagovalci)
summary(ucna) 


# ocenimo atribute
attrEval(Winner ~ ., ucna, "MDL")
attrEval(Winner ~ ., ucna, "InfGain")

# kaze, da dodani atribut ni prevec informativen

rezultat <- testiranje(Winner ~ RankPtsA + RankPtsB + PrevWinner, ucna, model = "tree")
KlasifikacijskaTocnost(rezultat)
BrierjevaMera(rezultat)

# tocnost se je znizala, dodani atribut ni pomagal...



# kaj pa naivni Bayes?
rezultat <- testiranje(Winner ~ RankPtsA + RankPtsB + PrevWinner, ucna, model="bayes")
KlasifikacijskaTocnost(rezultat)
BrierjevaMera(rezultat)

# pri NB modelu je nizja klas. tocnost toda brierjeva mera je boljsa...


# sprostimo pomnilnik...
destroyModels()




#
# Dodajmo atribut: trenutna forma ekip, ki je delez zmag na zadnjih n-tih tekmah
#

vrniDelezZmag <- function(Tekme, N=3)
{
    ekipeA <- vrniEkipe(Tekme, T)
    ekipeB <- vrniEkipe(Tekme, F)
    
    zmagovalci <- vrniZmagovalce(Tekme)
    
    delezZmagEkipA <- vector()
    delezZmagEkipB <- vector()


    for (i in 1:length(ekipeA))
    {
        for (e in c("A", "B"))
        {
            if (e == "A")
            {
                #poiscemo tekme ekipe A
                izbira <- which((ekipeA == ekipeA[i] | ekipeB == ekipeA[i]) & Tekme$Date < Tekme$Date[i])   
            }
            else
            {
                #poiscemo tekme ekipe B
                izbira <- which((ekipeA == ekipeB[i] | ekipeB == ekipeB[i]) & Tekme$Date < Tekme$Date[i])   
            }

            #izberemo samo zadnjih N tekem
            if (length(izbira) > N)
                izbira <- izbira[-(1:(length(izbira)-N))]
        
            if (length(izbira))
                delezZmag <- sum(zmagovalci[izbira] == e) / length(izbira)
            else
                delezZmag <- 0

            if (e == "A")
                delezZmagEkipA[i] <- delezZmag
            else
                delezZmagEkipB[i] <- delezZmag  
        }
    }

    list(WinRatioA = delezZmagEkipA, WinRatioB = delezZmagEkipB) 
}

delezZmag <- vrniDelezZmag(tekme)
delezZmag



# dodajmo nova stolpca
ucna <- cbind(ucna, delezZmag)
summary(ucna) 


# ocenimo atribute
attrEval(Winner ~ ., ucna, "MDL")
attrEval(Winner ~ ., ucna, "InfGain")

rezultat <- testiranje(Winner ~ RankPtsA + RankPtsB + WinRatioA + WinRatioB, ucna, model = "tree")
KlasifikacijskaTocnost(rezultat)
BrierjevaMera(rezultat)

# tocnost je se vedno nizja kot na samem zacetku...

# kaj pa naivni Bayes?
rezultat <- testiranje(Winner ~ RankPtsA + RankPtsB + WinRatioA + WinRatioB, ucna, model="bayes")
KlasifikacijskaTocnost(rezultat)
BrierjevaMera(rezultat)

# z novima atributoma je NB model postal boljsi od drevesa!


# to je to, treba je poskusiti z razlicnimi atributi in modeli in izbrati najboljsega...


# sprostimo pomnilnik...
destroyModels()






###########################################################################################################
#
# Poglejmo nekoliko spremenjen ucni problem: kaj pa, ce vemo rezultat prvega niza? 
# Ali to spremeni tocnost napovedovanja?
#
###########################################################################################################

# dodali bomo zmagovalca prvega niza
# opozorilo: s tem spreminjamo ucni problem - taksne dodatne informacije ne morejo biti atributi 
# pri napovedovanju zmagovalca pred zacetkom tekme!


vrniZmagovalcePrvegaNiza <- function(tekme)
{
    zmagovalci <- vector()

    for (i in 1:nrow(tekme))
    {
        rezultat <- as.character(tekme$Set1[i])
        rezultat <- strsplit(rezultat, "-")
        rezultat <- unlist(rezultat)

        if (rezultat[1] > rezultat[2])
            zmagovalci[i] <- "A"
        else
            zmagovalci[i] <- "B"
    }

    zmagovalci
}

zmagPrvegaNiza <- vrniZmagovalcePrvegaNiza(tekme)

# dodajmo novi stolpec
ucna <- cbind(ucna, FirstSetWinner = zmagPrvegaNiza)
summary(ucna)


rezultat <- testiranje(Winner ~ RankPtsA + RankPtsB + WinRatioA + WinRatioB + FirstSetWinner, ucna, model="bayes")
KlasifikacijskaTocnost(rezultat)
BrierjevaMera(rezultat)

#
# Logicno, ce poznamo zmagovalca prvega niza je nekoliko lazje napovedati koncnega zmagovalca...
#

#
# Lahko dodate se zmagovalca drugega niza, pa primerjate rezultate (za koliko se izboljsa tocnost modela, izrisete graf...)
#



##########################################################################################################
#
# Regresijski problem
#
##########################################################################################################

# zelimo napovedati razliko v dobljenih nizih iz perspektive prve ekipe 

# sestavimo dataset

datumi <- tekme$Date
ekipeA <- vrniEkipe(tekme, T)
ekipeB <- vrniEkipe(tekme, F)
rangTockeA <- vrniRangirneTocke(ekipeA, datumi, rank)
rangTockeB <- vrniRangirneTocke(ekipeB, datumi, rank)


vrniRezultate <- function(tekme)
{
    rezultati <- vector()

    for (i in 1:nrow(tekme))
    {
        nizi <- as.character(tekme$Result[i])
        nizi <- strsplit(nizi, "-")
        nizi <- unlist(nizi)

        rezultati[i] <- as.numeric(nizi[1]) - as.numeric(nizi[2])
    }

    rezultati
}


rezultati <- vrniRezultate(tekme)

ucnaReg <- data.frame(Date=datumi, RankPtsA = rangTockeA, RankPtsB = rangTockeB, Result = rezultati)
ucnaReg$Date <- as.character(ucnaReg$Date)
ucnaReg
summary(ucnaReg)



testiranjeReg <- function(formula, podatki, model = "regTree", skip = 5)
{
    # preberimo ime odvisne spremenljivke iz formule
    razred <- all.vars(formula)[1]

    praviRezultati <- vector()
    napovedaniRezultati<- vector()  

    # zgradimo vektor z datumi (brez ponavljanja)
    datumi <- unique(podatki$Date)

    # prvih nekaj datumov spustimo, da bi se na zacetku ucili iz vsaj nekaj primerov
    for (i in (skip+1):length(datumi))
    {
        dejanska.ucna <- podatki[podatki$Date < datumi[i],]
        dejanska.testna <- podatki[podatki$Date == datumi[i],]

        cm <- CoreModel(formula, dejanska.ucna, model = model)
        
        praviRezultati <- c(praviRezultati, dejanska.testna[,razred])
        napovedaniRezultati <- c(napovedaniRezultati, predict(cm, dejanska.testna))
    }

    res <- list(Pravi = praviRezultati, Napovedi = napovedaniRezultati)
    res
}

# pri ucenju ne potrebujemo atributov "Date"
rezultatReg <- testiranjeReg(Result ~ RankPtsA + RankPtsB, ucnaReg, model="regTree")
rezultatReg

# srednja kvadraticna napaka
mse <- mean((rezultatReg$Pravi - rezultatReg$Napovedi)^2)
mse

# napaka modela, ki napoveduje srednjo vrednost iz ucne mnozice
napaka.triv.modela <- mean((rezultatReg$Pravi - mean(ucnaReg$Result))^2)
napaka.triv.modela

# relativna srednja kvadraticna napaka (dejansko je to samo njen priblizek, zaradi "koracnega" postopka testiranja)
mse/napaka.triv.modela

# ker je vrednost < 1 lahko sklepamo, da se je model nekaj naucil...

# sedaj bi bilo potrebno dodajati nove atribute in testirati druge modele v iskanju najboljsega....


