from selenium import webdriver
from selenium.webdriver.edge.options import Options
import random
from typing import Optional


class DriverManager:
    """Gestionnaire du driver Edge avec options anti‑détection renforcées"""

    # Quelques User‑Agents Chromium/Edge réalistes et récents
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
    ]

    @staticmethod
    def _build_options() -> Options:
        """Construit un objet Options prêt pour le stealth."""
        options = Options()

        # ▶ Mode headless moderne ("new") si souhaité
      
        options.add_argument("--headless=new")

        # ▶ Arguments anti‑détection
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # ▶ User‑Agent aléatoire
        options.add_argument(f"--user-agent={random.choice(DriverManager.USER_AGENTS)}")

        # ▶ Locale / Langue
        options.add_argument("--lang=fr-FR")

        # ▶ Perf & stabilité
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")

        # ▶ Réduction du bruit dans la console
        options.add_argument("--log-level=3")
        options.add_argument("--disable-logging")

        return options

    @staticmethod
    def _apply_stealth_scripts(driver: webdriver.Edge) -> None:
        """Injecte, le plus tôt possible, les scripts JavaScript de stealth."""
        # 1️⃣ Masquer navigator.webdriver AVANT l'exécution de scripts de la page
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(navigator, 'languages', { get: () => ['fr-FR', 'fr', 'en-US', 'en'] });
                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
            """
        })

        # 2️⃣ Double‑sécurité après le load de la page
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', { get: () => undefined })")

    @staticmethod
    def create_stealth_driver() -> Optional[webdriver.Edge]:
        """Crée un driver Edge configuré pour contourner les protections anti‑bot."""
        try:
            options = DriverManager._build_options()
            driver = webdriver.Edge(options=options)

            DriverManager._apply_stealth_scripts(driver)
            return driver

        except Exception as exc:
            print(f"❌ Erreur lors de la création du driver: {exc}")
            return None
