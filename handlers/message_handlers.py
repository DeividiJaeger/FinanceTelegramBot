from datetime import datetime
from config.settings import COLUMN_OFFSET, logger
from utils.formatters import get_current_date_str, format_date_from_day, format_financial_message, format_day_summary
from handlers.command_handlers import main_menu

async def handle_message(update, context, user_state_manager, sheets_service):
    """Handler principal para mensagens."""
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    text = update.message.text

    # Verifica se o usuário está em algum estado
    if user_state_manager.has_state(user_id):
        await handle_user_in_state(update, context, user_state_manager, sheets_service)
        return

    # Processa as opções do menu principal
    if text == '💰 Entrada':
        user_state_manager.set_state(user_id, {'action': 'entrada'})
        await context.bot.send_message(chat_id, '💰 Digite o valor da entrada (será somado ao total do dia):')
    
    elif text == '💸 Saída':
        user_state_manager.set_state(user_id, {'action': 'saida'})
        await context.bot.send_message(chat_id, '💸 Digite o valor da saída (será somado ao total do dia):')

    elif text == '💳 Diário (Gasto)':
        user_state_manager.set_state(user_id, {'action': 'diario'})
        await context.bot.send_message(chat_id, '💳 Digite o valor gasto hoje (será somado ao diário):')

    elif text == '📊 Resumo do Dia':
        await show_day_summary(chat_id, datetime.now().day, context, sheets_service)

    elif text == '📅 Ver Outro Dia':
        user_state_manager.set_state(user_id, {'action': 'ver_dia'})
        await context.bot.send_message(chat_id, '📅 Digite o dia (apenas o número) que deseja consultar (do mês atual):')

async def handle_user_in_state(update, context, user_state_manager, sheets_service):
    """Processa mensagens quando o usuário está em um estado específico."""
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    text = update.message.text
    state = user_state_manager.get_state(user_id)
    action = state['action']
    
    try:
        value = float(text.replace(',', '.'))
    except ValueError:
        await context.bot.send_message(chat_id, '❌ Por favor, digite um valor numérico válido.')
        return

    user_state_manager.clear_state(user_id)

    if action in ['entrada', 'saida', 'diario']:
        date_to_find = get_current_date_str()
        date_location = await sheets_service.find_date_row(date_to_find)

        if not date_location['success']:
            await context.bot.send_message(chat_id, f"❌ {date_location['error']}", reply_markup=main_menu)
            return

        base_row = date_location['row']
        base_col = date_location['col']
        
        target_col = base_col + COLUMN_OFFSET[action]
        
        update_result = await sheets_service.update_cell_value(base_row, target_col, value)

        if update_result['success']:
            new_total = update_result['newValue']
            response_message = format_financial_message(action, value, date_to_find, new_total)
            await context.bot.send_message(chat_id, response_message, reply_markup=main_menu)
        else:
            await context.bot.send_message(chat_id, f'❌ Erro ao registrar {action}. Tente novamente.', reply_markup=main_menu)
    
    elif action == 'ver_dia':
        day_to_show = int(value)
        await show_day_summary(chat_id, day_to_show, context, sheets_service)

async def show_day_summary(chat_id, day, context, sheets_service):
    """Busca os dados de um dia e envia o resumo."""
    if not 1 <= day <= 31:
        await context.bot.send_message(chat_id, '❌ Dia inválido. Por favor, digite um número de 1 a 31.', reply_markup=main_menu)
        return
    
    date_to_find = format_date_from_day(day)
    
    date_location = await sheets_service.find_date_row(date_to_find)
    if not date_location['success']:
        await context.bot.send_message(chat_id, f"❌ {date_location['error']}", reply_markup=main_menu)
        return

    base_row = date_location['row']
    base_col = date_location['col']
    
    # Lê os valores das colunas adjacentes usando o offset
    entrada_res = await sheets_service.read_cell_value(base_row, base_col + COLUMN_OFFSET['entrada'])
    saida_res = await sheets_service.read_cell_value(base_row, base_col + COLUMN_OFFSET['saida'])
    diario_res = await sheets_service.read_cell_value(base_row, base_col + COLUMN_OFFSET['diario'])
    saldo_res = await sheets_service.read_cell_value(base_row, base_col + COLUMN_OFFSET['saldo'])

    if not all([entrada_res['success'], saida_res['success'], diario_res['success'], saldo_res['success']]):
        await context.bot.send_message(chat_id, '❌ Erro ao buscar dados da planilha. Tente novamente.', reply_markup=main_menu)
        return
        
    resumo = format_day_summary(
        date_to_find, 
        entrada_res['value'], 
        saida_res['value'], 
        diario_res['value'], 
        saldo_res['value']
    )
    
    await context.bot.send_message(chat_id, resumo, parse_mode='Markdown', reply_markup=main_menu)
