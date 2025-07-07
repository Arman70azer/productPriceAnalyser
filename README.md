# 🔍 Analyseur de Prix Google – Comparateur de Produits

Ce projet est un **analyseur de prix automatisé** pour un produit donné, capable d'extraire les **offres sponsorisées** affichées par Google (Shopping Ads). Il vous permet de comparer rapidement les prix, vendeurs, frais de livraison et autres informations clés pour un produit spécifique.

WARNING !!! EN COURS DE DEVELOPEMENT...

---

## 🚀 Fonctionnalités

- 🛒 Analyse des résultats sponsorisés Google Shopping
- 💬 Extraction automatique des données utiles :
  - Titre du produit
  - Prix affiché
  - Vendeur
  - Frais de livraison (s'il y en a)
  - Lien vers la page du vendeur
  - Image du produit
- 📦 Idéal pour surveiller les prix d’un produit dans le temps

---

## 📷 Aperçu

Exemple de résultat extrait :

```json
{
  "titre": "iPhone 13 128 Go - Reconditionné",
  "prix": "309,99 €",
  "vendeur": "CertiDeal",
  "livraison": "+ 5,90 € de frais de port",
  "lien": "https://certideal.com/iphone-13-reconditionne/iphone-13-128-go-lumiere-stellaire-6844",
  "image": "https://example.com/image.jpg"
}

