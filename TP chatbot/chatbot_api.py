from fastapi import FastAPI
from pydantic import BaseModel
from chatbot_tfidf import repondre  # on réutilise ta fonction existante

app = FastAPI()#On crée un serveur web FastAPI

#  On définit le format attendu pour le message envoyé (texte)
class Message(BaseModel):#Message(BaseModel) = type + validation + extraction automatique depuis le JSON.
    texte: str

# Définir une route POST pour envoyer un message. Dés qu'un message est envoyé sur l'url /chatbot ca execute cette fonction.
@app.post("/chatbot")
def chatbot_endpoint(msg: Message):#Fonction qui sera appelée quand quelqu’un envoie un message
    reponse = repondre(msg.texte)
    return {"reponse": reponse}
