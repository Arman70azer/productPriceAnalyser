from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from datetime import datetime
from typing import Optional, List, Dict
import re

class ProductExtractor:
    """Classe pour extraire les informations des produits"""

    def products_detected(self, driver: WebDriver) -> int:
        """Retourne le nombre de produits détectés sur la page"""
        try:
            # Détecter les deux types de div
            type1_elements = driver.find_elements(By.CSS_SELECTOR, "div.rwVHAc.itPOE")
            type2_elements = driver.find_elements(By.CSS_SELECTOR, "div.njFjte[jsname='ZvZkAe']")
            total = len(type1_elements) + len(type2_elements)
            print(f"    Type 1: {len(type1_elements)}, Type 2: {len(type2_elements)}")
            return total
        except Exception as e:
            print(f"    ❌ Erreur détection produits: {e}")
            return 0
    
    @staticmethod
    def extract_product_info(element: WebElement) -> Optional[Dict]:
        """Extraire les informations d'un produit depuis les deux types de div"""
        try:
            class_attr = element.get_attribute("class")
            if class_attr is None:
                return None
            
            if "rwVHAc itPOE" in class_attr:
                return ProductExtractor._extract_type1(element)
            elif "njFjte" in class_attr:
                return ProductExtractor._extract_type2(element)
            else:
                return None
        except Exception:
            return None

    
    @staticmethod
    def _extract_type1(element: WebElement) -> Optional[Dict]:
        """Extraction pour div.rwVHAc.itPOE"""
        product_info = {}
        
        try:
            # Titre
            title_selectors = ["span.pymv4e", "a.plantl span", "div.RnJeZd span"]
            product_info['title'] = ProductExtractor._find_text_by_selectors(element, title_selectors)
            
            if product_info['title'] == "N/A":
                try:
                    link_element = element.find_element(By.CSS_SELECTOR, "a.plantl")
                    aria_label = link_element.get_attribute("aria-label")
                    if aria_label:
                        product_info['title'] = aria_label
                except:
                    pass
            
            # Prix
            price_selectors = ["span.e10twf", "div.T4OwTb span"]
            product_info['price'] = ProductExtractor._find_text_by_selectors(element, price_selectors)
            
            # Vendeur
            seller_selectors = ["span.zPEcBd.VZqTOd", "div.LbUacb span"]
            product_info['seller'] = ProductExtractor._find_text_by_selectors(element, seller_selectors)
            
            if product_info['seller'] == "N/A":
                try:
                    seller_element = element.find_element(By.CSS_SELECTOR, "span[aria-label*='Vendu par']")
                    aria_label = seller_element.get_attribute("aria-label")
                    if aria_label:
                        match = re.search(r'Vendu par\s+(.+)', aria_label)
                        if match:
                            product_info['seller'] = match.group(1)
                except:
                    pass
            
            # Note
            rating_selectors = ["span[aria-label*='Note']", "span.z3HNkc"]
            rating_text = ProductExtractor._find_attribute_by_selectors(element, rating_selectors, 'aria-label')
            if rating_text != "N/A":
                match = re.search(r'Note\s*:\s*([0-9,\.]+)', rating_text)
                if match:
                    product_info['rating'] = match.group(1)
                else:
                    product_info['rating'] = rating_text
            else:
                product_info['rating'] = "N/A"
            
            # Nombre d'avis
            reviews_selectors = ["span.RDApEe.YrbPuc"]
            product_info['reviews_count'] = ProductExtractor._find_text_by_selectors(element, reviews_selectors)
            
            # Lien
            link_selectors = ["a.plantl", "a[data-impdclcc]"]
            product_info['link'] = ProductExtractor._find_attribute_by_selectors(element, link_selectors, 'href')
            
            # État
            condition_selectors = ["div.OkcyVb.PPi4nd.XyaVue.bHWJj"]
            product_info['condition'] = ProductExtractor._find_text_by_selectors(element, condition_selectors)
            
            # Frais de port
            shipping_text = "N/A"
            try:
                shipping_elements = element.find_elements(By.CSS_SELECTOR, "div.OkcyVb.PPi4nd.XyaVue.bHWJj")
                for elem in shipping_elements:
                    text = elem.text.strip()
                    if "frais de port" in text.lower() or "€" in text:
                        shipping_text = text
                        break
            except:
                pass
            product_info['shipping'] = shipping_text
            
            # Spécifications
            specs_selectors = ["div.OCkIVb.r4L8M"]
            specs_text = ProductExtractor._find_text_by_selectors(element, specs_selectors)
            product_info['specifications'] = specs_text
            product_info['specs_dict'] = ProductExtractor._parse_specifications(specs_text)
            
            # Image
            image_selectors = ["img[src*='shopping']", "img[alt*='iPhone']", "img"]
            product_info['image'] = ProductExtractor._find_attribute_by_selectors(element, image_selectors, 'src')
            
            # Type
            product_info['div_type'] = "type1"
            product_info['scraped_at'] = datetime.now().isoformat()
            
            return product_info if product_info.get('title') != "N/A" else None
            
        except Exception as e:
            print(f"    ❌ Erreur extraction type1: {e}")
            return None
    
    @staticmethod
    def _extract_type2(element: WebElement) -> Optional[Dict]:
        """Extraction pour div.njFjte[jsname='ZvZkAe'] depuis aria-label"""
        product_info = {}
        
        try:
            # Récupérer l'aria-label complet
            aria_label = element.get_attribute("aria-label")
            if not aria_label:
                return None
            
            # Parsing de l'aria-label
            # Format: "Apple iPhone 13. Prix actuel : 329,98 €. Plus de prix disponibles. Electro Dépôt et plus. En magasin. Note : 4,7 sur 5. 68 k avis."
            
            # Titre (première partie avant le premier point)
            title_match = re.search(r'^([^.]+)', aria_label)
            if title_match:
                product_info['title'] = title_match.group(1).strip()
            else:
                product_info['title'] = "N/A"
            
            # Prix
            price_match = re.search(r'Prix actuel\s*[:\s]*([0-9,\.\s]+€)', aria_label)
            if price_match:
                product_info['price'] = price_match.group(1).strip()
            else:
                product_info['price'] = "N/A"
            
            # Vendeur (partie avant "En magasin" ou "Note")
            seller_match = re.search(r'disponibles\.\s*([^.]+?)\s*(?:En magasin|Note)', aria_label)
            if seller_match:
                seller_text = seller_match.group(1).strip()
                if "et plus" in seller_text:
                    seller_text = seller_text.replace(" et plus", "").strip()
                product_info['seller'] = seller_text
            else:
                product_info['seller'] = "N/A"
            
            # Note
            rating_match = re.search(r'Note\s*[:\s]*([0-9,\.]+)', aria_label)
            if rating_match:
                product_info['rating'] = rating_match.group(1).strip()
            else:
                product_info['rating'] = "N/A"
            
            # Nombre d'avis
            reviews_match = re.search(r'([0-9]+\s*[kK]?\+?)\s*avis', aria_label)
            if reviews_match:
                product_info['reviews_count'] = reviews_match.group(1).strip()
            else:
                product_info['reviews_count'] = "N/A"
            
            # Disponibilité
            if "En magasin" in aria_label:
                product_info['availability'] = "En magasin"
            else:
                product_info['availability'] = "N/A"
            
            # Lien (essayer de trouver un lien dans l'élément parent ou enfant)
            try:
                parent = element.find_element(By.XPATH, "..")
                link_element = parent.find_element(By.CSS_SELECTOR, "a[href]")
                product_info['link'] = link_element.get_attribute("href")
            except:
                product_info['link'] = "N/A"
            
            # Image
            try:
                img_element = element.find_element(By.CSS_SELECTOR, "img")
                product_info['image'] = img_element.get_attribute("src")
            except:
                product_info['image'] = "N/A"
            
            # Champs par défaut pour ce type
            product_info['condition'] = "N/A"
            product_info['shipping'] = "N/A"
            product_info['specifications'] = "N/A"
            product_info['specs_dict'] = {}
            
            # Type
            product_info['div_type'] = "type2"
            product_info['scraped_at'] = datetime.now().isoformat()
            
            return product_info if product_info.get('title') != "N/A" else None
            
        except Exception as e:
            print(f"    ❌ Erreur extraction type2: {e}")
            return None

    @staticmethod
    def _parse_specifications(specs_text: str) -> Dict[str, str]:
        """Parse les spécifications techniques en dictionnaire"""
        specs_dict = {}
        
        if specs_text == "N/A" or not specs_text:
            return specs_dict
            
        try:
            specs_parts = [part.strip() for part in specs_text.split(" · ")]
            
            for spec in specs_parts:
                if ":" in spec:
                    key, value = spec.split(":", 1)
                    specs_dict[key.strip()] = value.strip()
                elif spec:
                    if "GO" in spec.upper():
                        specs_dict["Stockage"] = spec
                    elif "PO" in spec.upper():
                        specs_dict["Taille écran"] = spec
                    elif "IOS" in spec.upper():
                        specs_dict["OS"] = spec
                    elif "5G" in spec.upper():
                        specs_dict["Connectivité"] = spec
                    elif "MP" in spec.upper():
                        specs_dict["Caméra"] = spec
                    elif spec in ["Noir", "Blanc", "Rouge", "Bleu", "Vert", "Violet", "Rose"]:
                        specs_dict["Couleur"] = spec
                    elif "iPhone" in spec:
                        specs_dict["Modèle"] = spec
                    else:
                        specs_dict[f"Spec_{len(specs_dict)}"] = spec
                        
        except Exception as e:
            print(f"    ⚠️ Erreur parsing spécifications: {e}")
            
        return specs_dict

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