# chatbot_tfidf.py
import unicodedata
import string
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

FAQ = {
 "bonjour": "Salut ! Comment puis-je t’aider ?",
 "qui es tu": "Je suis un petit chatbot en Python 🤖",
 "aide": "Tu peux me demander l’heure, une blague, ou des infos sur ce projet.",
 "comment ca va": "Super, merci ! Et toi ?",
 "aide projet": "Ce projet illustre un mini chatbot basé sur similarité + quelques règles."
}
#dico
SYNOS = {"salut": "bonjour", "coucou": "bonjour", "hello": "bonjour"}


def normaliser_texte(t: str) -> str:
 # 1) minuscules
 t = t.lower()
 # 2) supprimer accents
 t = unicodedata.normalize("NFKD", t)
 t = "".join(ch for ch in t if not unicodedata.combining(ch))
 # 3) enlever ponctuation simple
 t = t.translate(str.maketrans("", "", string.punctuation))
 # 4) trim espaces
 t = " ".join(t.split())
 return t

# --- 1) Construire le "corpus" des intentions (clés de la FAQ) normalisées
intentions = list(FAQ.keys())
intentions_norm = [normaliser_texte(x) for x in intentions] #liste de ttes mes clés faq normalisées
# --- 2) Vectoriseur TF-IDF (avec un petit prétraitement)
vectorizer = TfidfVectorizer( # vectorizer contient une instance d'objet quel'on configure (analyzer...)
 analyzer="word",
 ngram_range=(1, 2), # unigrammes + bigrammes aident pour "qui es"
 min_df=1, # garder tous les termes
)
# Ajuster le vocabulaire sur les intentions de la FAQ
X_intentions = vectorizer.fit_transform(intentions_norm) # shape: (n_intents, vocab_size)


def log_incomprehension(message, suggestions):
  """Enregistre les messages non compris dans un fichier log."""
  with open("chatbot_log.txt", "a", encoding="utf-8") as f:
    f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
      f"Message: {message} | Suggestions: {suggestions}\n")

 
 
def repondre(message: str) -> str:
 
 m_norm = normaliser_texte(message)

 # Remplacement des synonymes 
 for k, v in SYNOS.items():
   m_norm = m_norm.replace(k, v)

 # Règles "prioritaires"
 if "blague" in m_norm:
  return "Pourquoi les programmeurs confondent Halloween et Noël ? Parce que OCT 31 == DEC 25."
 if "heure" in m_norm:
  return "Il est " + datetime.now().strftime("%H:%M")
 
 # --- 3) Vectoriser le message utilisateur et comparer
 X_msg = vectorizer.transform([m_norm]) # shape: (1, vocab_size) ex : [[1.0, 0.0, 0.0, 0.0]]
 sims = cosine_similarity(X_msg, X_intentions)[0] # shape: (n_intents,)
 # Trouver la meilleure intention
 idx_best = sims.argmax()
 score = sims[idx_best]
 best_intent = intentions[idx_best]
 # --- 4) Seuil de confiance
 if score >= 0.25:
  return FAQ[best_intent]
 candidats = sorted(zip(sims, intentions), reverse=True)[:3] #Réponses “fallback” intelligentes
 suggest = ", ".join(i for _, i in candidats)
 log_incomprehension(message, suggest)
 return f"Je n’ai pas compris. Tu peux essayer: {suggest}"


if __name__ == "__main__":
 print("Chatbot TF-IDF prêt. Tape 'exit' pour quitter.")
 while True:
  msg = input("> ")
  if msg.strip().lower() == "exit":
   break
  print(repondre(msg))