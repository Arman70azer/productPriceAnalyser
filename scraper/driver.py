from selenium import webdriver
from selenium.webdriver.edge.options import Options
import random
from typing import Optional

class DriverManager:
    """Gestionnaire du driver avec options anti-détection"""
    
    @staticmethod
    def create_stealth_driver() -> Optional[webdriver.Edge]:
        """Crée un driver Edge avec des options pour éviter la détection"""
        
        try:
            options = Options()
            
            # Mode headless optimisé
            options.add_argument("--headless=new")
            
            # Options anti-détection
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # User-Agent aléatoire
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52"
            ]
            options.add_argument(f"--user-agent={random.choice(user_agents)}")
            
            # Optimisations de performance
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-extensions")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-images")  # Désactiver les images pour plus de vitesse
            options.add_argument("--disable-javascript")  # Désactiver JS non essentiel
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-java")
            
            # Désactiver les logs
            options.add_argument("--log-level=3")
            options.add_argument("--disable-logging")
            
            # Créer le driver
            driver = webdriver.Edge(options=options)
            
            # Scripts anti-détection
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_script("""
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['fr-FR', 'fr', 'en-US', 'en']
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
            """)
            
            return driver
            
        except Exception as e:
            print(f"❌ Erreur lors de la création du driver: {e}")
            return None