import tkinter as tk


class MenuFrame(tk.Frame):
    """
    Меню. Колбэки:
      on_start_solved, on_start_random, on_load_file, on_exit
    """
    def __init__(self, master,
                 on_start_solved,
                 on_start_random,
                 on_load_file,
                 on_exit):
        super().__init__(master, bg="#222222")
        self.on_start_solved = on_start_solved
        self.on_start_random = on_start_random
        self.on_load_file = on_load_file
        self.on_exit = on_exit

        title = tk.Label(self, text="Rubik's Cube", fg="#FFFFFF", bg="#222222",
                         font=("Arial", 20, "bold"))
        title.pack(pady=20)

        btn1 = tk.Button(self, text="Начать со собранного", width=30,
                         command=self.on_start_solved)
        btn2 = tk.Button(self, text="Начать со случайного", width=30,
                         command=self.on_start_random)
        btn3 = tk.Button(self, text="Загрузить из файла…", width=30,
                         command=self.on_load_file)
        btn4 = tk.Button(self, text="Выйти", width=30,
                         command=self.on_exit)

        for b in (btn1, btn2, btn3, btn4):
            b.pack(pady=6)
