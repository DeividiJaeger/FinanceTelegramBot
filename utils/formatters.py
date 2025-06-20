from datetime import datetime

def get_current_date_str():
    """Retorna a data atual formatada como 'DD/MM/YYYY'."""
    return datetime.now().strftime('%d/%m/%Y')

def format_date_from_day(day):
    """Formata a data a partir do dia, usando o mês e ano atuais."""
    now = datetime.now()
    return f"{day:02d}/{now.month:02d}/{now.year}"

def format_financial_message(action, value, date, new_total=None):
    """Formata mensagem para operações financeiras."""
    message = f"✅ {action.capitalize()} de R$ {value:,.2f} registrada para {date}!\n"
    if new_total is not None:
        message += f"💰 Novo total de {action}s nesta célula: R$ {new_total:,.2f}"
    
    # Formatação para o padrão brasileiro de números
    return message.replace(',', 'X').replace('.', ',').replace('X', '.')

def format_day_summary(date, entrada, saida, diario, saldo):
    """Formata resumo do dia."""
    resumo = (
        f"📊 *Resumo de {date}*\n\n"
        f"💰 Entradas: R$ {entrada:,.2f}\n"
        f"💸 Saídas: R$ {saida:,.2f}\n"
        f"💳 Diário: R$ {diario:,.2f}\n"
        f"💵 Saldo: R$ {saldo:,.2f}"
    )
    # Formatação para o padrão brasileiro de números
    return resumo.replace(',', 'X').replace('.', ',').replace('X', '.')
