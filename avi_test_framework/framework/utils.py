import yaml
import logging
import sys
from colorama import init, Fore

init(autoreset=True)

def load_config(config_file: str):
    try:
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: {config_file} not found")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"{Fore.RED}Error parsing {config_file}: {e}")
        sys.exit(1)

def setup_logging(level=logging.INFO):
    import os
    os.makedirs('logs', exist_ok=True)
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/test_execution.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )