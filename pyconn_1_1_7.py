import customtkinter
import socket
import tkinter.messagebox
import os
import time
import pickle
from PIL import Image, ImageTk
from tkinter import filedialog


customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")


class Client:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IP = '31.28.54.133'
        self.PORT = 25565
        self.data = None

    def server_data(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT

    def conn_serv(self):
        self.client.connect((self.IP, self.PORT))

    def send_data(self, data, status):
        self.data = (data + f'\n{status}').encode('utf-8')
        self.client.send(self.data)

    def get_data(self):
        self.data = self.client.recv(1024).decode()


class LogRegApp:

    def __init__(self):

        self.status = True
        self.app = customtkinter.CTk()
        self.app.geometry('450x320')
        self.app.title('Python Connect Версия 1_1_7!!!')
        self.app.resizable(False, False)
        self.tabview = customtkinter.CTkTabview(master=self.app, width=250)
        self.tabview.pack()
        self.tabview.add('Регистрация')
        self.tabview.add('Вход')

        self.loginr = customtkinter.CTkEntry(master=self.tabview.tab("Регистрация"), placeholder_text="Логин")
        self.loginr.pack(pady=10, padx=10)
        self.pswr = customtkinter.CTkEntry(master=self.tabview.tab("Регистрация"), placeholder_text="Пароль")
        self.pswr.pack(pady=10, padx=10)
        self.regdbtn = customtkinter.CTkButton(master=self.tabview.tab("Регистрация"), command=self.regbtn_callback, text='Ok')
        self.regdbtn.pack(pady=10, padx=10)

        self.login = customtkinter.CTkEntry(master=self.tabview.tab("Вход"), placeholder_text="Логин")
        self.login.pack(pady=10, padx=10)
        self.psw = customtkinter.CTkEntry(master=self.tabview.tab("Вход"), placeholder_text="Пароль", show='*')
        self.psw.pack(pady=10, padx=10)
        self.logdbtn = customtkinter.CTkButton(master=self.tabview.tab("Вход"), command=self.logbtn_callback, text='Ок')
        self.logdbtn.pack(pady=10, padx=10)

    def regbtn_callback(self):
        client = Client()
        client.conn_serv()
        client.send_data(f'{self.loginr.get()}\n{self.pswr.get()}', 'reg_func')
        client.get_data()
        self.open_dialog_event(client.data)

    def logbtn_callback(self):
        client = Client()
        client.conn_serv()
        client.send_data(f'{self.login.get()}\n{self.psw.get()}', 'log_func')
        client.get_data()
        data = client.data.split('\n')
        self.open_dialog_event(data[0])
        if data[1] == 'OK':
            self.app.destroy()
            app = MainProgram(data[2:-1])
            app.mainloop()

    @staticmethod
    def open_dialog_event(text):
        info = tkinter.messagebox
        info.showinfo(title='Информация', message=text)


class MainProgram(customtkinter.CTk):

    def __init__(self, user_data):
        super().__init__()

        self.user_data = None
        self.user_applications_to_friends = None
        self.user_friends = None
        self.read_ud(user_data)

        self.get_user_pfp()

        self.get_user_application_to_friends()
        self.get_user_friends()

        self.geometry('900x600')
        self.resizable(False, False)
        self.title('Python Connect версия 1_1_7!!!')

        # tkinter.messagebox.showinfo(title='Инфо', message='Укажите местоположение exe файла программы')
        # self.image_path = filedialog.askopenfilename().split(f"pyconn{version}.exe")[0] + 'images/'

        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join('images/', "icon_photo.png")), size=(100, 100))
        try:
            self.image_for_pfp = customtkinter.CTkImage(Image.open(os.path.join('images/', "pfp_image.png")), size=(150, 150))
        except:
            self.image_for_pfp = customtkinter.CTkImage(Image.open(os.path.join('images/', "pfp_image_standart.png")), size=(150, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join('images/', "image_icon_light.png")), size=(20, 20))
        self.myacc_image = customtkinter.CTkImage(Image.open(os.path.join('images/', "home_dark.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(Image.open(os.path.join('images/', "chat_dark.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(Image.open(os.path.join('images/', "add_user_dark.png")), size=(20, 20))
        self.accept_image = customtkinter.CTkImage(Image.open(os.path.join('images/', "accept.png")), size=(40, 40))
        self.decline_image = customtkinter.CTkImage(Image.open(os.path.join('images/', "decline.png")), size=(40, 40))
        self.background_image = customtkinter.CTkImage(Image.open(os.path.join('images/', "bg_gradient.jpg")), size=(1000, 600))
        self.exit_image = customtkinter.CTkImage(Image.open(os.path.join('images/', "exit_btn.png")), size=(20, 20))
        self.logout_image = customtkinter.CTkImage(Image.open(os.path.join('images/', "logout_btn.png")), size=(20, 20))
        self.send_message_image = customtkinter.CTkImage(Image.open(os.path.join('images/', "send_message.png")), size=(25, 25))

        icon_photo = ImageTk.PhotoImage(file='images/icon_photo.png')

        self.iconphoto(False, icon_photo)

        self.navframe = customtkinter.CTkFrame(self, corner_radius=25)
        self.navframe.grid(row=0, column=0, sticky="nsew")
        self.navframe.grid_rowconfigure(4, weight=1)

        self.navframe_label = customtkinter.CTkLabel(self.navframe, text="  Pyconn", image=self.logo_image,
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=25, weight="bold"))
        self.navframe_label.grid(row=0, column=0, padx=20, pady=20)

        self.myacc_button = customtkinter.CTkButton(self.navframe, corner_radius=0, height=40, border_spacing=10,
                                                   text="Мой аккаунт",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.myacc_image, anchor="w", command=self.myacc_button_event)
        self.myacc_button.grid(row=1, column=0, sticky="ew")

        self.messenger_button = customtkinter.CTkButton(self.navframe, corner_radius=0, height=40,
                                                      border_spacing=10, text="Мессенджер",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w",
                                                      command=self.frame_2_button_event)
        self.messenger_button.grid(row=2, column=0, sticky="ew")

        self.friends_button = customtkinter.CTkButton(self.navframe, corner_radius=0, height=40,
                                                      border_spacing=10, text="Друзья",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w",
                                                      command=self.frame_3_button_event)
        self.friends_button.grid(row=3, column=0, sticky="ew")

        self.myacc_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color='transparent')
        self.myacc_frame.grid_columnconfigure(0, weight=1)
        self.myacc_frame_login = customtkinter.CTkLabel(self.myacc_frame, text="login: " + self.user_data.get('login'),
                                                       font=customtkinter.CTkFont(size=12, family='Impact'),
                                                       anchor='center', bg_color="#dbdbdb", width=150)
        self.myacc_frame_login.grid(row=0, column=0, sticky='n', pady=5)
        self.myacc_frame_id = customtkinter.CTkLabel(self.myacc_frame, text="id: " + self.user_data.get('id'),
                                                        font=customtkinter.CTkFont(size=12, family='Impact'),
                                                        anchor='center', bg_color="#dbdbdb", width=150)
        self.myacc_frame_id.grid(row=0, column=1, sticky='nw', pady=5)
        self.myacc_frame_pfp = customtkinter.CTkLabel(self.myacc_frame, text="", image=self.image_for_pfp)
        self.myacc_frame_pfp.grid(row=1, column=0, padx=25, sticky='e')
        self.myacc_frame_choose_pfp_btn = customtkinter.CTkButton(self.myacc_frame, text="Выбрать ФП",
                                                                 font=customtkinter.CTkFont(size=10, family='fixed'),
                                                                 command=lambda: self.save_user_pfp(), width=20, text_color="black",
                                                                 anchor='center', fg_color="#d9d9d9", hover_color="#b5baba")
        self.myacc_frame_choose_pfp_btn.grid(row=2, column=0, sticky='n', pady=10)
        self.myacc_frame_name = customtkinter.CTkLabel(self.myacc_frame, text=self.user_data.get('name'),
                                                       font=customtkinter.CTkFont(size=26, family='Comic Sans MS'),
                                                       anchor='s', bg_color="#dbdbdb")
        self.myacc_frame_name.grid(row=1, column=1, padx=1, pady=5, sticky='sw')
        self.myacc_frame_profile_status = customtkinter.CTkLabel(self.myacc_frame, text=self.user_data.get('status'),
                                                                 font=customtkinter.CTkFont(size=18, family='Comic Sans MS'),
                                                                 anchor='center', bg_color="#dbdbdb")
        self.myacc_frame_profile_status.grid(row=2, column=1, sticky='nw', pady=10)
        self.myacc_frame_settings_btn = customtkinter.CTkButton(self.myacc_frame, text="Настройки",
                                                                 font=customtkinter.CTkFont(size=14, family='fixed'),
                                                                 command=lambda: self.show_settings_btns(), width=30, height=10, text_color="black",
                                                                 anchor='s', fg_color="#d9d9d9", hover_color="#b5baba")
        self.myacc_frame_settings_btn.grid(row=3, column=0, sticky='s', pady=75)


        self.messager_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.messager_frame_scrollable_frame = customtkinter.CTkScrollableFrame(self.messager_frame, width=600, height=500, fg_color='transparent')
        self.messager_frame_scrollable_frame.grid(row=0, column=0, sticky='nsew', padx=25, pady=25)

        self.friends_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.friends_frame_tabview = customtkinter.CTkTabview(self.friends_frame, height=575, width=600)
        self.friends_frame_tabview.grid(sticky="n", padx=19, pady=5)
        self.friends_frame_tabview.add("Друзья")
        self.friends_frame_tabview.add("Добавить в друзья")
        self.friends_frame_tabview.add("Заявки в друзья")

        self.friends_frame_add_friend_entry = customtkinter.CTkEntry(self.friends_frame_tabview.tab("Добавить в друзья"),
                                                                     placeholder_text="Введите ID/Login того, кого хотите добавить...",
                                                                     font=customtkinter.CTkFont(size=18, family="fixed"),
                                                                     width=500, height=50)
        self.friends_frame_add_friend_entry.grid(row=1, column=0, padx=15, pady=15, sticky="n")
        self.friends_frame_add_friend_btn = customtkinter.CTkButton(self.friends_frame_tabview.tab("Добавить в друзья"),
                                                                    font=customtkinter.CTkFont(size=18, family="fixed"),
                                                                    text="Добавить в друзья", command=lambda: self.add_friend_btn())
        self.friends_frame_add_friend_btn.grid(row=2, column=0, pady=15, padx=15, sticky='w')
        self.friends_frame_application_friends_scrollable_list = customtkinter.CTkScrollableFrame(
                                                        self.friends_frame_tabview.tab("Заявки в друзья"),
                                                        height=510, width=550)
        self.friends_frame_application_friends_scrollable_list.grid(row=0, column=0, sticky="n", padx=10)
        """ self.friends_frame_add_friend_lbl = customtkinter.CTkLabel(self.friends_frame_tabview.tab("Добавить в друзья"),
                                                                   font=customtkinter.CTkFont(size=18, family="fixed"),
                                                                   text="")
        self.friends_frame_add_friend_lbl.grid(row=3, column=0, pady=15, padx=15, sticky="w") """
        self.friends_frame_friends_scrollable_list = customtkinter.CTkScrollableFrame(self.friends_frame_tabview.tab("Друзья"),
                                                                                      height=510, width=550)
        self.friends_frame_friends_scrollable_list.grid(row=0, column=0, sticky="n", padx=10)

        self.select_frame_by_name("myacc")

        self.empty_lbl = customtkinter.CTkLabel(self.navframe, text='')
        self.empty_lbl.grid(row=5, column=0, pady=100)

        self.exit_button = customtkinter.CTkButton(self.navframe, corner_radius=0, text='Выход', command=lambda: self.close(),
                                                   text_color='black', fg_color="gray85", hover_color="gray75", anchor='w',
                                                   height=42, image=self.exit_image, border_spacing=10)
        self.exit_button.grid(row=7, column=0, sticky="nsew")
        self.logout_button = customtkinter.CTkButton(self.navframe, corner_radius=0, fg_color="gray85", hover_color="gray75",
                                                     text='Разлогиниться', command=lambda: self.logout(), text_color='black',
                                                     anchor='w', height=42, font=customtkinter.CTkFont(size=13), border_spacing=10,
                                                     image=self.logout_image)
        self.logout_button.grid(row=6, column=0, sticky="ew")

        self.refresh_btn = customtkinter.CTkButton(
            self.navframe, text="Обновить", command=lambda: self.refresh_command_btn(),
            corner_radius=0, fg_color='gray85', hover_color='gray75', anchor='w',
            height=42, font=customtkinter.CTkFont(size=13), border_spacing=10, text_color='black'
        )
        self.refresh_btn.grid(row=5, column=0, sticky='nsew')

        if self.user_applications_to_friends is not None:
            self.load_friends_application()

        if self.user_friends is not None:
            self.load_friends()
            self.load_message_btns()

    def refresh_command_btn(self):
        try:
            for el in self.friends_frame_dict.values():
                el.destroy()
        except Exception:
            pass

        try:
            for el in self.frame_list.values():
                el.destroy()
        except Exception:
            pass

        try:
            for el in self.messager_frame_dict.values():
                el.destroy()
        except Exception:
            pass

        self.get_user_application_to_friends()
        self.get_user_friends()

        if self.user_applications_to_friends is not None:
            self.load_friends_application()

        if self.user_friends is not None:
            self.load_friends()
            self.load_message_btns()


    def load_friends(self):
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.friends_frame_dict = {}
        for ell in self.user_friends:
            client = Client()
            client.conn_serv()
            client.send_data(f"{ell}", "get_user_data")
            client.get_data()
            friend_data = self.read_fd(client.data.split('\n')[:-1])
            self.get_friend_pfp(ell)
            image_for_pfp = customtkinter.CTkImage(Image.open(os.path.join('images/', "friend_pfp_image.png")), size=(75, 75))
            self.friends_frame_friend_frame = customtkinter.CTkFrame(master=self.friends_frame_friends_scrollable_list, width=550, height=100)
            self.friends_frame_friend_frame.grid(row=self.user_friends.index(ell), column=0, pady=15)
            self.friends_frame_friend_frame_friend_pfp = customtkinter.CTkLabel(self.friends_frame_friend_frame, text="", image=image_for_pfp)
            self.friends_frame_friend_frame_friend_pfp.grid(sticky='w', column=0, row=0, padx=15, pady=15)
            self.friends_frame_friend_frame_friend_name = customtkinter.CTkLabel(self.friends_frame_friend_frame, text=friend_data.get("name"),
                                                                                font=customtkinter.CTkFont(size=18, family="fixed"), width=250, anchor='w')
            self.friends_frame_friend_frame_friend_name.grid(sticky='w', column=1, row=0, padx=10)
            self.friends_frame_friend_frame_show_profile_btn = customtkinter.CTkButton(
                self.friends_frame_friend_frame, text="Профиль", corner_radius=0, text_color='black',
                font=customtkinter.CTkFont(size=12, family="fixed"), fg_color="gray75", hover_color="gray80",
                anchor='w', command=lambda friend_data=friend_data:
                self.show_friend_profile(friend_data))
            self.friends_frame_friend_frame_delete_btn = customtkinter.CTkButton(
                self.friends_frame_friend_frame, text="Убрать из друзей", corner_radius=0, text_color='black',
                font=customtkinter.CTkFont(size=12, family="fixed"), fg_color="gray75", hover_color="gray80",
                anchor='w', command=lambda ell=ell:self.delete_friend(ell))
            self.friends_frame_friend_frame_block_btn = customtkinter.CTkButton(
                self.friends_frame_friend_frame, text="Заблокировать", corner_radius=0,
                font=customtkinter.CTkFont(size=12, family="fixed"),
                anchor='w', fg_color="#bc3124", hover_color="#96271d",
                command=lambda ell=ell:self.block_friend(ell))
            self.friends_frame_friend_frame_show_profile_btn.grid(row=0, column=2, sticky='n', pady=15, padx=15)
            self.friends_frame_friend_frame_delete_btn.grid(row=1, column=2, sticky='s')
            self.friends_frame_friend_frame_block_btn.grid(row=2, column=2, sticky='s', pady=10)
            self.friends_frame_dict[ell] = self.friends_frame_friend_frame

    def load_message_btns(self):
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.messager_frame_dict = {}
        for el in self.user_friends:
            client = Client()
            client.conn_serv()
            client.send_data(f"{el}", "get_user_data")
            client.get_data()
            friend_data = self.read_fd(client.data.split('\n')[:-1])
            self.get_friend_pfp(el)
            image_for_pfp = customtkinter.CTkImage(Image.open(os.path.join('images/', "friend_pfp_image.png")), size=(50, 50))
            self.messager_frame_chat_btn = customtkinter.CTkButton(
                master=self.messager_frame_scrollable_frame, corner_radius=15, command=lambda el=el: self.open_chat_with(el),
                width=550, height=55, text=f"{friend_data.get('name')}", fg_color='gray85', font=customtkinter.CTkFont(size=15, weight='bold'),
                image=image_for_pfp, anchor='w', hover_color="gray75", text_color='black', border_color='gray65', border_width=1)
            self.messager_frame_chat_btn.grid(row=self.user_friends.index(el), column=0, pady=3, sticky='nsew')
            self.messager_frame_dict[el] = self.messager_frame_chat_btn

    def open_chat_with(self, friend_id):
        self.messager_frame_scrollable_frame.grid_forget()
        self.chat_frame = customtkinter.CTkScrollableFrame(self.messager_frame, width=600, height=470)
        self.chat_frame.grid(row=2, column=0, padx=10, columnspan=2)
        self.chat_frame_entry = customtkinter.CTkEntry(self.messager_frame, width=565, height=30, placeholder_text='Напишите сообщение...')
        self.chat_frame_entry.grid(row=1, column=0, padx=10)
        # self.chat_frame_entry_message = customtkinter.CTkEntry()
        self.open_chat_with_back_btn = customtkinter.CTkButton(self.messager_frame, text='Назад', command=lambda: self.back_from_chat_btn())
        self.open_chat_with_back_btn.grid(row=0, column=0, pady=15)
        client = Client()
        client.conn_serv()
        client.send_data(f"{friend_id}", 'get_user_data')
        client.get_data()
        friend_data = self.read_fd(client.data.split('\n')[:-1])
        self.get_friend_pfp(friend_id)
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        image_for_pfp = customtkinter.CTkImage(Image.open(os.path.join('images/', "friend_pfp_image.png")), size=(50, 50))
        user_image_for_pfp = customtkinter.CTkImage(Image.open(os.path.join('images/', "pfp_image.png")), size=(50, 50))
        client = Client()
        client.conn_serv()
        client.send_data(self.user_data.get("id"), "get_user_messages")
        data = client.client.recv(4096)
        messages = pickle.loads(data, encoding='utf-8')
        self.chat_frame_send_message_btn = customtkinter.CTkButton(
            self.messager_frame, text='', image=self.send_message_image, command=lambda: self.chat_send_message(friend_id),
            width=1, fg_color='transparent', anchor='w', hover_color='gray85')
        self.chat_frame_send_message_btn.grid(row=1, column=1)
        cnt = 0
        for el in messages[::-1]:
            sendrec, message = el.split('>>>')
            sender, reciever = sendrec.split('=')
            if (sender != friend_id) and (reciever != friend_id):
                continue
            if sender != self.user_data.get('id'):
                self.message_from_friend_frame = customtkinter.CTkFrame(
                    self.chat_frame, width=550)
                self.message_from_friend_frame.grid(row=cnt, column=0, sticky='ew', pady=10)
                self.message_from_friend_frame_pfp = customtkinter.CTkLabel(
                    self.message_from_friend_frame, anchor='w', text='', image=image_for_pfp)
                self.message_from_friend_frame_pfp.grid(row=0, column=0, rowspan=2, padx=25)
                self.message_from_friend_frame_name = customtkinter.CTkLabel(
                    self.message_from_friend_frame, text=friend_data.get('name'), anchor='nw',
                    font=customtkinter.CTkFont(size=14, weight='bold'), width=1)
                self.message_from_friend_frame_name.grid(row=0, column=1, sticky='nw')
                self.message_from_friend_frame_message = customtkinter.CTkLabel(
                    self.message_from_friend_frame, text=message, anchor='w', width=1)
                self.message_from_friend_frame_message.grid(row=1, column=1)
            if sender == self.user_data.get('id'):
                self.message_from_friend_frame = customtkinter.CTkFrame(
                    self.chat_frame, width=550)
                self.message_from_friend_frame.grid(row=cnt, column=0, sticky='we', pady=10)
                self.message_from_friend_frame_pfp = customtkinter.CTkLabel(
                    self.message_from_friend_frame, anchor='e', text='', image=user_image_for_pfp)
                self.message_from_friend_frame_pfp.grid(row=0, column=0, rowspan=2, padx=25, sticky='w')
                self.message_from_friend_frame_name = customtkinter.CTkLabel(
                    self.message_from_friend_frame, text=self.user_data.get('name'), anchor='nw',
                    font=customtkinter.CTkFont(size=14, weight='bold'), width=1)
                self.message_from_friend_frame_name.grid(row=0, column=1, sticky='nw')
                self.message_from_friend_frame_message = customtkinter.CTkLabel(
                    self.message_from_friend_frame, text=message, anchor='w', width=1)
                self.message_from_friend_frame_message.grid(row=1, column=1, sticky='w')
            cnt += 1

    def chat_send_message(self, friend_id):
        user_image_for_pfp = customtkinter.CTkImage(Image.open(os.path.join('images/', "pfp_image.png")), size=(50, 50))
        message = self.chat_frame_entry.get()
        if message in ('', ' ', '  ', '   '):
            tkinter.messagebox.showwarning(title='Предупреждение', message='Ваше сообщение пустое!')
            return
        receiver = friend_id
        sender = self.user_data.get('id')
        client = Client()
        client.conn_serv()
        client.send_data(f'{sender}\n{receiver}\n{message}', 'chat_send_message')
        self.back_from_chat_btn()
        self.open_chat_with(friend_id)

    def back_from_chat_btn(self):
        self.chat_frame.grid_forget()
        self.open_chat_with_back_btn.destroy()
        self.chat_frame_entry.destroy()
        self.chat_frame_send_message_btn.destroy()
        self.refresh_command_btn()
        self.messager_frame_scrollable_frame.grid(row=0, column=0, sticky='nsew', padx=25, pady=25)

    def show_friend_profile(self, friend_data):
        self.friends_frame_tabview.grid_forget()
        self.get_friend_pfp(friend_data.get('id'))
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        image_for_pfp = customtkinter.CTkImage(Image.open(os.path.join('images/', "friend_pfp_image.png")), size=(150, 150))
        self.friends_frame_frame = customtkinter.CTkFrame(self.friends_frame, fg_color='transparent')
        self.friends_frame_frame.grid(sticky='nsew')
        self.friend_frame_login = customtkinter.CTkLabel(self.friends_frame_frame, text="login: " + friend_data.get('login'),
                                                        font=customtkinter.CTkFont(size=12, family='Impact'),
                                                        anchor='center', bg_color="#dbdbdb", width=150)
        self.friend_frame_login.grid(row=0, column=0, sticky='n', pady=5)
        self.friend_frame_id = customtkinter.CTkLabel(self.friends_frame_frame, text="id: " + friend_data.get('id'),
                                                     font=customtkinter.CTkFont(size=12, family='Impact'),
                                                     anchor='center', bg_color="#dbdbdb", width=150)
        self.friend_frame_id.grid(row=0, column=1, sticky='nw', pady=5)
        self.friend_frame_pfp = customtkinter.CTkLabel(self.friends_frame_frame, text="", image=image_for_pfp)
        self.friend_frame_pfp.grid(row=1, column=0, padx=25, sticky='e')
        self.friend_frame_name = customtkinter.CTkLabel(self.friends_frame_frame, text=friend_data.get('name'),
                                                       font=customtkinter.CTkFont(size=26, family='Comic Sans MS'),
                                                       anchor='s', bg_color="#dbdbdb")
        self.friend_frame_name.grid(row=1, column=1, padx=1, pady=5, sticky='sw')
        self.friend_frame_profile_status = customtkinter.CTkLabel(self.friends_frame_frame, text=friend_data.get('status'),
                                                                 font=customtkinter.CTkFont(size=18,
                                                                                            family='Comic Sans MS'),
                                                                 anchor='center', bg_color="#dbdbdb")
        self.friend_frame_profile_status.grid(row=2, column=1, sticky='nw', pady=10)
        self.friends_frame_back_btn = customtkinter.CTkButton(self.friends_frame_frame, text='Назад',
                                                              font=customtkinter.CTkFont(size=18, family='Comic Sans MS'),
                                                              command=lambda: self.friend_frame_back_btn())
        self.friends_frame_back_btn.grid(row=3, column=0, columnspan=4)

    def friend_frame_back_btn(self):
        self.friends_frame_frame.destroy()
        self.friends_frame_tabview.grid(sticky="n", padx=19, pady=5)
        self.refresh_command_btn()

    def block_friend(self, ell):
        self.delete_friend(ell)
        client = Client()
        client.conn_serv()
        client.send_data(f"{self.user_data.get('id')}\n{ell}", "block_friend")
        client.get_data()
        if client.data != "OK":
            raise ValueError("Непредвиденная ошибка")
            return

    def delete_friend(self, ell):
        client = Client()
        client.conn_serv()
        client.send_data(f"{self.user_data.get('id')}\n{ell}", "delete_friend")
        client.get_data()
        if client.data != "OK":
            raise ValueError("Непредвиденная ошибка")
            return
        self.friends_frame_dict.get(ell).destroy()

    def load_friends_application(self):
        cnt = 0
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.frame_list = {}
        self.friends_aplic_btn_dict = {}
        for el in self.user_applications_to_friends:
            client = Client()
            client.conn_serv()
            client.send_data(f"{el}", "get_user_data")
            client.get_data()
            friend_data = self.read_fd(client.data.split('\n')[:-1])
            self.get_friend_pfp(el)
            image_for_pfp = customtkinter.CTkImage(Image.open(os.path.join('images/', "friend_pfp_image.png")), size=(75, 75))
            self.friends_frame_aplic_friend_frame = customtkinter.CTkFrame(master=self.friends_frame_application_friends_scrollable_list,
                                                                           width=550, height=100)
            self.friends_frame_aplic_friend_frame.grid(row=cnt, column=0, pady=15)
            self.friends_frame_aplic_friend_frame_friend_pfp = customtkinter.CTkLabel(self.friends_frame_aplic_friend_frame, text="", image=image_for_pfp)
            self.friends_frame_aplic_friend_frame_friend_pfp.grid(sticky='w', column=0, row=0, padx=15, pady=15)
            self.friends_frame_aplic_friend_frame_friend_name = customtkinter.CTkLabel(self.friends_frame_aplic_friend_frame, text=friend_data.get("name"),
                                                                                       font=customtkinter.CTkFont(size=18, family="fixed"), width=250, anchor='w')
            self.friends_frame_aplic_friend_frame_friend_name.grid(sticky='w', column=1, row=0, padx=10)
            self.friends_frame_aplic_friend_frame_accept_btn = customtkinter.CTkButton(self.friends_frame_aplic_friend_frame, text='', fg_color='gray85',
                                                                                   image=self.accept_image, width=50, height=50, anchor='e', hover_color="gray75",
                                                                                       command=lambda el=el: self.accept_friend_aplic_btn(el))
            self.friends_frame_aplic_friend_frame_accept_btn.grid(sticky='e', column=3, row=0, padx=5)
            self.friends_aplic_btn_dict[el] = self.friends_frame_aplic_friend_frame_accept_btn
            self.friends_frame_aplic_friend_frame_decline_btn = customtkinter.CTkButton(self.friends_frame_aplic_friend_frame, text='', fg_color='gray85',
                                                                                        hover_color="gray75", command=lambda el=el: self.decline_friend_aplic_btn(el),
                                                                                       image=self.decline_image, width=50, height=50, anchor='e')
            self.friends_frame_aplic_friend_frame_decline_btn.grid(sticky='e', column=4, row=0, padx=15)
            self.frame_list[el] = self.friends_frame_aplic_friend_frame
            cnt += 1

    def accept_friend_aplic_btn(self, el):
        client = Client()
        client.conn_serv()
        client.send_data(f"{self.user_data.get('id')}\n{el}", "accept_friend_aplic")
        client.get_data()
        if client.data != "OK":
            raise ValueError("Непредвиденная ошибка")
            return
        self.frame_list.get(el).destroy()
        self.get_user_friends()
        self.load_friends()

    def decline_friend_aplic_btn(self, el):
        client = Client()
        client.conn_serv()
        client.send_data(f"{self.user_data.get('id')}\n{el}", "decline_friend_aplic")
        client.get_data()
        if client.data != "OK":
            raise ValueError("Непредвиденная ошибка")
            return
        self.frame_list.get(el).destroy()

    def get_user_application_to_friends(self):
        client = Client()
        client.conn_serv()
        client.send_data(self.user_data.get('id'), "send_user_application_to_friends")
        client.get_data()
        self.user_applications_to_friends = []
        for el in client.data.split('\n')[:-1]:
            if el is None or el == '':
                self.user_applications_to_friends = None
                break
            self.user_applications_to_friends.append(el)

    def get_user_friends(self):
        client = Client()
        client.conn_serv()
        client.send_data(self.user_data.get('id'), "send_user_friends")
        client.get_data()
        self.user_friends = []
        for el in client.data.split('\n')[:-1]:
            if el is None or el == '':
                self.user_friends = None
                break
            self.user_friends.append(el)

    def add_friend_btn(self):
        login = id = self.friends_frame_add_friend_entry.get()
        self.friends_frame_add_friend_entry.clipboard_clear()
        client = Client()
        client.conn_serv()
        client.send_data(f"{id}\n{login}\n{self.user_data.get('id')}", "add_friend")
        client.get_data()
        if client.data != "OK":
            tkinter.messagebox.showwarning(title="Предупреждение", message=client.data)
            return
        tkinter.messagebox.showinfo(title='Информация', message="Заявка успешно отправлена!")

    def show_settings_btns(self):
        self.myacc_frame_change_password = customtkinter.CTkButton(self.myacc_frame, text="Сменить пароль",
                                                                font=customtkinter.CTkFont(size=14, family='fixed'),
                                                                width=50, command=lambda: self.save_new_password(),
                                                                height=10, text_color="black",
                                                                anchor='center', fg_color="#d9d9d9", hover_color="#b5baba")
        self.myacc_frame_change_password.grid(row=4, column=0, sticky='s', pady=5)
        self.myacc_frame_login.destroy()
        self.myacc_frame_login_entry = customtkinter.CTkEntry(self.myacc_frame, placeholder_text="login: " + self.user_data.get('login'),
                                                        font=customtkinter.CTkFont(size=12, family='Impact'),
                                                        bg_color="#dbdbdb", width=150)
        self.myacc_frame_login_entry.grid(row=0, column=0, sticky='n', pady=5)
        self.myacc_frame_name.destroy()
        self.myacc_frame_name_entry = customtkinter.CTkEntry(self.myacc_frame, placeholder_text=self.user_data.get('name'), width=300,
                                                       font=customtkinter.CTkFont(size=26, family='Comic Sans MS'), bg_color="#dbdbdb")
        self.myacc_frame_name_entry.grid(row=1, column=1, padx=1, pady=5, sticky='sw')
        self.myacc_frame_profile_status.destroy()

        self.myacc_frame_profile_status_entry = customtkinter.CTkEntry(self.myacc_frame, placeholder_text=self.user_data.get('status'), width=300,
                                                                 font=customtkinter.CTkFont(size=18, family='Comic Sans MS'), bg_color="#dbdbdb")
        self.myacc_frame_profile_status_entry.grid(row=2, column=1, sticky='nw', pady=10)
        self.myacc_frame_settings_btn.destroy()
        self.myacc_frame_settings_btn = customtkinter.CTkButton(self.myacc_frame, text="OK",
                                                                font=customtkinter.CTkFont(size=14, family='fixed'),
                                                                width=50, command=lambda: self.save_new_profile_data(),
                                                                height=10, text_color="black",
                                                                anchor='s', fg_color="#d9d9d9", hover_color="#b5baba")
        self.myacc_frame_settings_btn.grid(row=3, column=0, sticky='n', pady=5)
        self.myacc_frame_settings_btn_cancel = customtkinter.CTkButton(self.myacc_frame, text="Отмена",
                                                                font=customtkinter.CTkFont(size=14, family='fixed'),
                                                                width=50, command=lambda: self.cancel_new_data(),
                                                                height=10, text_color="black",
                                                                anchor='s', fg_color="#d9d9d9", hover_color="#b5baba")
        self.myacc_frame_settings_btn_cancel.grid(row=5, column=0, sticky='s', pady=5)

    def save_new_password(self):
        dialog = customtkinter.CTkInputDialog(text="Введите старый пароль:", title="Сменить пароль")
        text = dialog.get_input()
        if text != self.user_data.get('password'):
            tkinter.messagebox.showerror(title="Ошибка", message="Неверный пароль!\nПрограмма разлогинит вас за подозрительные действия...")
            self.logout()
        dialog = customtkinter.CTkInputDialog(text="Введите новый пароль:", title="Сменить пароль")
        password = dialog.get_input()
        client = Client()
        client.conn_serv()
        client.send_data(f"{id}\n{password}", "change_password")
        client.get_data()
        report = client.data
        if report != "OK":
            tkinter.messagebox.showinfo(title="Информация", message=report)
            return
        elif report == "OK":
            tkinter.messagebox.showinfo(title="Информация", message="Пароль успешно сменён")
        client = Client()
        client.conn_serv()
        client.send_data(f'{self.user_data.get("id")}', 'get_user_data')
        client.get_data()
        user_data = client.data.split("\n")[:-1]
        self.read_ud(user_data)
        self.cancel_new_data()

    def cancel_new_data(self):
        self.myacc_frame_name_entry.destroy()
        self.myacc_frame_login_entry.destroy()
        self.myacc_frame_profile_status_entry.destroy()
        self.myacc_frame_settings_btn_cancel.destroy()
        self.myacc_frame_settings_btn.destroy()
        self.myacc_frame_change_password.destroy()
        self.myacc_frame_settings_btn = customtkinter.CTkButton(self.myacc_frame, text="Настройки",
                                                                font=customtkinter.CTkFont(size=14, family='fixed'),
                                                                command=lambda: self.show_settings_btns(), width=30,
                                                                height=10, text_color="black",
                                                                anchor='s', fg_color="#d9d9d9", hover_color="#b5baba")
        self.myacc_frame_settings_btn.grid(row=3, column=0, sticky='s', pady=75)
        self.myacc_frame_name = customtkinter.CTkLabel(self.myacc_frame, text=self.user_data.get('name'),
                                                       font=customtkinter.CTkFont(size=26, family='Comic Sans MS'),
                                                       anchor='s', bg_color="#dbdbdb")
        self.myacc_frame_name.grid(row=1, column=1, padx=1, pady=5, sticky='sw')
        self.myacc_frame_profile_status = customtkinter.CTkLabel(self.myacc_frame, text=self.user_data.get('status'),
                                                                 font=customtkinter.CTkFont(size=18,
                                                                                            family='Comic Sans MS'),
                                                                 anchor='center', bg_color="#dbdbdb")
        self.myacc_frame_profile_status.grid(row=2, column=1, sticky='nw', pady=10)
        self.myacc_frame_login = customtkinter.CTkLabel(self.myacc_frame, text="login: " + self.user_data.get('login'),
                                                        font=customtkinter.CTkFont(size=12, family='Impact'),
                                                        anchor='center', bg_color="#dbdbdb", width=150)
        self.myacc_frame_login.grid(row=0, column=0, sticky='n', pady=5)

    def save_new_profile_data(self):
        status = self.myacc_frame_profile_status_entry.get()
        name = self.myacc_frame_name_entry.get()
        login = self.myacc_frame_login_entry.get()
        client = Client()
        client.conn_serv()
        client.send_data(f"{self.user_data.get('id')}\n{login}\n{name}\n{status.replace('=', '€')}", "update_user_data")
        client.get_data()
        if client.data != "OK":
            tkinter.messagebox.showinfo(title="Информация", message=client.data)
            return
        client = Client()
        client.conn_serv()
        client.send_data(f'{self.user_data.get("id")}', 'get_user_data')
        client.get_data()
        user_data = client.data.split("\n")[:-1]
        self.read_ud(user_data)
        self.cancel_new_data()

    def select_frame_by_name(self, name):
        self.myacc_button.configure(fg_color=("gray75", "gray25") if name == "myacc" else "transparent")
        self.messenger_button.configure(fg_color=("gray75", "gray25") if name == "messenger" else "transparent")
        self.friends_button.configure(fg_color=("gray75", "gray25") if name == "friends" else "transparent")

        if name == "myacc":
            self.myacc_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.myacc_frame.grid_forget()
        if name == "messenger":
            self.messager_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.messager_frame.grid_forget()
        if name == "friends":
            self.friends_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.friends_frame.grid_forget()

    def myacc_button_event(self):
        self.select_frame_by_name("myacc")

    def frame_2_button_event(self):
        self.select_frame_by_name("messenger")

    def frame_3_button_event(self):
        self.select_frame_by_name("friends")

    def close(self):
        with open('reme/status.txt', 'w', encoding='utf-8') as file:
            file.write(f'status=True\nid={self.user_data.get("id")}')
        self.destroy()

    def logout(self):
        with open('reme/status.txt', 'w', encoding='utf-8') as file:
            file.write(f'status=False\nid=None')
        self.destroy()
        logreg = LogRegApp()
        logreg.app.mainloop()

    def save_user_pfp(self):
        print('getting file...')
        name = filedialog.askopenfilename()
        nn = name
        if nn.split('.')[-1] not in ('jpg', 'jpeg', 'png'):
            tkinter.messagebox.showerror(title='Ошибка', message='Допустимы только форматы .png, .jpg')
            return
        file_size = os.path.getsize(name)
        print(f'file_size -> {file_size}')
        file = open(name, "rb")
        if int(file_size) > 27000000:
            tkinter.messagebox.showerror(title='Информация', message='Максимальный допустимый размер изображения - 25МБ')
            return
        client = Client()
        print("Creating Client")
        client.conn_serv()
        print("Connecting to Server")
        data = file.read()
        client.send_data(f"{self.user_data.get('id')}.png\n{str(file_size)}", "save_user_pfp")
        time.sleep(1)
        print("Sended begin data -> listen for OK...")
        client.client.sendall(data)
        client.client.send(b"<END>")
        pfp_image = open("images/pfp_image.png", "wb")
        pfp_image.write(data)
        pfp_image.close()
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.image_for_pfp = customtkinter.CTkImage(Image.open(os.path.join('images/', "pfp_image.png")), size=(150, 150))
        self.myacc_frame_pfp.destroy()
        self.myacc_frame_pfp = customtkinter.CTkLabel(self.myacc_frame, text="", image=self.image_for_pfp)
        self.myacc_frame_pfp.grid(row=1, column=0, padx=25, sticky='e')
        file.close()
        
    def get_user_pfp(self):
        client = Client()
        client.conn_serv()
        client.send_data(f'{self.user_data.get("id")}', 'send_user_pfp')
        file = open(f"images/pfp_image.png", "wb")
        file_bytes = b""
        done = False
        while not done:
            data = client.client.recv(1024)
            if file_bytes[-5:] == b"<END>":
                done = True
            else:
                file_bytes += data
        file.write(file_bytes)
        file.close()

    def get_friend_pfp(self, id):
        client = Client()
        client.conn_serv()
        client.send_data(f'{id}', 'send_user_pfp')
        file = open(f"images/friend_pfp_image.png", "wb")
        file_bytes = b""
        done = False
        while not done:
            data = client.client.recv(1024)
            if file_bytes[-5:] == b"<END>":
                done = True
            else:
                file_bytes += data
        file.write(file_bytes)
        file.close()

    def read_ud(self, user_data):
        self.user_data = {}
        for el in user_data:
            ud = el.split('=')
            if ud[0] == "status":
                ud[1] = ud[1].replace("€", "=")
            self.user_data[ud[0]] = ud[1]
        print(self.user_data)

    def read_fd(self, user_data):
        friend_data = {}
        for el in user_data:
            ud = str(el).split('=')
            if ud[0] == "status":
                ud[1] = ud[1].replace("€", "=")
            friend_data[ud[0]] = ud[1]
        return friend_data


if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    version = '_1_1_7'
    """
    client = Client()
    client.conn_serv()
    client.send_data(version, 'check_version')
    client.get_data()
    if client.data != 'OK':
        with open('reme/version.txt', 'w', encoding='utf-8') as file:
            file.write(f"{version}\n{client.data}")
        version = client.data
        print('Обновляем инсталлятор, подождите...')
        client = Client()
        client.conn_serv()
        client.send_data(version, 'send_installator')
        client.get_data()
        file_size = client.data
        print(f'Скачиваем файл [version_loader.rar] - BYTES[{file_size}]')
        file = open(f"version_loader.rar", 'wb')
        file_bytes = b""
        done = False
        while not done:
            data = client.client.recv(1024)
            if file_bytes[-5:] == b"#END#":
                done = True
            else:
                file_bytes += data
        file.write(file_bytes)
        file.close()
        try:
            shutil.rmtree(f"{path}/build/version_loader")
        except:
            pass
        try:
            os.remove("version_loader.spec")
        except:
            pass
        try:
            os.remove("version_loader.exe")
        except:
            pass
        patoolib.extract_archive(archive='version_loader.rar')
        os.startfile('version_loader.exe')
        exit()
    """

    log_out_status = ''
    id = ''

    with open('reme/status.txt', 'r', encoding='utf-8') as file:
        data_from_file = file.read().split('\n')
        log_out_status += data_from_file[0].split('=')[1]
        id += data_from_file[1].split('=')[1]

    if log_out_status == 'True':
        client = Client()
        client.conn_serv()
        client.send_data(f'{id}', 'get_user_data')
        client.get_data()
        app = MainProgram(client.data.split('\n')[:-1])
        app.mainloop()
    elif log_out_status == 'False':
        logreg = LogRegApp()
        logreg.app.mainloop()




#END#