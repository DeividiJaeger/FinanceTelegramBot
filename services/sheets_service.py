import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config.settings import NOME_DA_PLANILHA, logger

class SheetsService:
    def __init__(self):
        self.sheet = None
        self.client = None
        self._connect()
    
    def _connect(self):
        """Estabelece conexão com o Google Sheets."""
        try:
            scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                    "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
            self.client = gspread.authorize(creds)
            self.sheet = self.client.open(NOME_DA_PLANILHA).sheet1
            logger.info("Conexão com Google Sheets bem-sucedida.")
        except FileNotFoundError:
            logger.critical("ERRO: O arquivo 'credentials.json' não foi encontrado.")
            raise
        except Exception as e:
            logger.critical(f"ERRO ao conectar com o Google Sheets: {e}")
            raise
    
    async def find_date_row(self, date_str):
        """Encontra a linha e coluna correspondente a uma data."""
        try:
            cell = self.sheet.find(date_str)
            return {"success": True, "row": cell.row, "col": cell.col}
        except gspread.exceptions.CellNotFound:
            return {"success": False, "error": f"A data {date_str} não foi encontrada na planilha."}
        except Exception as e:
            logger.error(f"Erro ao buscar data '{date_str}': {e}")
            return {"success": False, "error": "Ocorreu um erro ao acessar a planilha."}
    
    async def update_cell_value(self, row, col, value_to_add):
        """Soma um valor a uma célula existente."""
        try:
            current_value_str = self.sheet.cell(row, col).value or "0"
            current_value_str = str(current_value_str).replace('R$', '').replace('.', '').replace(',', '.').strip()
            current_value = float(current_value_str)
            
            new_value = current_value + value_to_add
            self.sheet.update_cell(row, col, f'R$ {new_value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))
            return {"success": True, "newValue": new_value}
        except Exception as e:
            logger.error(f"Erro ao atualizar célula (linha {row}, col {col}): {e}")
            return {"success": False}
    
    async def read_cell_value(self, row, col):
        """Lê o valor de uma célula."""
        try:
            value_str = self.sheet.cell(row, col).value or "0"
            value_str = str(value_str).replace('R$', '').replace('.', '').replace(',', '.').strip()
            value = float(value_str)
            return {"success": True, "value": value}
        except Exception as e:
            logger.error(f"Erro ao ler célula (linha {row}, col {col}): {e}")
            return {"success": False}
