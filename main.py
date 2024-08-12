import telebot
import json
import os
from datetime import datetime

# Ініціалізація бота з токеном
API_TOKEN = '7444998776:AAHJc8cgeet-V9iGdf5bF9JYkrBkpE90GQQ'
bot = telebot.TeleBot(API_TOKEN)

# Файл для зберігання даних
DATA_FILE = 'data.json'

# Список категорій витрат
EXPENSE_CATEGORIES = ['Їжа', 'Транспорт', 'Розваги', 'Комунальні послуги', 'Одяг', 'Інше']

# Ініціалізація порожнього файлу, якщо його не існує
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

# Функція для завантаження даних
def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


# Функція для збереження даних
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Функція для додавання витрат або доходів
def add_record(user_id, record_type, amount, category):
    data = load_data()
    if user_id not in data:
        data[user_id] = {'expenses': [], 'income': []}
    record = {
        'amount': amount,
        'category': category,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    data[user_id][record_type].append(record)
    save_data(data)

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Вітаю! Це бот для відстеження ваших витрат та доходів. "
                          "Використовуйте команди:\n"
                          "/add_expense - додати витрати\n"
                          "/add_income - додати дохід\n"
                          "/show_expenses - показати витрати\n"
                          "/show_income - показати доходи\n"
                          "/delete_record - видалити запис\n"
                          "/categories - показати категорії витрат\n"
                          "/stats - показати статистику")

# Команда для додавання витрат
@bot.message_handler(commands=['add_expense'])
def add_expense(message):
    msg = bot.reply_to(message, "Введіть суму витрат і категорію через пробіл (наприклад, '100 Їжа'):")
    bot.register_next_step_handler(msg, process_expense)


def process_expense(message):
    try:
        user_id = str(message.from_user.id)
        amount, category = message.text.split()
        amount = float(amount)
        if category in EXPENSE_CATEGORIES:
            add_record(user_id, 'expenses', amount, category)
            bot.reply_to(message, "Витрати додані!")
        else:
            bot.reply_to(message, "Категорія невідома. Спробуйте ще раз.")
    except ValueError:
        bot.reply_to(message, "Неправильний формат введення. Спробуйте ще раз.")

# Команда для додавання доходів
@bot.message_handler(commands=['add_income'])
def add_income(message):
    msg = bot.reply_to(message, "Введіть суму доходу і категорію через пробіл (наприклад, '100 Зарплата'):")
    bot.register_next_step_handler(msg, process_income)

def process_income(message):
    try:
        user_id = str(message.from_user.id)
        amount, category = message.text.split()
        amount = float(amount)
        add_record(user_id, 'income', amount, category)
        bot.reply_to(message, "Дохід доданий!")
    except ValueError:
        bot.reply_to(message, "Неправильний формат введення. Спробуйте ще раз.")

# Команда для перегляду витрат
@bot.message_handler(commands=['show_expenses'])
def show_expenses(message):
    user_id = str(message.from_user.id)
    data = load_data()
    if user_id in data and data[user_id]['expenses']:
        expenses = data[user_id]['expenses']
        response = "\n".join([f"{e['amount']} {e['category']} - {e['date']}" for e in expenses])
    else:
        response = "Ви ще не додали витрати."
    bot.reply_to(message, response)

# Команда для перегляду доходів
@bot.message_handler(commands=['show_income'])
def show_income(message):
    user_id = str(message.from_user.id)
    data = load_data()
    if user_id in data and data[user_id]['income']:
        income = data[user_id]['income']
        response = "\n".join([f"{e['amount']} {e['category']} - {e['date']}" for e in income])
    else:
        response = "Ви ще не додали доходи."
    bot.reply_to(message, response)

# Команда для видалення запису
@bot.message_handler(commands=['delete_record'])
def delete_record(message):
    bot.reply_to(message, "Функція видалення записів ще в розробці.")

# Команда для перегляду категорій витрат
@bot.message_handler(commands=['categories'])
def show_categories(message):
    response = "Доступні категорії витрат:\n" + "\n".join(EXPENSE_CATEGORIES)
    bot.reply_to(message, response)

# Команда для статистики
@bot.message_handler(commands=['stats'])
def show_stats(message):
    bot.reply_to(message, "Функція статистики ще в розробці.")


# Запуск бота
bot.polling()
