import time
from googleShop import GoogleShopping

# Exemple d'utilisation optimisé
def main():
    """Point d'entrée principal pour le scraping rapide de Google Shopping"""
    print("🚀 Démarrage du scraping rapide...")
    start_time = time.time()
    
    scraper = GoogleShopping("edge")
    results = scraper.scrape_product("Apple+iPhone+13+noir+128GB")
    
    end_time = time.time()
    print(f"⏱️ Temps d'exécution: {end_time - start_time:.2f} secondes")
    print("✅ Scraping terminé")
    
    return results


if __name__ == "__main__":
    main()