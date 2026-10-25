from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import requests
import json
import pprint

from bottle import response


def update_label(event):
    combobox = event.widget
    code = combobox.get()
    name = currencies[code]
    combobox.associated_label.config(text=name)

def exchange():
    target_code = target_combobox.get().strip()
    base_code = base_combobox.get().strip()
    if target_code and base_code:
        try:
            response = requests.get(f'https://open.er-api.com/v6/latest/{base_code}')
            response.raise_for_status()
            data = response.json()
            if target_code in data['rates']:
                exchange_rate = data['rates'][target_code]
                base = currencies[base_code]
                target = currencies[target_code]
                mb.showinfo('Курс обмена',
                            f'Курс: {exchange_rate:.1f} {target} за 1 {base}')
            else:
                mb.showerror('Ошибка',
                            f'Валюта {target_code} не найдена')
        except Exception as er:
            mb.showerror('Ошибка', er)

    else:
        mb.showwarning('Внимание', 'Введите код валюты')


currencies = {
    'EUR': 'Евро',
    'USD': 'Доллар США',
    'JPY': 'Японская йена',
    'GBP': 'Фунт стерлингов',
    'AUD': 'Австралийский доллар',
    'CAD': 'Канадский доллар',
    'CHF': 'Швейцарский франк',
    'CNY': 'Китайский юань',
    'RUB': 'Российский рубль',
    'KZT': 'Казахстанский тенге',
    'UZS': 'Узбекский сум'

}

root = Tk()
root.title('Курс обмена валют USD')
root.geometry('360x300')

def create_currency_block(title_text):
    Label(root, text=title_text, font=('Arial', 10, 'bold')).pack(pady=(10, 2))
    combo = ttk.Combobox(root, values=list(currencies.keys()), state="readonly")
    combo.pack(pady=3, padx=10)
    label = ttk.Label(root, text="")
    label.pack()

    combo.associated_label = label
    combo.bind('<<ComboboxSelected>>', update_label)
    return combo


base_combobox1 = create_currency_block('Первая базовая валюта')
base_combobox2 = create_currency_block('Вторая базовая валюта')
target_combobox = create_currency_block('Целевая валюта')

Button(text='Получить курс обмена',
       command=exchange).pack(pady=10, padx=10)


root.mainloop()