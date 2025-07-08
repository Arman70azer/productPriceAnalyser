from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from datetime import datetime
from typing import Optional, List, Dict

class ProductExtractor:
    """Classe pour extraire les informations des produits"""
    
    @staticmethod
    def extract_product_info(element: WebElement) -> Optional[Dict]:
        """Extraire les informations d'un produit iPhone"""
        
        product_info = {}
        
        try:
            # Titre du produit
            title_selectors = [
                "div.gkQHve", "h3.tAxDx", "div.tAxDx", "span.tAxDx",
                "div[role='heading']", "h4", "a[href*='shopping']"
            ]
            
            product_info['title'] = ProductExtractor._find_text_by_selectors(element, title_selectors)
            
            # Prix
            price_selectors = [
                "span.lmQWe", "span.pVBUqb", "span.T14wmb", "div.T14wmb",
                "span[aria-label*='€']", "span[aria-label*='euros']"
            ]
            
            product_info['price'] = ProductExtractor._find_text_by_selectors(element, price_selectors)
            
            # Vendeur
            seller_selectors = [
                "span.WJMUdc", "div.WJMUdc", "span.aULzUe", "div.aULzUe",
                "span[aria-label*='vendeur']", "div.merchant"
            ]
            
            product_info['seller'] = ProductExtractor._find_text_by_selectors(element, seller_selectors)
            
            # Note/Évaluation
            rating_selectors = [
                "span.yi40Hd", "span.Rsc7Yb", "div.yi40Hd",
                "span[aria-label*='étoiles']", "span[aria-label*='stars']"
            ]
            
            product_info['rating'] = ProductExtractor._find_text_by_selectors(element, rating_selectors)
            
            # Lien du produit
            link_selectors = [
                "a[href*='shopping']", "a[href*='url']", "a[data-ved]"
            ]
            
            product_info['link'] = ProductExtractor._find_attribute_by_selectors(element, link_selectors, 'href')
            
            # Image du produit
            image_selectors = [
                "img[src*='shopping']", "img[alt*='iPhone']", "img[alt*='iphone']", "img.rISBZc"
            ]
            
            product_info['image'] = ProductExtractor._find_attribute_by_selectors(element, image_selectors, 'src')
            
            # Disponibilité/Stock
            availability_selectors = [
                "span.Y4TKme", "div.Y4TKme", "span[aria-label*='disponible']",
                "span[aria-label*='stock']"
            ]
            
            product_info['availability'] = ProductExtractor._find_text_by_selectors(element, availability_selectors)
            
            # Livraison
            delivery_selectors = [
                "span.vEjMR", "div.vEjMR", "span[aria-label*='livraison']",
                "span[aria-label*='delivery']"
            ]
            
            product_info['delivery'] = ProductExtractor._find_text_by_selectors(element, delivery_selectors)
            
            # Timestamp
            product_info['scraped_at'] = datetime.now().isoformat()
            
            return product_info if product_info.get('title') else None
            
        except Exception as e:
            print(f"    ❌ Erreur extraction: {e}")
            return None

    @staticmethod
    def _find_text_by_selectors(element: WebElement, selectors: List[str]) -> str:
        """Trouve le texte en utilisant une liste de sélecteurs"""
        for selector in selectors:
            try:
                found_element = element.find_element(By.CSS_SELECTOR, selector)
                text = found_element.text.strip()
                if text:
                    return text
            except:
                continue
        return "N/A"

    @staticmethod
    def _find_attribute_by_selectors(element: WebElement, selectors: List[str], attribute: str) -> str:
        """Trouve un attribut en utilisant une liste de sélecteurs"""
        for selector in selectors:
            try:
                found_element = element.find_element(By.CSS_SELECTOR, selector)
                attr_value = found_element.get_attribute(attribute)
                if attr_value:
                    return attr_value
            except:
                continue
        return "N/A"