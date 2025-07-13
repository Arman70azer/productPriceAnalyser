# Google Shopping Scraper

Un scraper Python rapide et optimisé pour extraire des informations de produits depuis Google Shopping avec des techniques anti-détection avancées.

## 🚀 Fonctionnalités

- **Scraping rapide** : Optimisé pour la vitesse avec des timeouts courts
- **Anti-détection** : Utilise des techniques de stealth pour éviter les blocages
- **Extraction complète** : Récupère titre, prix, vendeur, notes, avis, liens et spécifications
- **Gestion automatique** : Cookies, captcha et comportement humain simulé
- **Support multi-types** : Gère différents formats d'affichage de Google Shopping
- **Multi-plateformes** : En initialisant le GoogleShopping, vous pouvez choisir votre navigateur (edge, firefox, chrome)

## 📦 Structure du projet

```
google-shopping-scraper/
├── main.py              # Exemple d'utilisation
├── googleShop.py        # Classe principale du scraper
└── lib/
    ├── driver.py        # Gestionnaire du driver Edge avec stealth
    ├── extractor.py     # Extraction des données produits
    ├── cookie.py        # Gestion des bannières cookies
    └── humanBehavior.py # Simulation de comportement humain
```

## 🔧 Installation

### Prérequis
- Python 3.7+
- Microsoft Edge installé
- EdgeDriver (téléchargeable depuis [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/))

### Dépendances
```bash
pip install selenium
```

## 📋 Utilisation

### Exemple basique

```python
from googleShop import GoogleShopping

# Créer une instance du scraper
scraper = GoogleShopping("edge")

# Scraper des produits (remplacer les espaces par des '+')
results = scraper.scrape_product("Apple+iPhone+13+noir+128GB")

# Afficher les résultats
for product in results:
    print(f"Titre: {product['title']}")
    print(f"Prix: {product['price']}")
    print(f"Vendeur: {product['seller']}")
    print(f"Note: {product['rating']}")
    print("-" * 50)
```

### Exemple avec mesure de performance

```python
import time
from googleShop import GoogleShopping

def main():
    print("🚀 Démarrage du scraping...")
    start_time = time.time()
    
    scraper = GoogleShopping()
    results = scraper.scrape_product("Apple+iPhone+13+noir+128GB")
    
    end_time = time.time()
    print(f"⏱️ Temps d'exécution: {end_time - start_time:.2f} secondes")
    print(f"📦 Produits trouvés: {len(results)}")
    
    return results

if __name__ == "__main__":
    main()
```

## 📊 Format des données

Chaque produit retourné contient les champs suivants :

```python
{
    'title': str,              # Nom du produit
    'price': str,              # Prix (format: "XXX,XX €")
    'seller': str,             # Nom du vendeur
    'rating': str,             # Note (format: "X,X")
    'reviews_count': str,      # Nombre d'avis
    'link': str,              # Lien vers le produit
    'condition': str,         # État du produit
    'shipping': str,          # Frais de port
    'specifications': str,    # Spécifications techniques
    'specs_dict': dict,       # Spécifications parsées
    'image': str,             # URL de l'image
    'div_type': str,          # Type d'élément HTML ("type1" ou "type2")
    'scraped_at': str,        # Timestamp de scraping
    'availability': str       # Disponibilité (type2 uniquement)
}
```

## ⚙️ Configuration

### Options du driver (driver.py)

- **Mode headless** : Activé par défaut pour plus de vitesse
- **User-Agents rotatifs** : Utilise des UA Edge/Chrome récents
- **Anti-détection** : Masque les signaux d'automatisation

### Personnalisation des timeouts

```python
# Dans cookie.py - Modifier le timeout des cookies
CookieManager.handle_cookies(driver, timeout=5)  # 5 secondes au lieu de 3
```

## 🛡️ Fonctionnalités anti-détection

1. **Stealth Driver** : Masque `navigator.webdriver` et autres signaux
2. **User-Agents réalistes** : Rotation d'UA Edge/Chrome récents
3. **Comportement humain** : Mouvements de souris et scrolling aléatoires
4. **Gestion des cookies** : Acceptation/refus automatique des bannières
5. **Détection de captcha** : Arrêt automatique si captcha détecté

## 🐛 Debug et dépannage

En cas d'erreur, le scraper génère automatiquement :
- `debug_page.html` : Code source de la page
- `debug_screenshot.png` : Capture d'écran

### Messages d'erreur courants

- `❌ Impossible de créer le driver` : Vérifier l'installation d'EdgeDriver
- `⚠️ Captcha détecté` : Attendre avant de relancer
- `❌ Aucun iPhone trouvé` : Vérifier la requête de recherche

## 🔍 Exemples de requêtes

```python
# Recherche spécifique
"Apple+iPhone+13+noir+128GB"

# Recherche générale
"iPhone+13"

# Avec marque et modèle
"Samsung+Galaxy+S21"

# Avec spécifications
"MacBook+Pro+M1+512GB"
```

## ⚠️ Limitations

- **Respect des robots.txt** : Utiliser de manière responsable
- **Rate limiting** : Éviter les requêtes trop fréquentes
- **Captcha** : Peut apparaître en cas d'usage intensif
- **Évolution Google** : Les sélecteurs peuvent changer

---

⚡ **Astuce** : Pour de meilleures performances, utilisez des requêtes spécifiques avec le format `marque+modèle+spécifications`.