from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox
root = Tk() 
root.geometry("1200x660") 
root.title("Notes") 

#variable for open file name 
global open_status_name 
open_status_name= False 


#Functions for the file menu 


#Create new file 
def new_file(e):
    #Delete previous text 
    text_box.delete("1.0",END)
    #Update status bars 
    root.title("New Notes")
    status_bar.config(text="New File    ")
    global open_status_name 
    open_status_name= False 
    

#Open a file 
def open_file(e):
    #delete previous text 
    text_box.delete("1.0",END)
    #Read file name 
    text_file=filedialog.askopenfilename(initialdir="D:\Atul\PES\Computer Science\Project",title="Open file",filetypes=(("Text Files ","*.txt"),("HTML Files","*.html"),("Python files","*.py"),("All Files","*.*")))
    #Check to see if file name exists
    if text_file:
        #Make file name global to access later
        global open_status_name 
        open_status_name= text_file
    
    #Update status bar
    name=text_file
    status_bar.config(text=f'{name}        ')
    name = name.replace("D:/Atul/PES/Computer Science/Project/"," ") 
    root.title(f'{name}')


    #Open file 
    text_file= open(text_file,'r')
    content=text_file.read()
    #File to text box
    text_box.insert(END, content)
    text_box.edit_modified(False)
    #Close the opened file 
    text_file.close()

#Save as file 
def save_as_file(e):
    text_file = filedialog.asksaveasfilename(defaultextension=".*",initialdir="D:\\Atul\\PES\\Computer Science\\Project",title ="Save File",filetypes=(("Text Files ","*.txt"),("HTML Files","*.html"),("Python files","*.py"),("All Files","*.*")))
    if text_file:
        #Update satus bars
        name = text_file
        status_bar.config(text=f'Saved: {name}        ')
        name = name.replace("D:/Atul/PES/Computer Science/Project/"," ")
        root.title(f'{name}')

        #save the file 
        text_file=open(text_file,'w')
        text_file.write(text_box.get(1.0,END))
        #close file 
        text_file.close()

#Save File 

def save_file(e):
    global open_status_name 
    if open_status_name:
       #save the file 
        text_file=open(open_status_name,'w')
        text_file.write(text_box.get(1.0,END))
        #close file 
        text_file.close()
        text_box.edit_modified(False)
        status_bar.config(text=f'Saved: {open_status_name }        ')  
    
    else:
        save_as_file(e)



#Functions for the edit menu 


def cut_text(e):
	global selected
	if e:
		selected=root.clipboard_get()
	else:
		if text_box.selection_get():
			selected=text_box.selection_get()
			text_box.delete("sel.first", "sel.last")
			root.clipboard_clear()	
			root.clipboard_append(selected)
			
		
def paste_text(e):
	global selected
	if e:
		selected=root.clipboard_get()
	else:
		if selected:
			position=text_box.index(INSERT)
			text_box.insert(position,selected)
	

def copy_text(e):
	global selected
	if e:
		selected =root.clipboard_get()
	else:
		if text_box.selection_get():
			selected=text_box.selection_get()
			root.clipboard_clear()
			root.clipboard_append(selected)

def quit_fn(e):
    if text_box.edit_modified():
        result = messagebox.askyesno("Save Your Changes To This File?", "There are unsaved changes to your file, would you like to save them?")
        if result:
            save_file(e)
    root.quit()


#main frame
main_frame = Frame(root)
main_frame.pack(pady=5)

#scrollbar
scroll = Scrollbar(main_frame)
scroll.pack(side=RIGHT, fill=Y)

#Horizontal Scroll bar 
hor_scroll = Scrollbar(main_frame,orient='horizontal')
hor_scroll.pack(side=BOTTOM, fill=X)

#textbox
text_box= Text(main_frame, width=1280,height=734,font=("Calibri",14),selectbackground="yellow",selectforeground="black",undo=True,yscrollcommand=scroll.set,wrap='none',xscrollcommand=hor_scroll.set)#add font and selection later (font=("font",13))
text_box.pack()

#config scrollbar
scroll.config(command=text_box.yview)
hor_scroll.config(command=text_box.xview)

#menu bar 
menu_bar = Menu(root)
root.config(menu=menu_bar)

#file menu 
file_menu = Menu(menu_bar,tearoff=False)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New",command=lambda:new_file(False),accelerator="(ctrl+n)")
file_menu.add_command(label="Open",command=lambda:open_file(False),accelerator="(ctrl+o)")
file_menu.add_command(label="Save",command=lambda:save_file(False),accelerator="(ctrl+s)")
file_menu.add_command(label="Save As",command=lambda:save_as_file(False),accelerator="(ctrl+shift+s)")
file_menu.add_separator()
file_menu.add_command(label="Exit",command=lambda:quit_fn(False))

#edit menu 
edit_menu = Menu(menu_bar,tearoff=False)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut",command=lambda:cut_text(False),accelerator="(ctrl+x)")
edit_menu.add_command(label="Copy",command=lambda:copy_text(False),accelerator="(ctrl+c)")
edit_menu.add_command(label="Paste",command=lambda:paste_text(False),accelerator="(ctrl+v)")
edit_menu.add_separator()
edit_menu.add_command(label="Undo",command =text_box.edit_undo,accelerator='(Ctrl+z)')
edit_menu.add_command(label="Redo",command =text_box.edit_redo,accelerator='(Ctrl+y)')


root.bind("<Control-x>",cut_text)
root.bind("<Control-c>",copy_text)
root.bind("<Control-v>",paste_text)
root.bind("<Control-s>", save_file)
root.bind("<Control-o>", open_file)
root.bind("<Control-Shift-S>",save_as_file)
root.bind("<Control-n>",new_file)
root.protocol('WM_DELETE_WINDOW', lambda:quit_fn(False))

#Status bar at the bottom of the app 
status_bar = Label(root, text="Ready        ",anchor=E)
status_bar.pack(fill=X, side=BOTTOM,ipady=5)


root.mainloop()