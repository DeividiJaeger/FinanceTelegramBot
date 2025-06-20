from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config.settings import TELEGRAM_TOKEN, logger
from services.sheets_service import SheetsService
from models.user_state import UserStateManager
from handlers.command_handlers import start_command
from handlers.message_handlers import handle_message

# Instâncias globais
sheets_service = None
user_state_manager = None

async def message_handler_wrapper(update, context):
    """Wrapper para o handler de mensagens para passar as dependências."""
    await handle_message(update, context, user_state_manager, sheets_service)

def main() -> None:
    """Inicia o bot."""
    global sheets_service, user_state_manager
    
    # Inicializa os serviços
    sheets_service = SheetsService()
    user_state_manager = UserStateManager()
    
    # Configura a aplicação
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Registra os handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("menu", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler_wrapper))
    
    # Inicia o bot
    logger.info("Bot iniciado! Pressione Ctrl+C para parar.")
    application.run_polling()

if __name__ == '__main__':
    main()

# --- FUNÇÃO PRINCIPAL ---
def main() -> None:
    """Inicia o bot."""
    global sheets_service, user_state_manager
    
    # Inicializa os serviços
    sheets_service = SheetsService()
    user_state_manager = UserStateManager()
    
    # Configura a aplicação
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Registra os handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("menu", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler_wrapper))
    
    # Inicia o bot
    logger.info("Bot iniciado! Pressione Ctrl+C para parar.")
    application.run_polling()

# --- PONTO DE ENTRADA DO SCRIPT ---
if __name__ == '__main__':
    main()
