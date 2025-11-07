# tests_chatbot.py
from chatbot_tfidf import repondre

cas = {
 "bonjour": "Salut",
 "Qui ES-tu ?": "Je suis un petit chatbot",
 "peux tu me faire une blague": "Pourquoi les programmeurs",
 "il est quelle heure": "Il est",
 "j'aimerais de l'aide sur le projet": "Ce projet illustre"
}

ok, ko = 0, 0
for question, attendu in cas.items():
 rep = repondre(question)
 if attendu.lower() in rep.lower():
  ok += 1
  print("[OK] ", question, "->", rep)
 else:
  ko += 1
  print("[KO] ", question, "->", rep, "(attendu contient:", attendu, ")")

print(f"\nRésumé: {ok} OK / {ok+ko} tests")