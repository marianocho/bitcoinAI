from dataclasses import dataclass
from pathlib import Path
import os, yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

@dataclass
class Settings:
    data_dir: Path = ROOT / "data"
    config_path: Path = ROOT / "config.yaml"
    openai_key: str | None = os.getenv("OPENAI_API_KEY")
    app_lang: str = os.getenv("APP_LANG", "pt")

    def yaml(self) -> dict:
        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

SETTINGS = Settings()
SETTINGS.data_dir.mkdir(parents=True, exist_ok=True)