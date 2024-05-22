from tkinter import Tk, Frame, Scrollbar, Label, Entry, Text, Button, messagebox, Toplevel
from tkinter.constants import END as TK_END
import socket
import threading
from Auth import Auth
from rooms import RoomsGUI

class GUI:
    def __init__(self, master):
        self.auth = Auth("users.db")
        self.root = master
        self.chat_transcript_area = None
        self.name_widget = None
        self.enter_text_widget = None
        self.join_button = None
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(0.5)
        self.room_name = None

        self.root.title("Chat")
        self.root.resizable(0, 0)
        self.root.config(bg="black")  # Set window background color to black

        # Button for opening chat rooms window
        self.chat_rooms_btn = Button(self.root, text="Chat Rooms", command=self.open_rooms_gui, bg="black", fg="white")
        self.chat_rooms_btn.pack(side='top', anchor='nw', padx=10, pady=10)

        # Title in the middle
        self.title_label = Label(self.root, text="Live Chat Service", font=("Helvetica", 14, "bold"), bg="black", fg="white")
        self.title_label.pack()

        # Button for opening user window on top right
        self.users_button = Button(self.root, text="Users", command=self.show_registered_users, bg="black", fg="white")
        self.users_button.pack(side='top', anchor='ne', padx=10, pady=10)

        self.room_label = Label(self.root, text="In Room: None", font=("Helvetica", 12), bg="black", fg="white")
        self.room_label.pack()

        self.initialize_gui()
        self.listen_for_incoming_messages_in_a_thread()
        self.display_login_registration()

    def initialize_gui(self):
        self.display_chat_box()
        self.display_chat_entry_box()
        self.chat_transcript_area.tag_config('blue', foreground='blue', font=('Helvetica', 12, 'bold'))

    def listen_for_incoming_messages_in_a_thread(self):
        thread = threading.Thread(target=self.receive_message_from_server)
        thread.daemon = True
        thread.start()

    def receive_message_from_server(self):
        while True:
            try:
                buffer, _ = self.client_socket.recvfrom(1024)
                if buffer:
                    message = buffer.decode('utf-8')
                    self.update_chat_transcript_area(message)
            except socket.timeout:
                continue

    def update_chat_transcript_area(self, message):
        self.root.after(0, self._insert_message, message)

    def _insert_message(self, message):
        if "joined" in message:
            user = message.split(":")[1]
            message = user + " has joined"
            self.chat_transcript_area.insert(TK_END, message + '\n')
        else:
            sender, received_message = message.split(":", 1)
            self.chat_transcript_area.insert(TK_END, sender + ":", 'blue')
            self.chat_transcript_area.insert(TK_END, received_message + '\n')
        self.chat_transcript_area.yview(TK_END)

    def display_chat_box(self):
        frame = Frame(bg="black")
        Label(frame, text='Chat Box:', font=("Serif", 12), bg="black", fg="white").pack(side='top', anchor='w')
        self.chat_transcript_area = Text(frame, width=60, height=10, font=("Serif", 12), bg="black", fg="white")
        scrollbar = Scrollbar(frame, command=self.chat_transcript_area.yview)
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

    def on_enter_key_pressed(self, event):
        if len(self.name_widget.get()) == 0 or self.room_name is None:
            messagebox.showwarning("Warning", "You should login and join a room first.")
            return
        self.send_chat()
        return 'break'

    def send_chat(self):
        senders_name = self.name_widget.get().strip()
        data = self.enter_text_widget.get(1.0, TK_END).strip()
        if data:
            message = f"{senders_name}: {data}"
            self.chat_transcript_area.insert(TK_END, senders_name + ":", 'blue')
            self.chat_transcript_area.insert(TK_END, " " + data + '\n')
            self.chat_transcript_area.yview(TK_END)
            full_message = f"MSG|{self.room_name}|{message}"
            self.client_socket.sendto(full_message.encode('utf-8'), ('127.0.0.1', 10320))
            self.enter_text_widget.delete(1.0, TK_END)

    def display_login_registration(self):
        frame = Frame(bg="black")
        Label(frame, text='Username:', font=("Helvetica", 12), bg="black", fg="white").grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.name_widget = Entry(frame, width=50, borderwidth=2)
        self.name_widget.grid(row=0, column=1, padx=10, pady=5)

        Label(frame, text='Password:', font=("Helvetica", 12), bg="black", fg="white").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.password_widget = Entry(frame, width=50, borderwidth=2, show='*')
        self.password_widget.grid(row=1, column=1, padx=10, pady=5)

        self.register_button = Button(frame, text="Register", width=10, command=self.register_user, bg="black", fg="white")
        self.register_button.grid(row=2, column=0, padx=10, pady=5)

        self.login_button = Button(frame, text="Login", width=10, command=self.login_user, bg="black", fg="white")
        self.login_button.grid(row=2, column=1, padx=10, pady=5)

        Label(frame, text='Room Code/Name:', font=("Helvetica", 12), bg="black", fg="white").grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.room_widget = Entry(frame, width=50, borderwidth=2)
        self.room_widget.grid(row=3, column=1, padx=10, pady=5)

        self.create_room_button = Button(frame, text="Create Room", width=10, command=self.create_room, bg="black", fg="white")
        self.create_room_button.grid(row=4, column=0, padx=10, pady=5)

        self.join_room_button = Button(frame, text="Join Room", width=10, command=self.join_room, bg="black", fg="white")
        self.join_room_button.grid(row=4, column=1, padx=10, pady=5)

        frame.pack(side='top', anchor='n', pady=20)

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

    def create_room(self):
        room_name = self.room_widget.get()
        if not room_name:
            messagebox.showerror("Error", "Please enter a room name.")
            return
        self.client_socket.sendto(f"CREATE|{room_name}".encode('utf-8'), ('127.0.0.1', 10320))
        self.room_name = room_name
        self.update_current_room_label()

    def join_room(self):
        room_name = self.room_widget.get()
        username = self.name_widget.get().strip()
        if not room_name or not username:
            messagebox.showerror("Error", "Please enter both room name and username.")
            return
        self.client_socket.sendto(f"JOIN|{room_name}|{username}".encode('utf-8'), ('127.0.0.1', 10320))
        self.room_name = room_name
        self.update_current_room_label()

    def update_current_room_label(self):
        self.room_label.config(text=f"Current Room: {self.room_name}")

    def open_rooms_gui(self):
        rooms_window = Tk()
        rooms_app = RoomsGUI(rooms_window)

    def show_registered_users(self):
        users_window = Toplevel(self.root)
        users_window.title("Registered Users")
        
        users_frame = Frame(users_window, bg="black")
        users_frame.pack(padx=20, pady=20)
        
        users_label = Label(users_frame, text="Registered Users", font=("Helvetica", 12, "bold"), bg="black", fg="white")
        users_label.pack()
        
        users = self.auth.get_registered_users()  # Fetch registered users
        for user in users:
            user_label = Label(users_frame, text=user[0], font=("Helvetica", 10), bg="black", fg="white")
            user_label.pack(anchor='w')

    def on_close_window(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            self.client_socket.close()
            exit(0)

if __name__ == '__main__':
    root = Tk()
    gui = GUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.on_close_window)
    root.mainloop()
