# Projet "MagicLock" réalise par Saatci Ari, Rixen Thomas, Tellez Sanclemente Mateo, Zanet Ionut Andrei

from sense_hat import SenseHat
from time import sleep
from file import *
from crypto import *

class Affichage:
    
    # Le but de cette classe est de mettre en place les fonctions d'affichage des chiffres
    # ainsi que d'initialiser le SenseHat
    
    count = 0
    s = SenseHat()
    def __init__(self):
        self.affichage = Affichage.count
        self.__sense = Affichage.s
    
    def sense(self):
        return self.__sense
    
    def incrementCount(self):
      
        """
        pre: aucun
        post: modifie le message à afficher à l'écran (+1)
        """
        if Affichage.count == 9:
            Affichage.count = 0
        else:
            Affichage.count += 1
        self.affichage = Affichage.count
        
    def decreaseCount(self):
        """
        pre: aucun
        post: modifie le message à afficher à l'écran (-1)
        """
        if Affichage.count == 0:
            Affichage.count = 9
        else:
            Affichage.count -= 1
        self.affichage = Affichage.count
    
    def resetCount(self):
        """
        pre: aucun
        post: réinitialise le compte à 0
        """
        Affichage.count = 0
        self.affichage = Affichage.count
        
    def showCount(self):
        """
        pre: aucun
        post: affiche le compte à l'écran
        """
        self.sense().show_letter(str(self.affichage))
    
    def showCountColor(self, color):
        """
        pre: color est une liste d'entiers [R, G, B] ou R, G et B sont des valeurs comprises entre 0 et 255 pour les couleurs rouges, vertes et bleues respectivement
        post: affiche le compte à l'écran de couleur color
        """
        self.sense().show_letter(str(self.affichage), text_colour=color)
    
class MagicLock(Affichage):
    
    # Cette classe contient la majorité des fonctions relatives au MagicLock
    # 1) Message
        # - Demander le message
        # - Effacer le message
    # 2) Code
        # - Demander le code
        # - Effacer le code
    # 3) Sécurité
        # - Encoder le message
        # - Hacher le mot de passe
    # 4) Fichier
        # - Vérifier si le fichier existe déjà
        # - Détruire le fichier
        # - Écrire le message encodé et le mot de passe hashé dans ce fichier
        # - Récupérer les infos du fichier
    
    
    def __init__(self):
        super().__init__()
        self.message = ""
        self.password = ""
    
    
    ###############
    #   MESSAGE   #
    ###############
    
    
    def clearMessage(self):
        self.message = ""
    
    def askMessage(self):
        """
        pre: aucun
        post: demande à l'utilisateur d'entrer son message.
            1) l'interface lui affiche un chiffre.
                UP = augmenter le chiffre de 1
                DOWN = diminuer le chiffre de 1
                MIDDLE = ajouter ce chiffre au message
                RIGHT = passer à la vérification du message
            2) une fois que l'utilisateur est à la vérification du message, il a deux choix
                RIGHT = stocker le message
                LEFT = recommencer à écrire le message
            3) une fois qu'il fait right deux fois d'affilée, le message est stocké.
        """
        self.sense().show_message("Enter Message", 0.05)                                        
        self.showCount()
        messageDone = False
        while messageDone == False:
            event = self.sense().stick.wait_for_event(emptybuffer=True)
            while event.direction == "left":
                self.sense().show_message("U/D/M/R", 0.05)
                event = self.sense().stick.wait_for_event()
            if event.direction == "up" and event.action == "released":
                self.incrementCount()
                self.showCount()
            elif event.direction == "down" and event.action == "released":
                self.decreaseCount()
                self.showCount()
            elif event.direction == "middle" and event.action == "pressed":
                # Feedback visuel pour indiquer que le chiffre a été ajouté
                self.showCountColor([255, 0, 0])
                sleep(0.1)
                self.showCount()
                self.message += str(self.affichage)
            elif event.direction == "right" and event.action == "released":
                if not(len(self.message) == 0):
                    self.sense().show_message(self.message, 0.05)
                    self.sense().show_message("L = Del R = Save", 0.05)
                    newEvent = self.sense().stick.wait_for_event()
                    while newEvent.direction == "up" or newEvent.direction == "down" or newEvent.direction == "middle":
                        self.sense().show_message("L/R", 0.05)
                        newEvent = self.sense().stick.wait_for_event()
                    if newEvent.direction == "right":
                        self.sense().show_message("Saved", 0.05)
                        messageDone = True
                    elif newEvent.direction == "left":
                        self.sense().show_message("Erased", 0.05)
                        self.clearMessage()
                        self.resetCount()
                        sleep(0.1)
                        self.showCount()
                else:
                    self.sense().show_message("Empty", 0.05)
                    self.showCount()
                    
                    
    ############
    #   CODE   #
    ############
    
    
    def clearPassword(self):
        self.password = ""
    
    def askPassword(self):
        """
        pre: aucun
        post: permet d'enregister le code (suite de positions Z, Y, X arrondies en dessous avec la fonction int()).
                RIGHT = confirmer le code
                    -> RIGHT = sauvegarder le code
                    -> LEFT = effacer le code et recommencer
                MIDDLE = ajouter les positions actuelles au code
        """
        self.sense().show_message("Enter Password", 0.05)                                    
        passwordDone = False
        while passwordDone == False:
            event = self.sense().stick.wait_for_event(emptybuffer=True)
            while event.direction == "up" or event.direction == "left" or event.direction == "down":
                self.sense().show_message("M/R", 0.05)
                event = self.sense().stick.wait_for_event()
            if event.direction == "middle" and event.action == "pressed":
                orientation = self.sense().get_orientation()
                pitch = int(orientation["pitch"])
                roll = int(orientation["roll"])
                yaw = int(orientation["yaw"])
                positions = [pitch, roll, yaw]
                for pos in range(len(positions)):
                    for x in range(5):
                        if positions[pos] >= 90*(x-1) and positions[pos] <= 90*x:
                            positions[pos] = x
                for i in positions:
                    self.password += str(i)
                self.sense().show_letter("S") # S pour Saved
                sleep(0.1)
                self.sense().clear() 
            elif event.direction == "right" and event.action == "released":
                if not(len(self.password) == 0):
                    self.sense().show_message("L = Del R = Save", 0.05)
                    newEvent = self.sense().stick.wait_for_event()
                    while newEvent.direction == "up" or newEvent.direction == "down" or newEvent.direction == "middle":
                        self.sense().show_message("L/R", 0.05)
                        newEvent = self.sense().stick.wait_for_event()
                    if newEvent.direction == "right":
                        self.sense().show_message("Saved", 0.05)
                        passwordDone = True
                    elif newEvent.direction == "left":
                        self.sense().show_message("Erased", 0.05)
                        self.clearPassword()
                else:
                    self.sense().show_message("Empty", 0.05)
                    
                    
    ###############
    #   FICHIER   #
    ###############
    
    
    def messageExists(self, filename):
        """
        pre: filename est un string
        post: si le fichier filename existe, renvoie True. False autrement
        """
        return exists(filename)
    
    def destroyFile(self, filename):
        """
        pre: aucun
        post: efface le contenu de message.txt et renvoie True. False si erreur (fichier existe pas)
        """
        if self.messageExists(filename) == True:
            delete(filename)
            return True
        else:
            return False
    
    def readFile(self, filename):
        """
        pre: aucun
        post: renvoie un string contenant les données du fichier message.txt
        """
        if self.messageExists(filename) == True:
            return read(filename)
        else:
            return None
        
    def writeToFile(self):
        """
        pre: aucun
        post: renvoie True si le message encodé et le mot de passe hashé a pu être écrit dans message.txt. False autrement
        """
        
        try:
            self.encodeData()
            write("message.txt", self.message)
            write("password.txt", self.password)
            return True
        except OSError:
            return False
        
    
    ################
    #   SÉCURITÉ   #
    ################
    
    
    def encodeMessage(self):
        """
        pre: password est une chaîne de caractères qui correspond à des suites de positions dans l'espace
        post: encode le message selon la fonction encode de crypto
        """
        self.message = encode(self.password, self.message)
    
    def hashPassword(self):
        """
        pre: aucun
        post: hash le mot de passe selon la fonction hashing de crypto
        """
        self.password = hashing(self.password)
    
    def encodeData(self):
        """
        pre: aucun
        post: renvoie une ligne contenant le message encodé et le mot de passe hashé.
        """
        self.encodeMessage()
        self.hashPassword()

class DecodeMessage(MagicLock):
    
    # Cette classe permet de vérifier que le mot de passe est correct ainsi que décoder le message
    # 1) Hashing
        # - Vérifier que le hashing est correct
    # 2) Décryption
        # - Décoder le message avec le mot de passe
    # 3) Interface post-décryption
        # Permet à l'utilisateur de choisir s'il veut
            # - Détruire le message et en écrire un nouveau
            # - Conserver le message
            # - Quitter l'application
    
    def __init__(self):
        super().__init__()
        self.encodedMessage = self.readFile("message.txt")
        self.hashedPassword = self.readFile("password.txt")
        
        
    ###############
    #   Hashing   #
    ###############
    
    
    def checkHash(self):
        """
        pre: aucun
        post: vérifie si le hash de password équivaut à celui stocké dans le fichier message.txt. True si oui, False autrement
        """
        return hashing(self.password) == self.hashedPassword
    
    
    ##################
    #   Décryption   #
    ##################
    
    
    def decodeMessage(self):
        """
        pre: aucun
        post: si le hash des mot de passes est identique, décode le message selon la méthode decode de crypto et l'affiche. Renvoie None autrement
        """
        if self.checkHash() == True:
            self.message = decode(self.password, self.encodedMessage)
            self.sense().show_message(self.message, 0.05)
            return True
        else:
            self.sense().show_message("Wrong", 0.05)
            return False
        
        
    #################
    #   Interface   #
    #################
    
    
    def postDecryption(self):
        """
        pre: aucun
        post: demande à l'utilisateur ce qu'il souhaite faire après avoir décodé le message
                LEFT = effacer le message et recommencer (renvoie -1)
                RIGHT = sauvegarder le message et recommencer (renvoie 1)
                MIDDLE = quitter l'application (renvoie 0)
        """
        actionFinished = False
        self.sense().show_message("L = Del R = Save M = Exit", 0.05)
        while actionFinished == False:
            event = self.sense().stick.wait_for_event(emptybuffer=True)
            while event.direction == "up" or event.direction == "down":
                self.sense().show_message("L/M/R", 0.05)
                event = self.sense().stick.wait_for_event(emptybuffer=True)
            if event.direction == "right" and event.action == "released":
                return 1
            elif event.direction == "left" and event.action == "released":
                return -1
            elif event.direction == "middle" and event.action == "pressed":
                self.sense().show_message("Bye", 0.05)
                return 0
    
    
if __name__ == "__main__":    
    lock = MagicLock()
    if lock.messageExists("message.txt") == False or lock.messageExists("password.txt") == False:
        # si aucun message existe, alors demander un message et un code.
        lock.askMessage()
        lock.askPassword()
        lock.writeToFile()
    else:
        # demander le mot de passe
        decrypt = DecodeMessage()
        decrypt.askPassword()
        while decrypt.decodeMessage() == False:
            # tant qu'il est faux
            decrypt.clearPassword()
            decrypt.askPassword()
        after = decrypt.postDecryption()
        while after != 0:
            # voir pre/post conditions de postDecryption()
            if after == 1:
                decrypt.clearPassword()
                decrypt.askPassword()
                while decrypt.decodeMessage() == False:
                    decrypt.clearPassword()
                    decrypt.askPassword()
            elif after == -1:
                lock.destroyFile()
                lock.askMessage()
                lock.askPassword()
                lock.writeToFile()
            after = decrypt.postDecryption()

