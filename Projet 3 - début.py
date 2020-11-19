from sense_hat import SenseHat
from time import sleep


class Affichage:

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
    
    def __str__(self):
        return self.affichage()
    
class Message(Affichage):
    
    def __init__(self):
        super().__init__()
        self.message = ""
    
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
                                                
        self.showCount()
        messageDone = False
        while messageDone == False:
            event = self.sense().stick.wait_for_event()
            while event.direction == "left":
                event = self.sense().stick.wait_for_event()
            if event.direction == "up" and event.action == "released":
                self.incrementCount()
                self.showCount()
            elif event.direction == "down" and event.action == "released":
                self.decreaseCount()
                self.showCount()
            elif event.direction == "middle" and event.action == "pressed":
                self.showCountColor([255, 0, 0])
                sleep(0.1)
                self.showCount()
                self.message += str(self.affichage)
            elif event.direction == "right" and event.action == "released":
                if not(len(self.message) == 0):
                    self.sense().show_message(self.message)
                    self.sense().show_message("R -> Save")
                    self.sense().show_message("L -> Erase")
                    newEvent = self.sense().stick.wait_for_event()
                    while newEvent.direction == "up" or newEvent.direction == "down":
                        newEvent = self.sense().stick.wait_for_event()
                    if newEvent.direction == "right":
                        self.sense().show_message("Saved")
                        self.writeMessageToFile("message.txt")
                        messageDone = True
                    elif newEvent.direction == "left":
                        self.sense().show_message("Erased")
                        self.clearMessage()
                        self.resetCount()
                        sleep(0.1)
                        self.showCount()
                else:
                    self.sense().show_message("Empty")
                    self.showCount()

    def writeMessageToFile(self, filename):
        """
        pre: filename est une chaine de caractères qui correspond à un fichier texte
        post: écrit le message encodé (attention: à faire une fois qu'on a cryptographie.py) dans le fichier filename avec le hash du mot de passe
        """
        f = open(filename, "w")
        f.write(self.message)
        # Ici, il faudra faire attention à ENCODER le message avant de l'inscrire dans le fichier!
        # Pour l'instant, je n'écris que le message décodé (on n'a pas cryptographie.py)
        f.close()
    
    def messageExists(self, filename):
        """
        pre: filename est une chaine de caractères qui correspond à un fichier texte
        post: renvoie True si le fichier existe, et False s'il ne contient aucune ligne ou s'il n'existe pas
        """
        try:
            f = open(filename, "r")
            lines = f.readlines()
            if len(lines) == 0:
                return False
            return True
        except FileNotFoundError:
            return False
    
    def destroyFile(self, filename):
        """
        pre: filename est une chaine de caractères qui correspond à un fichier texte
        post: détruit le fichier s'il existe et renvoie True, False autrement
        """
        if messageExists(filename) == True:
            from os import remove
            remove(filename)
            return True
        return False
    
    def readFile(self, filename):
        """
        pre: filename est une chaîne de caractères correspondant à un fichier texte
        post: renvoie les lignes se trouvant dans le fichier, et False si le fichier n'existe pas.
        """
        if self.messageExists(filename) == False:
            return False
        else:
            f = open(filename, "r")
            lines = f.readlines()
            # Les données dans le fichier sont stockées de la manière suivante:
            # MESSAGE HASHPASSWORD
            return lines
    
    def checkPasswordHash(self, filename, password):
        """
        pre: filename est une chaîne de caractères qui correspond à un fichier texte
             password est une chaîne de caractères
        post: si le hash de password est identique à celui stocké dans le fichier filename, renvoyer True.  False autrement
        """
        lines = self.readFile(filename)
        # Quand on aura le fichier cryptographie.py de l'assistant on pourra compléter ce bout de code.
    
    def decodeMessage(self, password):
        # Quand on aura le fichier cryptographie.py de l'assistant on pourra compléter ce bout de code.
        """
        pre: password est une chaîne de caractères
        post: renvoie le message décodé selon la méthode d'encodage du fichier cryptographie.py
        """
        pass
    
    def __str__(self):
        return self.message

mess = Message()
mess.askMessage()
