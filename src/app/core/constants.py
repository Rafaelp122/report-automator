from pathlib import Path

# Base directories
ROOT_DIR = Path(__file__).parent.parent.parent.parent
SRC_DIR = ROOT_DIR / "src"
LOG_DIR = ROOT_DIR / "logs"
DATA_DIR = ROOT_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
ASSETS_DIR = ROOT_DIR / "assets"
STYLES_DIR = SRC_DIR / "app" / "ui" / "styles"

# Ensure directories exist
for directory in [LOG_DIR, INPUT_DIR, OUTPUT_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# File names
DEFAULT_CONFIG_PATH = ROOT_DIR / "config.toml"
APP_LOG_PATH = LOG_DIR / "app.log"
DEFAULT_TEMPLATE_PATH = ASSETS_DIR / "template.xlsx"
