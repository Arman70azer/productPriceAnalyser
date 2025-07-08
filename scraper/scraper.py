from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Optional, List, Dict
from scraper.driver import DriverManager
from scraper.extractor import ProductExtractor
from scraper.cookie import CookieManager
from scraper.humanBehavior import HumanBehavior

class GoogleShopping:
    """Scraper principal optimisé pour la vitesse"""
    
    def __init__(self):
        self.driver: Optional[webdriver.Edge] = None
        self.results: List[Dict] = []
    
    def scrape_product(self, query: str) -> List[Dict]:
        """Scrape les produits identiques avec vitesse optimisée"""
        
        try:
            # Création du driver avec vérification
            self.driver = DriverManager.create_stealth_driver()
            
            if not self.driver:
                print("❌ Impossible de créer le driver")
                return []
            
            print("✅ Driver créé avec succès")
            
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
        """Extraction rapide des produits"""
        
        if not self.driver:
            print("❌ Driver non disponible pour l'extraction")
            return
        
        # Sélecteurs de produits optimisés
        product_selectors = [
            "div.UC8ZCe.QS8Cxb",
            "div[data-ved]",
            "div.sh-dgr__content",
            "div.u30d4"
        ]
        
        print("🔍 Extraction rapide des produits...")
        
        for selector in product_selectors:
            try:
                # Attente minimale pour les éléments
                elements = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                )
                
                print(f"✅ {len(elements)} éléments trouvés avec {selector}")
                
                for element in elements:
                   
                    product_info = ProductExtractor.extract_product_info(element)
                    
                    if product_info and product_info.get('title') and 'iPhone' in product_info.get('title', '').lower():
                        self.results.append(product_info)
                        print(f"Produit trouvé: {product_info.get('title', 'N/A')}")
                
                # Si on a trouvé des produits, on arrête
                if self.results:
                    break
                    
            except Exception as e:
                print(f"❌ Erreur avec {selector}: {e}")
                continue
    
    def _display_results(self) -> None:
        """Affichage des résultats"""
        print(f"\n📊 RÉSUMÉ: {len(self.results)} iPhones trouvés")
        print("="*60)
        
        if self.results:
            for i, phone in enumerate(self.results, 1):
                print(f"{i}. {phone.get('title', 'N/A')} - {phone.get('price', 'N/A')} ({phone.get('seller', 'N/A')})")
        else:
            print("❌ Aucun iPhone trouvé")
    
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