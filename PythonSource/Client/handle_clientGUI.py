import tkinter as tk

class ClientApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Client")

        self.butApp = tk.Button(self, text="App Running", command=self.butApp_Click)
        self.butApp.pack()

        self.butConnect = tk.Button(self, text="Kết nối", command=self.butConnect_Click)
        self.butConnect.pack()

        self.txtIP = tk.Entry(self)
        self.txtIP.insert(0, "Nhập IP")
        self.txtIP.pack()

        self.butTat = tk.Button(self, text="Tắt máy", command=self.butTat_Click)
        self.butTat.pack()

        self.butReg = tk.Button(self, text="Sửa registry", command=self.butReg_Click)
        self.butReg.pack()

        self.butExit = tk.Button(self, text="Thoát", command=self.butExit_Click)
        self.butExit.pack()

        self.butPic = tk.Button(self, text="Chụp màn hình", command=self.butPic_Click)
        self.butPic.pack()

        self.butKeyLock = tk.Button(self, text="Keystroke", command=self.butKeyLock_Click)
        self.butKeyLock.pack()

        self.butProcess = tk.Button(self, text="Process Running", command=self.butProcess_Click)
        self.butProcess.pack()

    def butApp_Click(self):
        print("App Running")

    def butConnect_Click(self):
        print("Kết nối")

    def butTat_Click(self):
        print("Tắt máy")

    def butReg_Click(self):
        print("Sửa registry")

    def butExit_Click(self):
        print("Thoát")

    def butPic_Click(self):
        print("Chụp màn hình")

    def butKeyLock_Click(self):
        print("Keystroke")

    def butProcess_Click(self):
        print("Process Running")

app = ClientApp()
app.mainloop()
