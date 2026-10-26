from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import requests


def update_label(event):
    combobox = event.widget
    code = combobox.get()
    name = currencies[code]
    combobox.associated_label.config(text=name)

def exchange():
    base1 = base_combobox1.get().strip()
    base2 = base_combobox2.get().strip()
    target = target_combobox.get().strip()

    if not target:
        mb.showwarning('Внимание', 'Пожалуйста, выберите целевую валюту')
        return

    if not base1 and not base2:
        mb.showwarning('Внимание', 'Выберите хотя бы одну базовую валюту')
        return

    results = []  # Сюда будем собирать строки с результатами

    if base1:
        try:
            resp = requests.get(f'https://open.er-api.com/v6/latest/{base1}')
            resp.raise_for_status()
            data = resp.json()
            if target in data['rates']:
                rate = data['rates'][target]
                results.append(f"1 {currencies[base1]} = {rate:.2f} {currencies[target]}")
        except Exception as e:
            results.append(f"Ошибка по 1-й валюте: {e}")

    if base2:
        try:
            resp = requests.get(f'https://open.er-api.com/v6/latest/{base2}')
            resp.raise_for_status()
            data = resp.json()
            if target in data['rates']:
                rate = data['rates'][target]
                results.append(f"1 {currencies[base2]} = {rate:.2f} {currencies[target]}")
        except Exception as e:
            results.append(f"Ошибка по 2-й валюте: {e}")

    mb.showinfo('Курс обмена', "\n\n".join(results))


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
root.geometry('360x350')

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

Button(text='Получить курс обмена', font=('Arial', 10, 'bold'),
       bg='#4CAF50', fg='white', command=exchange).pack(pady=20, padx=10)


root.mainloop()