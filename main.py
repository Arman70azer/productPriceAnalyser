import time
import requests
from scraper.scraper import GoogleShopping


class Utils:
    """Utilitaires divers"""
    
    @staticmethod
    def check_ip() -> None:
        """Vérifier l'IP actuelle"""
        try:
            response = requests.get("https://httpbin.org/ip", timeout=5)
            print(f"IP actuelle: {response.json()['origin']}")
        except:
            print("Impossible de vérifier l'IP")


def main():
    """Fonction principale optimisée"""
    print("🚀 Démarrage du scraping rapide...")
    start_time = time.time()
    
    Utils.check_ip()
    
    scraper = GoogleShopping()
    results = scraper.scrape_product("Apple+iPhone+13+noir+128GB")
    
    end_time = time.time()
    print(f"⏱️ Temps d'exécution: {end_time - start_time:.2f} secondes")
    print("✅ Scraping terminé")
    
    return results


if __name__ == "__main__":
    main()