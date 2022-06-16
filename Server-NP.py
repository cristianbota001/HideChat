from socket import*
from threading import*
import time
on_users = {}
file_users_des = {}
file_users_mitt = {}
ban = []

class Terminale(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        while True:
            mossa = input()
            if mossa[0:3] == "ban":
                bann = mossa.replace("ban","")
                bann = bann.replace(" ","")
                if bann not in ban:
                    ban.append(bann)
                    for x in on_users:
                        if on_users[x][1] == bann:
                            on_users[x][0].sendall(bytes("!!ban##" + "<--[°+°]-->","utf-8"))
            if mossa == "ban":
                print(ban)
            if mossa == "on_users":
                print(on_users)
            if mossa[0:5] == "noban":
                nbann = mossa.replace("noban","")
                nbann = nbann.replace(" ","")
                if nbann in ban:
                    ban.remove(nbann)

class Server(Thread):
    def __init__(self, so, ind):
        Thread.__init__(self)
        self.so = so
        self.ind = ind
    def run(self):
        class users():
            def __init__(self, so, ind):
                self.so = so
                self.ind = ind
                while True:
                    try:
                        data = so.recv(4096)
                        mess = data.decode()
                        num = []
                        self.controllo_messaggio(mess, num)
                        for mess in num:
                            if mess[0:8] == "!!iscr##":
                                self.iscrizione(mess)
                            if mess[0:8] == "!!mess##":
                                self.spacc_e_trasm(mess)
                            if mess[0:14] == "!!sta_scrive##":
                                self.sta_scrive(mess)
                            if mess[0:9] == "##okdes!!":
                                self.okdes(mess)
                            if mess[0:10] == "##okmitt!!":
                                self.okmitt(mess)
                    except:
                        t = time.localtime()
                        print(self.nome, "left the chat",time.strftime("%H:%M:%S", t))
                        self.uscita()
                        del on_users[self.nome]
                        break
            def iscrizione(self, mess):
                mess = mess.replace("!!iscr##","")
                if self.ind[0] not in ban:
                    if mess not in on_users:
                        on_users[mess] = (self.so,self.ind[0])
                        self.nome = mess
                        self.so.sendall(bytes("!!ok##","utf-8"))
                        t = time.localtime()
                        print(self.nome,self.ind[0], "join the chat", time.strftime("%H:%M:%S", t))
                        self.entrata()
                        self.send_partec()
                    else:
                        self.so.sendall(bytes("!!noiscr##","utf-8"))
                else:
                    self.so.sendall(bytes("!!ban##","utf-8"))
            def controllo_messaggio(self,mess,num):
                while mess != "":
                    mes = mess.find("<--[°+°]-->",1)
                    bb = mess[0:mes]
                    mess = mess.replace(mess[0:mes] + "<--[°+°]-->","",1)
                    num.append(bb)
            def spacc_e_trasm(self, msg):
                mess = msg.replace("!!mess##","")
                for ogg in on_users:
                    if ogg != self.nome:
                        on_users[ogg][0].sendall(bytes("##mess!!" + self.nome + "§" + mess + "<--[°+°]-->","utf-8"))
            def sta_scrive(self, mess):
                mess = mess.replace("!!sta_scrive##","")
                for ogg in on_users:
                    if ogg != self.nome:
                        on_users[ogg][0].sendall(bytes("##sta_scrive!!" + self.nome + "<--[°+°]-->","utf-8"))
            def entrata(self):
                for ogg in on_users:
                    if ogg != self.nome:
                        on_users[ogg][0].sendall(bytes("##join!!" + self.nome + "<--[°+°]-->","utf-8"))
            def send_partec(self):
                for ogg in on_users:
                    self.so.sendall(bytes("##partec!!" + ogg + "<--[°+°]-->","utf-8"))
            def uscita(self):
                for ogg in on_users:
                    if ogg != self.nome:
                        on_users[ogg][0].sendall(bytes("##left!!" + self.nome + "<--[°+°]-->","utf-8"))
            def okdes(self, mess):
                aa = mess.replace("##okdes!!","")
                des = aa[0:aa.find("§",1)]
                mitt = aa.replace(des + "§","",1)[0:aa.replace(des + "§","",1).find("§")]
                dire = aa.replace(des + "§" + mitt + "§","",1)
                on_users[des][0].sendall(bytes("##okdes!!" + mitt + "§" + dire + "<--[°+°]-->","utf-8"))
            def okmitt(self, mess):
                aa = mess.replace("##okmitt!!","")
                mitt = aa[0:aa.find("§",1)]
                des = aa.replace(mitt + "§","",1)[0:aa.replace(mitt + "§","",1).find("§")]
                dire = aa.replace(mitt + "§" + des + "§","",1)
                on_users[mitt][0].sendall(bytes("##okmitt!!" + des + "§" + dire + "<--[°+°]-->","utf-8"))
                
        users(self.so, self.ind)
class Server_Transfer_Receiver(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        with socket(AF_INET, SOCK_STREAM) as so:
            so.bind(('', 1234))
            so.listen()
            while True:
                cl, ind = so.accept()
                tr = Transfer_Receiver(cl,ind)
                tr.start()
class Transfer_Receiver(Thread):
    def __init__(self,so,ind):
        self.so = so
        self.ind = ind
        Thread.__init__(self)
    def run(self):
        try:
            while True:
                info = self.so.recv(4096)
                info = info.decode()
                if info[0:4] == "!des":
                    file_users_des[info.replace("!des","")] = self.so
                    break
                elif info[0:5] == "!mitt":
                    file_users_mitt[self.so] = info.replace("!mitt","")
                elif info[0:5] == "!stop":
                    file_users_des[file_users_mitt[self.so]].sendall(bytes("!stop","utf-8"))   
                    del file_users_des[file_users_mitt[self.so]]
                    del file_users_mitt[self.so]
                    break
                else:
                    file_users_des[file_users_mitt[self.so]].sendall(bytes(info,"utf-8"))
        except:
            del file_users_des[file_users_mitt[self.so]]
            del file_users_mitt[self.so]
                       
trre = Server_Transfer_Receiver()
trre.start()

with socket(AF_INET, SOCK_STREAM) as so:
    so.bind(('', 8000))
    so.listen()
    te = Terminale()
    te.start()
    while True:
        cl, ind = so.accept()
        tt = Server(cl,ind)
        tt.start()