#!/usr/bin/env python3
"""
Analyseur de prix de produits par image et description
Utilise la recherche d'images et le web scraping pour trouver des prix moyens
"""

import requests
import re
import statistics
from typing import List, Dict, Optional, Union
from dataclasses import dataclass
import base64
from bs4 import BeautifulSoup
import urllib.parse
from enum import Enum

class StateProduct(Enum):
    """État du produit pour l'analyse"""
    RECONDITIONNE = "reconditionné"
    NEUF = "neuf"
    OCCASION = "occasion"
    NULL = "inconnu"


@dataclass
class ProductInfo:
    name: str
    image_url: str = ""
    color: str = ""
    brand: str = ""
    category: str = ""
    additional_keywords: Optional[List[str]] = None
    state = StateProduct.NULL


@dataclass
class PriceResult:
    price: float
    currency: str
    source: str
    title: str
    url: str

@dataclass
class AnalysisResult:
    product: str
    search_query: str
    total_results: int
    valid_prices: int
    average_price: float
    median_price: float
    min_price: float
    max_price: float
    price_range: str
    source_averages: Dict[str, float]
    all_prices: List[float]
    currency: str

@dataclass
class ErrorResult:
    error: str

class ProductPriceAnalyzer:
    def __init__(self) -> None:
        self.headers: Dict[str, str] = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session: requests.Session = requests.Session()
        self.session.headers.update(self.headers)
        
    def encode_image_to_base64(self, image_url: str) -> str:
        """Encode une image en base64 pour l'API"""
        try:
            response: requests.Response = self.session.get(image_url, timeout=10)
            response.raise_for_status()
            return base64.b64encode(response.content).decode('utf-8')
        except Exception as e:
            print(f"Erreur lors de l'encodage de l'image: {e}")
            return ""
        
    def extraire_sponso(self, soup: BeautifulSoup) -> List[PriceResult]:
        """Extrait les résultats sponsorisés de la page Google Shopping"""
        results: List[PriceResult] = []
        
        # Recherche des éléments contenant les informations de prix
        for item in soup.select('.sh-dlr__list-result'):
            title: str = item.select_one('.sh-dlr__title').get_text(strip=True)
            price_str: str = item.select_one('.sh-dlr__price').get_text(strip=True)
            url: str = item.select_one('a')['href']
            
            
            price_match = re.search(r'(\d+[\.,]?\d*)', price_str)
            if price_match:
                price: float = float(price_match.group(1).replace(',', '.'))
                results.append(PriceResult(price=price, currency='EUR', source='Google Shopping', title=title, url=url))
        
        return results
    
    def search_google_shopping(self, query: str, max_results: int = 10) -> List[PriceResult]:
        """Recherche sur Google Shopping (simulation)"""
        results: List[PriceResult] = []
        
       
        encoded_query: str = urllib.parse.quote(query)
        url: str = f"https://www.google.com/search?tbm=shop&q={encoded_query}&hl=fr&gl=fr"
        
        try:
            response: requests.Response = self.session.get(url, timeout=15)
            response.raise_for_status()
            soup: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')
            
            res = extraire_sponso(soup)
                    
        except Exception as e:
            print(f"Erreur lors de la recherche Google Shopping: {e}")
            
        return results
    
    
    
    def create_search_query(self, product_info: ProductInfo) -> str:
        """Crée une requête de recherche optimisée"""
        query_parts: List[str] = []
        
        if product_info.brand:
            query_parts.append(product_info.brand)
        
        query_parts.append(product_info.name)
        
        if product_info.color:
            query_parts.append(product_info.color)
        
        if product_info.category:
            query_parts.append(product_info.category)
        
        if product_info.additional_keywords:
            query_parts.extend(product_info.additional_keywords)
        
        return " ".join(query_parts)
    
    def _is_valid_url(self, url: str) -> bool:
        """Vérifie si une URL est valide"""
        try:
            parsed = urllib.parse.urlparse(url)
            return bool(parsed.netloc and parsed.scheme in ('http', 'https'))
        except Exception:
            return False
    
    def filter_outliers(self, prices: List[float]) -> List[float]:
        """Filtre les prix aberrants"""
        if len(prices) < 3:
            return prices
        
        mean: float = statistics.mean(prices)
        std_dev: float = statistics.stdev(prices)
        
        # Garde les prix dans 2 écarts-types de la moyenne
        filtered: List[float] = [p for p in prices if abs(p - mean) <= 2 * std_dev]
        
        return filtered if filtered else prices
    
    def analyze_product_price(self, product_info: ProductInfo) -> Union[AnalysisResult, ErrorResult]:
        """Analyse le prix d'un produit à partir d'une URL d'image et d'une description"""
        
        print(f"Analyse du produit: {product_info.name}")
        print(f"Image URL: {product_info.image_url}")
        
        if product_info.image_url and not self._is_valid_url(product_info.image_url):
            return ErrorResult(error=f"URL d'image invalide: {product_info.image_url}")
        
        if product_info.image_url:
            try:
                response: requests.Response = self.session.head(product_info.image_url, timeout=10)
                response.raise_for_status()
                
                # Vérification du type de contenu
                content_type: str = response.headers.get('content-type', '').lower()
                if not content_type.startswith('image/'):
                    return ErrorResult(error=f"L'URL ne pointe pas vers une image: {product_info.image_url}")
                    
            except Exception as e:
                print(f"Avertissement: Impossible de vérifier l'image: {e}")
        
        search_query: str = self.create_search_query(product_info)
        print(f"Requête de recherche: {search_query}")
        
        all_results: List[PriceResult] = []
        
        # Recherche sur différentes plateformes
        print("Recherche sur Google Shopping...")
        google_results: List[PriceResult] = self.search_google_shopping(search_query)
        all_results.extend(google_results)
        
    
        if not all_results:
            return ErrorResult(error="Aucun prix trouvé")
        
        prices: List[float] = [result.price for result in all_results]
        
        filtered_prices: List[float] = self.filter_outliers(prices)
        
        if not filtered_prices:
            return ErrorResult(error="Aucun prix valide après filtrage")
        
        # Calcul des statistiques
        average_price: float = statistics.mean(filtered_prices)
        median_price: float = statistics.median(filtered_prices)
        min_price: float = min(filtered_prices)
        max_price: float = max(filtered_prices)
        
        # Groupement par source
        sources: Dict[str, List[float]] = {}
        for result in all_results:
            if result.source not in sources:
                sources[result.source] = []
            sources[result.source].append(result.price)
        
        source_averages: Dict[str, float] = {}
        for source, prices_list in sources.items():
            source_averages[source] = statistics.mean(prices_list)
        
        return AnalysisResult(
            product=product_info.name,
            search_query=search_query,
            total_results=len(all_results),
            valid_prices=len(filtered_prices),
            average_price=round(average_price, 2),
            median_price=round(median_price, 2),
            min_price=round(min_price, 2),
            max_price=round(max_price, 2),
            price_range=f"{round(min_price, 2)} - {round(max_price, 2)} €",
            source_averages={k: round(v, 2) for k, v in source_averages.items()},
            all_prices=filtered_prices,
            currency="EUR"
        )

def main() -> None:
    """Fonction principale d'exemple"""
    analyzer = ProductPriceAnalyzer()
    
    # Exemple d'utilisation
    product = ProductInfo(
        name="iPhone 13",
        image_url="https://th.bing.com/th/id/OPEC.2wPMU3bm7vFoNA474C474?w=128&h=188&o=6&bw=6&bc=ffffff&pid=21.1g",
        color="noir",
        brand="Apple",
        category="",
        additional_keywords=["128GB"]
    )
    
    # Analyse du prix
    result: Union[AnalysisResult, ErrorResult] = analyzer.analyze_product_price(product)
    
    if isinstance(result, ErrorResult):
        print(f"Erreur: {result.error}")
    else:
        print("\n=== RÉSULTATS DE L'ANALYSE ===")
        print(f"Produit: {result.product}")
        print(f"Requête utilisée: {result.search_query}")
        print(f"Nombre de résultats: {result.total_results}")
        print(f"Prix moyen: {result.average_price} €")
        print(f"Prix médian: {result.median_price} €")
        print(f"Fourchette de prix: {result.price_range}")
        print("\nPrix moyens par source:")
        for source, avg_price in result.source_averages.items():
            print(f"  {source}: {avg_price} €")

if __name__ == "__main__":
    main()