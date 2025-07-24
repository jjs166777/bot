import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Ваш Bitcoin-адрес (замените на свой)
BITCOIN_ADDRESS = "bc1qexampleyourwalletaddress"

# Главное меню
main_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("Товары 1", callback_data="category_1")],
    [InlineKeyboardButton("Товары 2", callback_data="category_2")],
    [InlineKeyboardButton("Товары 3", callback_data="category_3")],
    [InlineKeyboardButton("Личный кабинет", callback_data="profile")],
])

# Продукты по категориям
def product_buttons(category):
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(f"Товар {i+1}", callback_data=f"buy_{category}_{i+1}")]
         for i in range(3)] +  # сократим до 3, чтобы не было перегруза
        [[InlineKeyboardButton("Назад", callback_data="main")]]
    )

# Клавиатура профиля
profile_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("Баланс: 0 USD", callback_data="none")],
    [InlineKeyboardButton("Пополнить", callback_data="topup")],
    [InlineKeyboardButton("Назад", callback_data="main")]
])

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Главное меню", reply_markup=main_keyboard)

# Обработка нажатий кнопок
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data in ["main", "back_main"]:
        await query.edit_message_text("Главное меню", reply_markup=main_keyboard)
    elif data == "category_1":
        await query.edit_message_text("Товары 1", reply_markup=product_buttons("1"))
    elif data == "category_2":
        await query.edit_message_text("Товары 2", reply_markup=product_buttons("2"))
    elif data == "category_3":
        await query.edit_message_text("Товары 3", reply_markup=product_buttons("3"))
    elif data == "profile":
        await query.edit_message_text("Ваш личный кабинет", reply_markup=profile_keyboard)
    elif data == "topup":
        await query.edit_message_text(
            f"Для пополнения ваш биткоин-адрес:\n<code>{BITCOIN_ADDRESS}</code>",
            parse_mode='HTML',
            reply_markup=profile_keyboard
        )
    elif data.startswith("buy_"):
        await query.edit_message_text(
            "Не достаточно средств. / Not enough funds.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("В личный кабинет / Go to profile", callback_data="profile")]
            ])
        )

# Запуск бота
async def main():
    token = os.getenv("8313235069:AAGgV97DRQy9LquFcPrvEidz6TvlqLRV6dI")
    if not token:
        print("❌ Ошибка: переменная окружения YOUR_BOT_TOKEN не установлена.")
        return

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))

    print("✅ Бот запущен...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
