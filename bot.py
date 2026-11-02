
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, LabeledPrice

BOT_TOKEN = "9226422583:AAEso3x4OrnNEKNqyJwIemCTlh0KI4X0p_g"
WEBAPP_URL = "https://uarhag90.github.io/crush-app/"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

@bot.message_handler(commands=['start'])
def start(message):
    args = message.text.split()
    url = WEBAPP_URL
    if len(args) > 1:
        url = f"{WEBAPP_URL}?to={args[1]}"
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💘 Открыть CRUSH", web_app=WebAppInfo(url=url)))
    markup.add(InlineKeyboardButton("🔗 Моя ссылка", callback_data="mylink"))
    
    bot.send_message(message.chat.id, "💘 <b>CRUSH - Твоя ссылка на признания готова!</b>\n\nДелись ссылкой в сторис и узнай кто в тебя влюблен.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "mylink")
def mylink_callback(call):
    link = f"https://t.me/{bot.get_me().username}?start={call.from_user.id}"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📲 Поделиться", url=f"https://t.me/share/url?url={link}"))
    bot.send_message(call.message.chat.id, f"Твоя ссылка:\n<code>{link}</code>", reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['pay49'])
def pay49(message):
    bot.send_invoice(
        chat_id=message.chat.id,
        title="Узнать кто в тебя влюблен",
        description="Открой анонимное признание и получи подсказку",
        invoice_payload="reveal_49",
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label="Открытие", amount=49)],
        start_parameter="pay49"
    )

@bot.message_handler(commands=['pay99'])
def pay99(message):
    bot.send_invoice(
        chat_id=message.chat.id,
        title="AI Совместимость",
        description="Полный отчет о совместимости",
        invoice_payload="compat_99",
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label="Совместимость", amount=99)],
        start_parameter="pay99"
    )

@bot.pre_checkout_query_handler(func=lambda query: True)
def pre_checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def success_payment(message):
    amount = message.successful_payment.total_amount
    bot.send_message(message.chat.id, f"✅ Оплата {amount} Stars успешна! Признание открыто! Подсказка: Парень, имя на А 😉")

@bot.message_handler(content_types=['web_app_data'])
def web_app_data(message):
    import json
    try:
        data = json.loads(message.web_app_data.data)
        action = data.get("action")
        if action == "buy_reveal":
            bot.send_invoice(
                chat_id=message.chat.id,
                title="Узнать кто в тебя влюблен",
                description="Открой признание и узнай подсказку",
                invoice_payload="reveal_49",
                provider_token="",
                currency="XTR",
                prices=[LabeledPrice(label="Открытие", amount=49)],
                start_parameter="reveal"
            )
        elif action == "buy_compat":
            bot.send_invoice(
                chat_id=message.chat.id,
                title="AI Совместимость",
                description="Полный отчет",
                invoice_payload="compat_99",
                provider_token="",
                currency="XTR",
                prices=[LabeledPrice(label="Совместимость", amount=99)],
                start_parameter="compat"
            )
    except Exception as e:
        print(e)

print(f"Бот запущен! Твое приложение: {WEBAPP_URL}")
print("Команды: /pay49 и /pay99")
bot.infinity_polling()
