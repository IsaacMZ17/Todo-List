from tkinter import *
from tkinter import filedialog
import customtkinter
import pickle

#Definimos la apariencia de la aplicacion
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

#Se define la varibale que contiene la app
root = customtkinter.CTk()

#Definimos el titulo y el tamaño por defecto de la app
root.title('Todo list')
root.geometry('825x400')

#definimos la fuente que van a tener las tareas
P_font = customtkinter.CTkFont(
    family="Helvetica",
    size=30,
    weight="bold"
)

#Creamos una funcion para poner un placeholder a nuestro Entry
def placeHolderIn(event):
	if D_entry.get() == "Ingresa un mensaje":
		D_entry.delete(0, 'end')
		D_entry.config(fg='#ffffff')
		
def placeHolderOut(event):
	if D_entry.get() == "":
		D_entry.insert(0, "Ingresa un mensaje")
		D_entry.config(fg='#cccccc')

#creamos una entrada de datos para añadir las tareas
D_entry = customtkinter.CTkEntry(root, font=("Helvetica", 16))
D_entry.pack(fill='x', pady=25, padx=20)
D_entry.insert(0, "Ingresa un mensaje")
D_entry.bind("<FocusIn>", placeHolderIn)
D_entry.bind("<FocusOut>", placeHolderOut)


#creamos un frame para los botones
button_frame = customtkinter.CTkFrame(root, fg_color="transparent")
button_frame.pack(fill='x', expand=True, pady=0, padx=20)

#creamos un frame para las tareas
my_frame = customtkinter.CTkFrame(root)
my_frame.pack(fill= 'both', expand=True ,pady=10, padx=20)

#creamos un listbox
my_list = Listbox(my_frame,
                  font=P_font,
                  width=25,
                  height=5,
                  bg="#242424",
                  borderwidth=0,
                  fg='#cccccc',
                  selectbackground='#303030')
my_list.pack(side=LEFT, fill=BOTH, expand=True)

#creamos un scrollbar
my_scrollbar = Scrollbar(my_frame)
my_scrollbar.pack(side=RIGHT, fill=BOTH)

#agregamos scrollbar a el listbox
my_list.config(yscrollcommand=my_scrollbar.set)
my_scrollbar.config(command=my_list.yview)

#Funciones de la aplicacion

def add_item():
	my_list.insert(END, D_entry.get())
	D_entry.delete(0, END)

def delete_item():
	my_list.delete(ANCHOR)

def mark_item():
	my_list.itemconfig(
		my_list.curselection(),
		fg="#787878")
	my_list.selection_clear(0, END)

def unmark_item():
	my_list.itemconfig(
		my_list.curselection(),
		fg="#ffffff")
	my_list.selection_clear(0, END)

def delete_crossed():
	count = 0
	while count < my_list.size():
		if my_list.itemcget(count, "fg") == "#787878":
			my_list.delete(my_list.index(count))
		
		else: 
			count += 1

def save_list():
	file_name = filedialog.asksaveasfilename(
		initialdir="C:/gui/data",
		title="Save File",
		filetypes=(
			("Dat Files", "*.dat"), 
			("All Files", "*.*"))
		)
	if file_name:
		if file_name.endswith(".dat"):
			pass
		else:
			file_name = f'{file_name}.dat'

		count = 0
		while count < my_list.size():
			if my_list.itemcget(count, "fg") == "#dedede":
				my_list.delete(my_list.index(count))
			
			else: 
				count += 1

		stuff = my_list.get(0, END)

		output_file = open(file_name, 'wb')

		pickle.dump(stuff, output_file)


def open_list():
	file_name = filedialog.askopenfilename(
		initialdir="C:/gui/data",
		title="Open File",
		filetypes=(
			("Dat Files", "*.dat"), 
			("All Files", "*.*"))
		)

	if file_name:
		my_list.delete(0, END)

		input_file = open(file_name, 'rb')

		stuff = pickle.load(input_file)

		for item in stuff:
			my_list.insert(END, item)

def delete_list():
	my_list.delete(0, END)


# Creamos el menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Añadimos datos al menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Archivo", menu=file_menu)

# Añadimos datos al dropdown menu
file_menu.add_command(label="Guardar lista", command=save_list)
file_menu.add_command(label="Abrir lista", command=open_list)
file_menu.add_separator()
file_menu.add_command(label="Limpiar lista", command=delete_list)


# Añadimos los botones de la aplicacion
add_button = customtkinter.CTkButton(button_frame, text="Añadir", command=add_item)
delete_button = customtkinter.CTkButton(button_frame, text="Eliminar", fg_color="#db4f4f", command=delete_item)
mark_button = customtkinter.CTkButton(button_frame, text="Completar", fg_color="#57c930", command=mark_item)
unmark_button = customtkinter.CTkButton(button_frame, text="Desmarcar", fg_color="#117cad", command=unmark_item)
delete_crossed_button = customtkinter.CTkButton(button_frame, text="Eliminar Completados", fg_color="#eb8a4d", command=delete_crossed)

add_button.grid(row=0, column=0)
delete_button.grid(row=0, column=1, padx=20)
mark_button.grid(row=0, column=2)
unmark_button.grid(row=0, column=3, padx=20)
delete_crossed_button.grid(row=0, column=4)

root.mainloop()