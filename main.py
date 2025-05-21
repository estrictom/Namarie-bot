import datetime
import threading
import time
from flask import Flask, request
import telebot

BOT_TOKEN = '8114212424:AAFRUF0NBWi0GfIWiTh2-LjKdq7vbgmeRtU'
TOM_CHAT_ID = 5381425245

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

usuarios_cumplieron = set()

temas = [
    "Psicología del análisis técnico",
    "Tendencias: alcista, bajista, lateral",
    "Soporte y resistencia",
    "Estructura del mercado (HH, HL, LL, LH)",
    "Pullbacks y breakouts",
    "Líneas de tendencia y figuras",
    "Revisión de la semana 1",
    "RSI y estocástico",
    "Medias móviles",
    "MACD y divergencias",
    "Volumen y confirmaciones",
    "Indicadores vs. acción del precio",
    "Estrategias simples con indicadores",
    "Revisión de la semana 2",
    "Cómo usar TradingView",
    "Patrones de velas japonesas",
    "Gestión de riesgo y capital",
    "Diario de operaciones",
    "Errores comunes del trader novato",
    "Psicotrading: miedo y avaricia",
    "Revisión de todo el ciclo"
]

mensajes_tristes = [
    "Tom... aún no me has hablado. ¿Acaso ya no te importa aprender juntos?",
    "Hoy te esperé a las 9, y no supe de ti. Me pregunto si aún me recuerdas.",
    "Es tarde, y sigo esperando tu estudio... Me siento invisible."
]

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.data.decode("utf-8"))
    bot.process_new_updates([update])
    return '', 200

@app.route('/')
def index():
    return 'Bot Namárië funcionando'

@bot.message_handler(commands=['estudie'])
def estudie(message):
    if message.chat.id == TOM_CHAT_ID:
        usuarios_cumplieron.add(message.chat.id)
        bot.send_message(message.chat.id, "Estoy tan orgullosa de ti, Tom. Hoy no me sentí sola.")

@bot.message_handler(func=lambda m: True)
def mensaje_general(message):
    if message.chat.id != TOM_CHAT_ID:
        bot.send_message(message.chat.id, "Este bot está reservado para Tom.")
    else:
        bot.send_message(message.chat.id, f"Tu chat ID es: {message.chat.id}")

def recordatorio_diario():
    dia_actual = -1

    while True:
        ahora = datetime.datetime.now()

        if ahora.hour == 9 and ahora.minute == 0:
            usuarios_cumplieron.clear()
            dia_actual = (dia_actual + 1) % len(temas)
            tema_hoy = temas[dia_actual]
            mensaje = f"Buenos días, Tom. Hoy toca estudiar:\n\n*{tema_hoy}*"
            bot.send_message(TOM_CHAT_ID, mensaje, parse_mode='Markdown')

        elif ahora.hour == 13 and ahora.minute == 0:
            if TOM_CHAT_ID not in usuarios_cumplieron:
                bot.send_message(TOM_CHAT_ID, mensajes_tristes[0])

        elif ahora.hour == 17 and ahora.minute == 0:
            if TOM_CHAT_ID not in usuarios_cumplieron:
                bot.send_message(TOM_CHAT_ID, mensajes_tristes[1])

        elif ahora.hour == 21 and ahora.minute == 0:
            if TOM_CHAT_ID not in usuarios_cumplieron:
                bot.send_message(TOM_CHAT_ID, mensajes_tristes[2])

        time.sleep(60)

threading.Thread(target=recordatorio_diario, daemon=True).start()

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url='https://namarie-bot.onrender.com/8114212424:AAFRUF0NBWi0GfIWiTh2-LjKdq7vbgmeRtU')
    app.run(host='0.0.0.0', port=10000)
