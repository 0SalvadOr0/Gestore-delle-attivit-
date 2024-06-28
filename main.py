import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import pickle

def aggiungi_task():
    task = txt_input.get()
    comment = comment_input.get()
    if task != "":
        op = messagebox.askyesno(title="Attenzione!", message="Vuoi aggiungere una scadenza?")
        if op:
            data_scadenza = scadenza_input.get_date()
            ora_scadenza = ora_input.get()
            scadenza = datetime.combine(data_scadenza, datetime.strptime(ora_scadenza, '%H:%M').time())
            tree.insert('', 'end', text=task, values=(comment, scadenza))
        else:
            tree.insert('', 'end', text=task, values=(comment,))
        txt_input.delete(0, tk.END)
        comment_input.delete(0, tk.END)
    else:
        messagebox.showwarning(title="Attenzione!", message="Devi inserire un task.")


def elimina_task():
    try:
        selected_item = tree.selection()[0]
        op = messagebox.askyesno(title="Attenzione!", message="Sei sicuro di voler eliminare la task?")
        if op:
            tree.delete(selected_item)
    except:
        messagebox.showwarning(title="Attenzione!", message="Devi selezionare un task.")

def modifica_task():
    try:
        selected_item = tree.selection()[0]
        op = messagebox.askyesno(title="Attenzione!", message="Sei sicuro di voler modificare la task?")
        if op:
            new_task = txt_input.get()
            new_comment = comment_input.get()
            if new_task != "":
                tree.item(selected_item, text=new_task, values=(new_comment,))
                txt_input.delete(0, tk.END)
                comment_input.delete(0, tk.END)
            else:
                messagebox.showwarning(title="Attenzione!", message="Devi inserire un task.")
    except:
        messagebox.showwarning(title="Attenzione!", message="Devi selezionare un task.")

def ricerca_task():
    termine_ricerca = ricerca_input.get()
    selezionati = tree.get_children('')
    for selezionato in selezionati:
        task = tree.item(selezionato, 'text')
        if termine_ricerca.lower() in task.lower():
            tree.selection_add(selezionato)

def ordina_task():
    items = tree.get_children('')
    items_sorted = sorted(items, key=lambda x: tree.item(x, 'text'))
    for index, item in enumerate(items_sorted):
        tree.move(item, '', index)

def salva_task():
    items = tree.get_children('')
    tasks = []
    for item in items:
        task = tree.item(item, 'text')
        comment, scadenza = tree.item(item, 'values')
        tasks.append((task, comment, scadenza))
    with open('tasks.pkl', 'wb') as f:
        pickle.dump(tasks, f)

def carica_task():
    try:
        with open('tasks.pkl', 'rb') as f:
            tasks = pickle.load(f)
        for task, comment, scadenza in tasks:
            tree.insert('', 'end', text=task, values=(comment, scadenza))
    except FileNotFoundError:
        pass

window = tk.Tk()
window.title("Gestore di Attività")

frame_buttons_top = tk.Frame(window)
frame_buttons_top.pack()

btn_ordina_task = tk.Button(frame_buttons_top, text="Ordina task", command=ordina_task, background="purple", font=('Helvetica', 12))
btn_ordina_task.pack(side=tk.LEFT)

btn_ricerca_task = tk.Button(frame_buttons_top, text="Ricerca task", command=ricerca_task, background="yellow", font=('Helvetica', 12))
btn_ricerca_task.pack(side=tk.LEFT)

ricerca_input = tk.Entry(frame_buttons_top, width=50, font=('Helvetica', 10))
ricerca_input.pack(side=tk.LEFT)

frame_tasks = tk.Frame(window)
frame_tasks.pack()

tree = ttk.Treeview(frame_tasks, columns=('Commenti', 'Data di scadenza'), height=15)
tree.heading('#0', text='Attività')
tree.heading('#1', text='Commenti')
tree.heading('#2', text='Data di scadenza')
tree.column('#1', stretch=tk.NO, width=200)
tree.column('#2', stretch=tk.NO, width=200)
tree.pack(side=tk.LEFT)

scrollbar_tasks = tk.Scrollbar(frame_tasks)
scrollbar_tasks.pack(side=tk.RIGHT, fill=tk.Y)

tree.config(yscrollcommand=scrollbar_tasks.set)
scrollbar_tasks.config(command=tree.yview)


txt_input = tk.Entry(window, width=50, font=('Helvetica', 14))
txt_input.pack()

comment_input = tk.Entry(window, width=50, font=('Helvetica', 14))
comment_input.pack()

frame_time = tk.Frame(window)
frame_time.pack()

scadenza_input = DateEntry(frame_time, width=12, background='darkblue', foreground='white', borderwidth=2, font=('Helvetica', 12))
scadenza_input.set_date(datetime.now() + timedelta(days=1))  # Imposta la data di default per domani
scadenza_input.pack(side=tk.LEFT)

ora_input = tk.Entry(frame_time, width=5, font=('Helvetica', 12))
ora_input.insert(0, '00:00')  # Imposta l'ora di default per mezzanotte
ora_input.pack(side=tk.LEFT)

frame_buttons_bottom = tk.Frame(window)
frame_buttons_bottom.pack()

btn_add_task = tk.Button(frame_buttons_bottom, text="Aggiungi task", command=aggiungi_task, background="green", font=('Helvetica', 14))
btn_add_task.pack(side=tk.LEFT)

btn_del_task = tk.Button(frame_buttons_bottom, text="Elimina task", command=elimina_task, background="red", font=('Helvetica', 14))
btn_del_task.pack(side=tk.LEFT)

btn_mod_task = tk.Button(frame_buttons_bottom, text="Modifica task", command=modifica_task, background="blue", font=('Helvetica', 14))
btn_mod_task.pack(side=tk.LEFT)

# Aggiungi questi pulsanti al tuo codice
btn_salva_task = tk.Button(frame_buttons_bottom, text="Salva task", command=salva_task, background="blue", font=('Helvetica', 14))
btn_salva_task.pack(side=tk.LEFT)

btn_carica_task = tk.Button(frame_buttons_bottom, text="Carica task", command=carica_task, background="green", font=('Helvetica', 14))
btn_carica_task.pack(side=tk.LEFT)


window.mainloop()

