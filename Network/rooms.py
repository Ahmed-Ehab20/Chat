from tkinter import Tk, Frame, Button, Label

class RoomsGUI:
    def __init__(self, master):
        self.root = master
        self.root.title("Available Chat Rooms")
        self.root.geometry("600x400")
        
        self.frame = Frame(self.root)
        self.frame.pack(pady=20)

        self.header_label = Label(self.frame, text="All Rooms available", font=("Helvetica", 12, "bold"), fg="blue")
        self.header_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.family_btn = Button(self.frame, text="Family", command=self.join_family_chat)
        self.family_btn.grid(row=1, column=0, padx=10, pady=5)

        self.work_btn = Button(self.frame, text="Work", command=self.join_work_chat)
        self.work_btn.grid(row=2, column=0, padx=10, pady=5)

        self.friends_btn = Button(self.frame, text="Friends", command=self.join_friends_chat)
        self.friends_btn.grid(row=3, column=0, padx=10, pady=5)

        self.jobs_btn = Button(self.frame, text="Jobs", command=self.join_jobs_chat)
        self.jobs_btn.grid(row=4, column=0, padx=10, pady=5)

    def join_family_chat(self):
        # Implement joining family chat room logic
        pass

    def join_work_chat(self):
        # Implement joining work chat room logic
        pass

    def join_friends_chat(self):
        # Implement joining friends chat room logic
        pass

    def join_jobs_chat(self):
        # Implement joining jobs chat room logic
        pass

if __name__ == "__main__":
    root = Tk()
    app = RoomsGUI(root)
    root.mainloop()
