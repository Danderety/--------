import socket
import platform
import netifaces
import tkinter as tk
from tkinter import ttk, filedialog
import csv

def get_main_network_info():
    gateways = netifaces.gateways()
    default_gateway = gateways.get('default', {}).get(netifaces.AF_INET)
    if default_gateway:
        main_interface = default_gateway[1]
        addrs = netifaces.ifaddresses(main_interface)
        ipv4_info = addrs.get(netifaces.AF_INET, [{}])[0]
        mac_address = addrs.get(netifaces.AF_LINK, [{}])[0].get('addr', 'Unknown')
        return ipv4_info.get('addr', 'No IP'), ipv4_info.get('netmask', 'No Mask'), mac_address
    return "No IP", "No Mask", "No MAC"

def populate_table():
    for row in table.get_children():
        table.delete(row)
    
    hostname = socket.gethostname()
    os_name = platform.system()
    ipv4, netmask, mac_address = get_main_network_info()
    
    data = [
        ("Имя компьютера", hostname),
        ("Операционная система", os_name),
        ("MAC-адрес", mac_address),
        ("IPv4-адрес", ipv4),
        ("Маска сети", netmask)
    ]
    
    for item in data:
        table.insert("", "end", values=item)

def search_and_filter_table():
    query = search_var.get().strip().lower()
    
    for row in table.get_children():
        table.delete(row)
    
    hostname = socket.gethostname()
    os_name = platform.system()
    ipv4, netmask, mac_address = get_main_network_info()
    
    data = [
        ("Имя компьютера", hostname),
        ("Операционная система", os_name),
        ("MAC-адрес", mac_address),
        ("IPv4-адрес", ipv4),
        ("Маска сети", netmask)
    ]
    
    for item in data:
        if query in item[0].lower() or query in item[1].lower():
            table.insert("", "end", values=item)

def save_to_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All Files", "*.*")])
    if not file_path:
        return
    
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Параметр", "Значение"])
        for row in table.get_children():
            writer.writerow(table.item(row, "values"))

root = tk.Tk()
root.title("Просмотр параметров")
root.geometry("600x300")

frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

search_var = tk.StringVar()
search_entry = tk.Entry(frame, textvariable=search_var)
search_entry.pack(pady=5, padx=10, ipadx=5, fill="x", anchor="n")
search_entry.bind("<KeyRelease>", lambda event: search_and_filter_table())

columns = ("Параметр", "Значение")
table = ttk.Treeview(frame, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=200)

table.pack(expand=True, fill="both")

button_frame = tk.Frame(root)
button_frame.pack(fill="x", side="bottom", padx=10, pady=5)

left_space = tk.Frame(button_frame)
left_space.pack(side="left", expand=True, fill="x")


btn_save = tk.Button(button_frame, text="Сохранить", command=save_to_file)
btn_save.pack(side="left", padx=5, pady=5)

right_space = tk.Frame(button_frame)
right_space.pack(side="left", expand=True, fill="x")

populate_table()
root.mainloop()