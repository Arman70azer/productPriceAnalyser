from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class CookieManager:
    """Gestionnaire des cookies"""
    
    @staticmethod
    def handle_cookies(driver: webdriver.Edge, timeout: int = 3) -> None:
        """Gère les bannières de cookies rapidement"""
        
        if not driver:
            print("❌ Driver non disponible pour la gestion des cookies")
            return
        
        try:
            # Sélecteurs pour refus rapide
            refuse_selectors = [
                "#W0wltc",  # ID spécifique Google
                "button:contains('Refuser')",
                "button:contains('Tout refuser')",
                "button[aria-label*='Refuser']",
                "button[id*='reject']"
            ]
            
            # Tentative de refus direct (plus rapide)
            for selector in refuse_selectors:
                try:
                    refuse_btn = WebDriverWait(driver, 1).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    refuse_btn.click()
                    print("❌ Cookies refusés rapidement")
                    return
                except:
                    continue
            
            # Fallback: chercher "Gérer" puis refuser
            manage_selectors = [
                "button:contains('Gérer')",
                "button[aria-label*='Gérer']"
            ]
            
            for selector in manage_selectors:
                try:
                    manage_btn = WebDriverWait(driver, 1).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    manage_btn.click()
                    time.sleep(0.2)  # Attente minimale
                    
                    # Refuser dans la popup
                    final_btn = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button:contains('Tout refuser')"))
                    )
                    final_btn.click()
                    print("❌ Cookies refusés via popup")
                    return
                except:
                    continue
                    
        except:
            print("ℹ️ Pas de bannière cookies ou timeout")