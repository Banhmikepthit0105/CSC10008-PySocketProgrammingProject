import tkinter as tk

class ClientApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.AutoScaleDimensions = (6, 13)
        self.AutoScaleMode = tk.constants.Font
        self.ClientSize = (372, 302)
        self.title("Client")

        self.butApp = tk.Button(self, text="App Running", command=self.butApp_Click)
        self.butApp.place(x=93, y=64, width=145, height=63)

        self.butConnect = tk.Button(self, text="Kết nối", command=self.butConnect_Click)
        self.butConnect.place(x=244, y=27, width=100, height=23)

        self.txtIP = tk.Entry(self)
        self.txtIP.insert(0, "Nhập IP")
        self.txtIP.place(x=12, y=29, width=226, height=20)

        self.butTat = tk.Button(self, text="Tắt máy", command=self.butTat_Click)
        self.butTat.place(x=93, y=133, width=48, height=57)

        self.butReg = tk.Button(self, text="Sửa registry", command=self.butReg_Click)
        self.butReg.place(x=93, y=196, width=198, height=65)

        self.butExit = tk.Button(self, text="Thoát", command=self.butExit_Click)
        self.butExit.place(x=297, y=196, width=47, height=65)

        self.butPic = tk.Button(self, text="Chụp màn hình", command=self.butPic_Click)
        self.butPic.place(x=147, y=133, width=91, height=57)

        self.butKeyLock = tk.Button(self, text="Keystroke", command=self.butKeyLock_Click)
        self.butKeyLock.place(x=244, y=64, width=100, height=126)

        self.butProcess = tk.Button(self, text="Process Running", command=self.butProcess_Click)
        self.butProcess.place(x=12, y=64, width=75, height=197)

        self.protocol("WM_DELETE_WINDOW", self.client_Closing)

    def butApp_Click(self):
        pass

    def butConnect_Click(self):
        pass

    def butTat_Click(self):
        pass

    def butReg_Click(self):
        pass

    def butExit_Click(self):
        pass

    def butPic_Click(self):
        pass

    def butKeyLock_Click(self):
        pass

    def butProcess_Click(self):
        pass

    def client_Closing(self):
        pass

if __name__ == "__main__":
    app = ClientApp()
    app.mainloop()
