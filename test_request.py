import sqlite3

conn = sqlite3.connect('Database/Stockage.db')
cursor = conn.cursor()

query = "INSERT INTO produits (id, Code_reference,nom_produit, composition, quantite, prix_achat, prix_vente, marge, date_expiration, date_ajout) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"