from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import requests


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
