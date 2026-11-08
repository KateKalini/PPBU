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
            # Для KuCoin формируем торговую пару к USDT (например, BTC-USDT)
            symbol = f"{crypto_code}-USDT"

            url = "https://api.kucoin.com/api/v1/market/orderbook/level1"
            response = requests.get(url, params={"symbol": symbol})
            response.raise_for_status()
            res_data = response.json()

            if res_data.get("code") == "200000" and res_data.get("data"):
                exchange_rate = float(res_data["data"]["price"])
                crypto_name = crypto_currencies[crypto_code]['name']

                # Форматируем вывод: для дешевых монет выводим больше знаков после точки
                fmt = ".2f" if exchange_rate >= 1 else ".5f"

                mb.showinfo('Курс обмена (KuCoin)',
                            f'Курс: {exchange_rate:{fmt}} USDT (USD) за 1 {crypto_name}')
            else:
                mb.showerror('Ошибка API', f'Биржа вернула ошибку: {res_data.get("msg", "Неизвестная ошибка")}')
        except Exception as er:
            mb.showerror('Ошибка', f'Не удалось получить данные с KuCoin:\n{er}')
    else:
        mb.showwarning('Внимание', 'Пожалуйста, выберите криптовалюту')


crypto_currencies = {
    'BTC': {'name': 'Биткоин'},
    'ETH': {'name': 'Эфириум'},
    'SOL': {'name': 'Солана'},
    'BNB': {'name': 'Бинанс Коин'},
    'XRP': {'name': 'Рипл'},
    'DOGE': {'name': 'Догикоин'},
    'TON': {'name': 'Тонкоин'}
}


root = Tk()
root.title('Крипто-Калькулятор (KuCoin)')
root.geometry('360x150')


Label(root, text='Выберите криптовалюту', font=('Arial', 10, 'bold')).pack(pady=(15, 0))
base_combobox = ttk.Combobox(root, values=list(crypto_currencies.keys()), state="readonly")
base_combobox.pack(pady=5, padx=10)
base_combobox.bind('<<ComboboxSelected>>', update_base_label)

base_label = ttk.Label(root)
base_label.pack()

style = ttk.Style()
style.configure('TButton', font=('Arial', 10, 'bold'))

Button = ttk.Button(root, text='Получить курс к USDT', command=exchange)
Button.pack(pady=15, padx=10)

root.mainloop()
