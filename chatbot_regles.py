import math
import unicodedata
import string


FAQ = {
 "bonjour": "Salut ! Comment puis-je t’aider ?",
 "qui es tu": "Je suis un petit chatbot en Python 🤖",
 "aide": "Tu peux me demander l’heure, une blague, ou des infos sur ce projet.",
 "comment ca va": "Super, merci ! Et toi ?",
 "aide projet": "Ce projet illustre un mini chatbot basé sur similarité + quelquesrègles."
}

def normaliser(texte):
 # minuscules
 t = texte.lower()
 # enlever accents
 t = unicodedata.normalize("NFKD", t)
 t = "".join(ch for ch in t if not unicodedata.combining(ch))
 # enlever ponctuation simple
 t = t.translate(str.maketrans("", "", string.punctuation))
 return t

def similarite(a, b):
 A, B = normaliser(a).split(), normaliser(b).split()  # nettoyage du texte - découpage(tokeniser)
 inter = len(set(A) & set(B)) #On transforme les listes en ensembles (pour éviter les doublons) et on calcule l’intersection, c’est-à-dire les mots communs.
 return inter / math.sqrt(len(A) * len(B)) # calcul de la similarité

def repondre(message):
 
 meilleur, score = None, 0.0

 for k in FAQ:
  s = similarite(message, k)
  if s > score:
    meilleur, score = k, s

 if score > 0.2:
  return FAQ[meilleur]
 
 if "blague" in message.lower():
  return "Pourquoi les programmeurs confondent Halloween et Noël ? Parce que OCT 31 == DEC 25."
 
 if "heure" in message.lower():
  from datetime import datetime
  return "Il est " + datetime.now().strftime("%H:%M")
 
 return "Je n’ai pas compris. Essaie de reformuler 🙂"


if __name__ == "__main__":
  print("Chatbot prêt. Tape 'exit' pour quitter.")
  while True:
   msg = input("> ")
   if msg.strip().lower() == "exit":
    break
   print(repondre(msg))
