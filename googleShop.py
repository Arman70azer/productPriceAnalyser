from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Optional, List, Dict, Union
from lib.driver import DriverManager
from lib.extractor import ProductExtractor
from lib.cookie import CookieManager
from lib.humanBehavior import HumanBehavior

class GoogleShopping:
    """Scraper principal optimisé pour la vitesse"""

    
    def __init__(self, browser: str = "edge"):
        """Initialisation du scraper avec le navigateur choisi"""
        self.browser = browser.lower()
        if self.browser not in ["edge", "chrome", "firefox"]:
            raise ValueError("Navigateur non supporté. Utilisez 'edge', 'chrome' ou 'firefox'.")
        
        # Le driver sera initialisé lors de l'appel à scrape_product
        self.driver: Optional[WebDriver] = None
        self.results: List[Dict] = []
    
    def scrape_product(self, query: str) -> List[Dict]:
        """Scrape les produits identiques avec vitesse optimisée"""
        
        try:
            # Création du driver avec le navigateur spécifié
            self.driver = DriverManager.create_stealth_driver(browser=self.browser)
            
            if not self.driver:
                print(f"❌ Impossible de créer le driver {self.browser}")
                return []
            
            print(f"✅ Driver {self.browser} créé avec succès")
            
            # Navigation rapide vers Google Shopping
            url = f"https://www.google.com/search?q={query}&hl=fr&gl=fr&udm=28"
            self.driver.get(url)
            
            # Gestion cookies rapide
            CookieManager.handle_cookies(self.driver)
            
            # Comportement humain minimal
            HumanBehavior.quick_human_actions(self.driver)
            
            # Vérification captcha rapide
            if self._check_captcha():
                print("⚠️ Captcha détecté - Arrêt du scraping")
                return []
            
            # Extraction des produits
            self._extract_products()
            
            # Affichage des résultats
            self._display_results()
            
            return self.results
            
        except Exception as e:
            print(f"❌ Erreur générale: {e}")
            import traceback
            traceback.print_exc()
            self._save_debug_info()
            return []
        
        finally:
            if self.driver:
                self.driver.quit()
    
    def _check_captcha(self) -> bool:
        """Vérification rapide du captcha"""
        if not self.driver:
            return False
            
        try:
            self.driver.find_element(By.CSS_SELECTOR, "div[class*='captcha'], div[id*='captcha'], iframe[src*='recaptcha']")
            return True
        except:
            return False
    
    def _extract_products(self) -> None:
        """Extraction des produits des deux types"""
        if not self.driver:
            return
        
        try:
            # Récupération des deux types d'éléments
            type1_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.rwVHAc.itPOE")
            type2_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.njFjte[jsname='ZvZkAe']")
            
            all_elements = type1_elements + type2_elements
            print(f"📦 Trouvé {len(type1_elements)} type1 + {len(type2_elements)} type2 = {len(all_elements)} produits")
            
            # Extraction de chaque produit
            for element in all_elements:
                product_info = ProductExtractor.extract_product_info(element)
                if product_info and product_info.get('title') != "N/A":
                    self.results.append(product_info)
        
        except Exception as e:
            print(f"❌ Erreur extraction: {e}")
            self._save_debug_info()
    
    def _display_results(self) -> None:
        """Affichage des résultats"""
        print(f"\n📊 RÉSUMÉ: {len(self.results)} produits trouvés")
        print("="*60)
        
        if self.results:
            for i, product in enumerate(self.results, 1):
                print(f"{i}. {product.get('title', 'N/A')} - {product.get('price', 'N/A')} ({product.get('seller', 'N/A')})")
        else:
            print("❌ Aucun produit trouvé")
    
    def _save_debug_info(self) -> None:
        """Sauvegarde des informations de debug"""
        if not self.driver:
            print("🔧 Impossible de sauvegarder - driver non disponible")
            return
            
        try:
            with open("debug_page.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            self.driver.save_screenshot("debug_screenshot.png")
            print("🔧 Informations de debug sauvegardées")
        except Exception as e:
            print(f"🔧 Erreur lors de la sauvegarde debug: {e}")
    
    def change_browser(self, browser: str) -> None:
        """Change le navigateur pour les futurs scraping"""
        if browser.lower() not in ["edge", "chrome", "firefox"]:
            raise ValueError("Navigateur non supporté. Utilisez 'edge', 'chrome' ou 'firefox'.")
        
        self.browser = browser.lower()
        print(f"🔄 Navigateur changé vers: {self.browser}")
    
    def get_current_browser(self) -> str:
        """Retourne le navigateur actuellement configuré"""
        return self.browser