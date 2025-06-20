from telegram import ReplyKeyboardMarkup
from utils.formatters import get_current_date_str

# Teclado do menu principal
main_menu_keyboard = [
    ['💰 Entrada', '💸 Saída'],
    ['💳 Diário (Gasto)', '📊 Resumo do Dia'],
    ['📅 Ver Outro Dia']
]
main_menu = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)

async def start_command(update, context):
    """Handler para o comando /start."""
    chat_id = update.message.chat_id
    welcome_message = (
        f"🏦 *Assistente Financeiro*\n\n"
        f"Olá! Hoje é {get_current_date_str()}.\n\n"
        f"Escolha uma das opções abaixo:"
    )
    await context.bot.send_message(
        chat_id, welcome_message, reply_markup=main_menu, parse_mode='Markdown'
    )
