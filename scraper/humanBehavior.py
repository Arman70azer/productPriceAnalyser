from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

class HumanBehavior:
    """Simulation de comportement humain optimisée"""
    
    @staticmethod
    def quick_human_actions(driver: webdriver.Edge) -> None:
        """Actions humaines rapides et discrètes"""
        
        if not driver:
            print("❌ Driver non disponible pour les actions humaines")
            return
        
        try:
            # Mouvement de souris minimal
            actions = ActionChains(driver)
            actions.move_by_offset(random.randint(5, 50), random.randint(5, 50))
            actions.perform()
            
            # Scroll minimal
            driver.execute_script(f"window.scrollTo(0, {random.randint(50, 150)});")
            
            # Pause très courte
            time.sleep(random.uniform(0.1, 0.3))
        except Exception as e:
            print(f"⚠️ Erreur dans les actions humaines: {e}")

    @staticmethod
    def minimal_wait() -> None:
        """Attente minimale entre les actions"""
        time.sleep(random.uniform(0.2, 0.5))