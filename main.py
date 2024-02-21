import json
import os
import sys

from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget
from functools import partial

SAVE_DIR = os.path.dirname(__file__)
SAVE_FILE = f"{SAVE_DIR}\contacts_list.json"

contacts_list = []

if  os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as element:
        contacts_list = json.load(element)
else :
    with open(SAVE_FILE, "w") as element:
        json.dump(contacts_list, element)
             
        
class MainWindow(QWidget) :
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRM")
        self.resize(700,400)
        
        self.main_layout = QHBoxLayout(self)
        self.left_layout = QVBoxLayout(self)
        self.right_layout = QVBoxLayout(self)
        
        
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)
    
        
        self.lbl_contacts = QLabel("Liste des contacts")
        self.list_contacts = QListWidget()
        self.left_layout.addWidget(self.lbl_contacts)
        self.left_layout.addWidget(self.list_contacts)
        
        
        self.btn_create = QPushButton("Nouveau contact")
        self.btn_modification = QPushButton("Modifier le contact")
        self.btn_search = QPushButton("Rechercher un contact")
        self.btn_del = QPushButton("Supprimmer le contact")
        self.right_layout.addWidget(self.btn_create)
        self.right_layout.addWidget(self.btn_modification)
        self.right_layout.addWidget(self.btn_search)
        self.right_layout.addWidget(self.btn_del)
        
        self.Display_contacts_list(self.list_contacts)
                 
        self.btn_create.clicked.connect(self.Contact_Creation)
        self.btn_modification.clicked.connect(self.Contact_Modification)
        self.btn_search.clicked.connect(self.Contact_Search)
        self.btn_del.clicked.connect(self.Contact_Delete)
        
            
    def Contact_Creation(self):
        """ fonction qui ferra apparaitre une fenêtre avec les champs à remplir pour la création du nouveau contact """
        
        self.creation_window = CreateModifWindow("Création de contact",self.list_contacts)
        self.creation_window.show()
        
        
        
    def Contact_Modification(self):
        """Fontion qui fera apparaitre une fenêtre avec les élements actuels du contact avec la possibilité de les modifiés"""
        
        self.creation_window = CreateModifWindow("Modification du contact", self.list_contacts)
        self.creation_window.show()
    
    def Contact_Search(self):
        """ fonction qui ferra apparaitre une fenêtre qui permet d'afficher seulement les contacts qui contiennent la valeur saisie par l'utilisateur"""
        
        self.research_window = ResearchWindow("Recherche de contact")
        self.research_window.show()
    
    def Contact_Delete(self):
        """Fonction qui supprimme le contact sélectionner dans la liste"""
        
        self.item = self.list_contacts.currentItem()
        del contacts_list[self.list_contacts.row(self.item)]
        self.list_contacts.takeItem(self.list_contacts.row(self.item))
        MainWindow.Display_contacts_list(self, self.list_contacts)
    
    
    def Display_contacts_list(self, widget_list: QListWidget):
        """Fonction qui sert à afficher la listes des contacts dans le QlistWidget"""
        
        self.widget_list = widget_list

        self.widget_list.clear()
        contacts_list.sort()
        
        for i in contacts_list:
            self.widget_list.addItem(f"{i[0]}  {i[1]} ---- {i[2]} ---- {i[3]}")
    
    
class CreateModifWindow(QWidget):
    
    def __init__(self, title, widget_list: QListWidget ):
          
        super().__init__()
        self.title = title
        self.widget_list = widget_list
        self.item = widget_list.currentItem()
        self.modification_autorisation = False
        self.setWindowTitle(self.title)
        self.setFixedSize(500, 150)
        
        self.cmw_main_layout = QHBoxLayout(self)
        self.cmw_left_layout = QVBoxLayout(self)
        self.cmw_right_layout = QVBoxLayout(self)
        
        
        self.cmw_main_layout.addLayout(self.cmw_left_layout)
        self.cmw_main_layout.addLayout(self.cmw_right_layout)
        
        self.lbl_name = QLabel("Nom :")
        self.lbl_lastname = QLabel("Prénom :")
        self.lbl_mail = QLabel("Mail :")
        self.lbl_phone = QLabel("Tel :")
        
        if self.title == "Création de contact":
            self.le_name = QLineEdit()
            self.le_lastname = QLineEdit()
            self.le_mail = QLineEdit()
            self.le_phone = QLineEdit()
        else:
            self.le_name = QLineEdit(contacts_list[self.widget_list.row(self.item)][0])
            self.le_lastname = QLineEdit(contacts_list[self.widget_list.row(self.item)][1])
            self.le_mail = QLineEdit(contacts_list[self.widget_list.row(self.item)][2])
            self.le_phone = QLineEdit(contacts_list[self.widget_list.row(self.item)][3])
            self.modification_autorisation = True
        
        self.btn_validation = QPushButton("Valider")
        self.btn_exit = QPushButton("Quitter")
        
        self.cmw_left_layout.addWidget(self.lbl_name)
        self.cmw_left_layout.addWidget(self.lbl_lastname)
        self.cmw_left_layout.addWidget(self.lbl_mail)
        self.cmw_left_layout.addWidget(self.lbl_phone)
        self.cmw_left_layout.addWidget(self.btn_exit)
        
        self.cmw_right_layout.addWidget(self.le_name)
        self.cmw_right_layout.addWidget(self.le_lastname)
        self.cmw_right_layout.addWidget(self.le_mail)
        self.cmw_right_layout.addWidget(self.le_phone)
        self.cmw_right_layout.addWidget(self.btn_validation)
        
        
        self.btn_validation.clicked.connect(partial(self.Validation, self.le_name, self.le_lastname, self.le_mail, self.le_phone))
        self.btn_exit.clicked.connect(self.Exit)
               
    def Validation(self, user_name: QLineEdit, user_lastname: QLineEdit, user_mail: QLineEdit, user_phone: QLineEdit):
        """Fonction qui récupere les informations dans les champs pour créer le contact et l'ajouter à la liste de contacts.
           En cas de modification de contact, il supprimera l'ancien contact avant d'ajouter le contact modifié """
        
        self.le_user_name = user_name
        self.le_user_lastname = user_lastname
        self.le_user_mail = user_mail
        self.le_user_phone = user_phone
        
        self.user_name = user_name.text().upper()
        self.user_lastname = user_lastname.text().title()
        self.user_mail = user_mail.text()
        self.user_phone = user_phone.text()
        
        if self.modification_autorisation:
            
            del contacts_list[self.widget_list.row(self.item)]
            self.widget_list.takeItem(self.widget_list.row(self.item))
            
            
        self.new_contact = [self.user_name,self.user_lastname,self.user_mail,self.user_phone]
        contacts_list.append(self.new_contact)
        MainWindow.Display_contacts_list(self, self.widget_list)
        self.close()
             
    
    def Exit(self):
        self.close()


class ResearchWindow(QWidget):
    
    def __init__(self, title):
          
        super().__init__()
        self.title = title
        self.setWindowTitle(self.title)
        self.setFixedSize(500,300)
    
        self.rw_main_layout = QVBoxLayout(self)
        
        self.lbl_research = QLabel("Saisissez votre recherche :")
        self.le_user_research = QLineEdit("...")
        self.btn_research = QPushButton("Validez la recherche")
        self.list_user_research = QListWidget()
        
        self.rw_main_layout.addWidget(self.lbl_research)
        self.rw_main_layout.addWidget(self.le_user_research)
        self.rw_main_layout.addWidget(self.btn_research)
        self.rw_main_layout.addWidget(self.list_user_research)
        
        self.btn_research.clicked.connect(partial(self.User_research, self.le_user_research, self.list_user_research))
        
    def User_research(self, research_value:QLineEdit, list_display:QListWidget) :
        """Fonction qui va afficher que les elements qui contiennent la recherche utilisateur"""
        self.research_value = research_value.text().lower()
        self.list_display = list_display
        self.lower_contacts_list = []
        
        
        for i in contacts_list:
            self.lower_contacts_list.append([elem.lower() for elem in i])
                
        self.counter = -1
        
        self.list_display.clear()
        for i in self.lower_contacts_list :
            self.counter += 1
            if self.research_value in i[0]:
                self.list_display.addItem(f"{contacts_list[self.counter][0]}  {contacts_list[self.counter][1]} ---- {contacts_list[self.counter][2]} ---- {contacts_list[self.counter][3]}")

            elif self.research_value in i[1]:
                self.list_display.addItem(f"{contacts_list[self.counter][0]}  {contacts_list[self.counter][1]} ---- {contacts_list[self.counter][2]} ---- {contacts_list[self.counter][3]}")
 
            elif self.research_value in i[2]:
                self.list_display.addItem(f"{contacts_list[self.counter][0]}  {contacts_list[self.counter][1]} ---- {contacts_list[self.counter][2]} ---- {contacts_list[self.counter][3]}")
                
            elif self.research_value in i[3]:
                self.list_display.addItem(f"{contacts_list[self.counter][0]}  {contacts_list[self.counter][1]} ---- {contacts_list[self.counter][2]} ---- {contacts_list[self.counter][3]}")    
            
           
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
app.exec()

with open(SAVE_FILE, "w") as element:
	    json.dump(contacts_list, element, indent=4, ensure_ascii=False)



