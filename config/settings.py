import os
import logging
from dotenv import load_dotenv

# Carrega os itens do dotenv
load_dotenv()

# Variáveis de ambiente
NOME_DA_PLANILHA = os.getenv("NOME_DA_PLANILHA")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Mapeamento de colunas
COLUMN_OFFSET = {
    'entrada': 1,
    'saida': 2,
    'diario': 3,
    'saldo': 4
}

# Configuração de logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)
