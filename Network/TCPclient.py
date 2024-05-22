from tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, Button, messagebox, Listbox, Scrollbar, VERTICAL
import socket
import threading
from Auth import Auth
from rooms import RoomsGUI

class GUI:
    client_socket = None
    last_received_message = None
    
    def __init__(self, master):
        self.auth = Auth("users.db") 
        self.root = master
        self.chat_transcript_area = None
        self.name_widget = None
        self.enter_text_widget = None
        self.join_button = None
        self.chat_rooms_btn = Button(self.root, text="Chat Rooms", command=self.open_rooms_gui, bg="black", fg="white")
        self.chat_rooms_btn.pack(pady=20)
        self.root.title("Chat")
        # self.display_sidebar() 

        self.initialize_socket()
        self.initialize_gui()
        self.listen_for_incoming_messages_in_a_thread()
        self.display_login_registration() 

    def initialize_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initialazing socket with TCP and IPv4
        remote_ip = '127.0.0.1' # IP address 
        remote_port = 10319 #TCP port
        self.client_socket.connect((remote_ip, remote_port)) #connect to the remote server

    def initialize_gui(self):
        self.root.title("Socket Chat")
        self.root.resizable(0, 0)
        self.root.config(bg="black")  # Set window background color to black

        # Display the chat room label
        self.chat_room_label = Label(self.root, text="Chat Room: Main", font=("Serif", 12), bg="black", fg="white")
        self.chat_room_label.pack(pady=5)

        self.display_chat_box()
        self.display_chat_entry_box()
        self.chat_transcript_area.tag_config('blue', foreground='blue', font=('Helvetica', 12, 'bold'))  # Tag configuration for username color and font

    def listen_for_incoming_messages_in_a_thread(self):
        thread = threading.Thread(target=self.receive_message_from_server, args=(self.client_socket,)) # Create a thread for the send and receive in same time 
        thread.start()

    #function to recieve msg
    def receive_message_from_server(self, so):
        while True:
            buffer = so.recv(256)
            if not buffer:
                break
            message = buffer.decode('utf-8')
        
            if "joined" in message:
                user = message.split(":")[1]
                message = user + " has joined"
                self.chat_transcript_area.insert('end', message + '\n')
                self.chat_transcript_area.yview(END)
            else:
                sender, received_message = message.split(":", 1)
                self.chat_transcript_area.insert('end', sender + ":", 'blue')  # Insert sender in blue
                self.chat_transcript_area.insert('end', received_message + '\n')  # Insert message
                self.chat_transcript_area.yview(END)

        so.close()

    def display_chat_box(self):
        frame = Frame(bg="black")
        Label(frame, text='Chat Box:', font=("Serif", 12), bg="black", fg="white").pack(side='top', anchor='w')
        self.chat_transcript_area = Text(frame, width=60, height=10, font=("Serif", 12), bg="black", fg="white")
        scrollbar = Scrollbar(frame, command=self.chat_transcript_area.yview, orient=VERTICAL)
        self.chat_transcript_area.config(yscrollcommand=scrollbar.set)
        self.chat_transcript_area.bind('<KeyPress>', lambda e: 'break')
        self.chat_transcript_area.pack(side='left', padx=10)
        scrollbar.pack(side='right', fill='y')
        frame.pack(side='top')

    def display_chat_entry_box(self):
        frame = Frame(bg="black")
        Label(frame, text='Enter message:', font=("Serif", 12), bg="black", fg="white").pack(side='top', anchor='w')
        self.enter_text_widget = Text(frame, width=60, height=3, font=("Serif", 12), bg="black", fg="white")
        self.enter_text_widget.pack(side='left', pady=15)
        self.enter_text_widget.bind('<Return>', self.on_enter_key_pressed)
        frame.pack(side='top')

    def on_join(self):
        if len(self.name_widget.get()) == 0:
            messagebox.showwarning("❌ warning","You should Login Frist... ❗")
            return
        self.name_widget.config(state='disabled')
        self.client_socket.send(("joined:" + self.name_widget.get()).encode('utf-8'))

    def display_login_registration(self):
        frame = Frame(bg="black")
        Label(frame, text='Username:', font=("Helvetica", 12), bg="black", fg="white").grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.name_widget = Entry(frame, width=50, borderwidth=2)
        self.name_widget.grid(row=0, column=1, padx=10, pady=5)

        Label(frame, text='Password:', font=("Helvetica", 12), bg="black", fg="white").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.password_widget = Entry(frame, width=50, borderwidth=2, show='*')
        self.password_widget.grid(row=1, column=1, padx=10, pady=5)

        login_register_frame = Frame(frame, bg="black")  # Create a new frame for the login and register buttons
        login_register_frame.grid(row=2, column=0, columnspan=2, pady=5)  # Set the frame's position and span it over two columns

        self.register_button = Button(login_register_frame, text="Register", width=10, command=self.register_user, bg="black", fg="white")
        self.register_button.pack(side='left', padx=(0, 5))  # Place the register button to the left with some padding

        self.login_button = Button(login_register_frame, text="Login", width=10, command=self.login_user, bg="black", fg="white")
        self.login_button.pack(side='left')  # Place the login button to the left of the register button

        frame.pack(side='top', anchor='nw')

    def register_user(self):
        username = self.name_widget.get()
        password = self.password_widget.get()
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return
        message = self.auth.register(username, password)
        messagebox.showinfo("Registration", message)

    def login_user(self):
        username = self.name_widget.get()
        password = self.password_widget.get()
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return
        message = self.auth.login(username, password)
        messagebox.showinfo("Login", message)

    def on_enter_key_pressed(self, event):
        if len(self.name_widget.get()) == 0:
            messagebox.showwarning("❌ warning","You should Login Frist... ❗")
            return
        self.send_chat()
        self.clear_text()

    def clear_text(self):
        self.enter_text_widget.delete(1.0, 'end')

    def send_chat(self):
        senders_name = self.name_widget.get().strip()
        data = self.enter_text_widget.get(1.0, 'end').strip()
        message = senders_name + ": " + data
        
        self.chat_transcript_area.insert('end', senders_name, 'blue')  # Insert username with 'blue' tag
        self.chat_transcript_area.insert('end', ": " + data + '\n')    # Insert message normally
        
        self.chat_transcript_area.yview(END)
        
        encoded_message = message.encode('utf-8')
        self.client_socket.send(encoded_message)
        
        self.enter_text_widget.delete(1.0, 'end')
        return 'break'

    def open_rooms_gui(self):
        rooms_window = Tk()
        rooms_app = RoomsGUI(rooms_window)

    def on_close_window(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            self.client_socket.close()
            exit(0)

# The main function 
if __name__ == '__main__':
    root = Tk()
    gui = GUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.on_close_window)
    root.mainloop()
