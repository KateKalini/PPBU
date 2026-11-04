from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import requests


def update_base_label(event):
    code = base_combobox.get()
    name = crypto_currencies[code]['name']
    base_label.config(text=name)


def exchange():
    crypto_code = base_combobox.get().strip()

    if crypto_code:
        try:
            coin_id = crypto_currencies[crypto_code]['id']

            response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd')
            response.raise_for_status()
            data = response.json()

            # Проверяем наличие данных в ответе сервера
            if coin_id in data and 'usd' in data[coin_id]:
                exchange_rate = data[coin_id]['usd']
                crypto_name = crypto_currencies[crypto_code]['name']

                # Форматируем вывод: для дешевых монет (DOGE) выводим больше знаков после точки
                fmt = ".2f" if exchange_rate >= 1 else ".5f"

                mb.showinfo('Курс обмена',
                            f'Курс: {exchange_rate:{fmt}} Долларов США за 1 {crypto_name}')
            else:
                mb.showerror('Ошибка', f'Курс для {crypto_code} не найден')
        except Exception as er:
            mb.showerror('Ошибка', f'Не удалось получить данные:\n{er}')
    else:
        mb.showwarning('Внимание', 'Пожалуйста, выберите криптовалюту')


crypto_currencies = {
    'BTC': {'id': 'bitcoin', 'name': 'Биткоин'},
    'ETH': {'id': 'ethereum', 'name': 'Эфириум'},
    'SOL': {'id': 'solana', 'name': 'Солана'},
    'BNB': {'id': 'binancecoin', 'name': 'Бинанс Коин'},
    'XRP': {'id': 'ripple', 'name': 'Рипл'},
    'DOGE': {'id': 'dogecoin', 'name': 'Догикоин'},
    'TON': {'id': 'the-open-network', 'name': 'Тонкоин'}
}

root = Tk()
root.title('Крипто-Калькулятор (USD)')
root.geometry('360x150')


Label(root, text='Выберите криптовалюту', font=('Arial', 10, 'bold')).pack(pady=(15, 0))
base_combobox = ttk.Combobox(root, values=list(crypto_currencies.keys()), state="readonly")
base_combobox.pack(pady=5, padx=10)
base_combobox.bind('<<ComboboxSelected>>', update_base_label)

base_label = ttk.Label(root)
base_label.pack()

style = ttk.Style()
style.configure('TButton', font=('Arial', 10, 'bold'))

Button = ttk.Button(root, text='Получить курс к доллару', command=exchange)
Button.pack(pady=15, padx=10)

root.mainloop()