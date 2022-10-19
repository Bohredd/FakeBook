from tkinter import *
import tkinter
from tkinter.tix import LabelEntry
import pessoas
import sqlite3
from tkinter import messagebox
import re

def janela_principal():
    pessoas.conexaocombanco()
    #inicializacao da janela
    master = Tk()
    master.title("FakeBook")
    master.geometry("1152x864+480+100")
    master.iconbitmap(default="imagens\\ico.ico")
    master.resizable(width=0,height=0) # deixa a pagina como headless

    #defs
    def pegar_login_senha_validar():
        login = en_email_login.get()
        senha = en_senha_login.get()

        login = login.strip()
        senha = senha.strip()

        banco = sqlite3.connect("cadastros.db")
        cursor = banco.cursor()

        try:
            cursor.execute("SELECT Senha FROM Pessoas Where Email = '{}'".format(login))
            
            senha_bd = cursor.fetchall()

            cursor.execute("SELECT Nome FROM Pessoas Where Email = '{}'".format(login))
            seu_nome_usuario = cursor.fetchall()
            print(senha_bd[0][0])
            print(seu_nome_usuario[0][0])

            banco.close()
        except:
            print("Erro ao validar login!")

        if senha == senha_bd[0][0]:
            print("Senha correta!")
            messagebox.showinfo(title="Sucesso!",message="Conectado com sucesso!")
            janela_chat()
        else:
            messagebox.showwarning(title="Erro!",message="Email ou senha incorretos! Tente novamente!")
   
    def pegar_dados_cadastro():
        nome = en_nome_cadastro.get()
        sobrenome = en_sobrenome_cadastro.get()
        email_cadastro = en_email_cadastro.get()
        senha_cadastro = en_senha_cadastro.get()
        data_nascimento = en_datanascimento_cadstro.get()


        nome = str("{nome} {sobrenome}".format(nome=nome,sobrenome=sobrenome))
        nome = nome.strip()
        nome = nome.title()
        email_cadastro = email_cadastro.strip()
        senha_cadastro = senha_cadastro.strip()
        print(nome)
        print(email_cadastro)
        print(senha_cadastro)
        print(data_nascimento)
        banco = sqlite3.connect("cadastros.db")
        cursor = banco.cursor()
        consulta_sql = "SELECT * From Pessoas"
        cursor.execute(consulta_sql)
        linhas = cursor.fetchall()
        existe_no_banco = True
        retornar_aviso = True
        dados_vazios = True
        aux = False

        if nome and email_cadastro and senha_cadastro and data_nascimento != None:
            dados_vazios = False


        else:
            messagebox.showerror(title="Erro no cadastro!",message="Insira todos os dados requisitados do cadastro!")
            dados_vazios = True

        for linha in linhas:
            if email_cadastro == linha[2]:
                banco.close()
                existe_no_banco = True
                retornar_aviso = True
                aux = True

        if aux == False:
            retornar_aviso = False
            existe_no_banco = False
            retornar_aviso = False


        if retornar_aviso == True:
            messagebox.showwarning(title="Email ja cadastrado!",message="Email cadastrado!! ")

        if existe_no_banco == False and dados_vazios == False and retornar_aviso == False:
            banco = sqlite3.connect("cadastros.db")
            cursor = banco.cursor()
            cursor.execute("INSERT INTO Pessoas (Nome, Email, Senha, Nascimento)VALUES ('"+nome+"','"+email_cadastro+"','"+senha_cadastro+"','"+data_nascimento+"')")

            banco.commit()
            banco.close()
            
            #limpando campos
            en_datanascimento_cadstro.delete(0, END)
            en_email_cadastro.delete(0, END)
            en_senha_cadastro.delete(0, END)
            en_nome_cadastro.delete(0, END)
            en_sobrenome_cadastro.delete(0, END)
            messagebox.showinfo(title="Cadastro Fakebook",message="Cadastro realizado com sucesso!")

    def recuperar_senha():
        masterrecuperar = Toplevel()
        masterrecuperar.title("FakeBook Recuperar Senha")
        masterrecuperar.geometry("800x600+480+100")
        masterrecuperar.iconbitmap(default="imagens\\ico.ico")
        masterrecuperar.resizable(width=0,height=0)

        #defs
        def verificar_email_nome_recuperar():
            nome_recuperar= en_nome_recuperar.get()
            email_recuperar = en_email_recuperar.get()

            nome_recuperar =nome_recuperar.strip()
            nome_recuperar = nome_recuperar.title()
            email_recuperar = email_recuperar.strip()
            print(nome_recuperar)
            print(email_recuperar)
            existe_no_banco_email = False
            existe_no_banco_nome = False
            aux = False
            banco = sqlite3.connect("cadastros.db")
            cursor = banco.cursor()
            consulta_sql = "SELECT * From Pessoas"
            cursor.execute(consulta_sql)
            linhas = cursor.fetchall()
            nova_senha = []
            i = ''
            j = 0
            if email_recuperar and nome_recuperar != None:
                for linha in linhas:
                    if email_recuperar == linha[2] and nome_recuperar == linha[1]:
                        for j in range(0,10,1):
                            i = linha[4][j]
                            nova_senha.insert(j,'{}'.format(i))
                            existe_no_banco_email = True
                            existe_no_banco_nome = True
                nova_senha = "".join(nova_senha)
                nova_senha = re.sub('/','',nova_senha)
                print(nova_senha)

                if existe_no_banco_email and existe_no_banco_nome == True:
                    for linha in linhas:
                        if email_recuperar == linha[2] and nome_recuperar == linha[1]:
                            existe_no_banco_email = True
                            existe_no_banco_nome = True
                            messagebox.showinfo(title="Sucesso na redefinição!",message="Seus dados conferem! Enviamos um email com sua nova senha!") 
                            cursor.execute("UPDATE Pessoas SET Senha = '{}' WHERE Email = '{}'".format(nova_senha,email_recuperar))
                            banco.commit()
                            aux = True
                else:
                    messagebox.showerror(title="Erro!",message="Seus dados não conferem!")

            if email_recuperar and nome_recuperar == None:
                messagebox.showerror(title="Erro!",message="Insira corretamente todos os dados!")
            
            if aux == True:
                masterrecuperar.destroy()
                banco.close()
            if aux == False:
                masterrecuperar.destroy()
                banco.close()
                recuperar_senha()

        def voltar_pagina_principal():
            masterrecuperar.destroy()
        #importação de imagens
        img_fundo_recuperar_senha = PhotoImage(file="imagens\\PAGINA RECUPERAR.png")
        img_botao_recuperar = PhotoImage(file="imagens\\RECUPERAR PAG RECUPERAR.png")
        img_botao_voltar_recuperar = PhotoImage(file="imagens\\VOLTAR.png")

        #label 
        lab_fundo_recuperar = Label(masterrecuperar,image=img_fundo_recuperar_senha)
        lab_fundo_recuperar.pack()

        #entradas de texto
        en_email_recuperar = Entry(masterrecuperar,bd=2,font=("Calibri",13),justify=LEFT)
        en_email_recuperar.place(width=353,height=44,x=217,y=218)

        en_nome_recuperar = Entry(masterrecuperar,bd=2,font=("Calibri",13),justify=LEFT)
        en_nome_recuperar.place(width=353,height=44,x=217,y=340)


        #botoes
        botao_recuperar_pag_recuperar = Button(masterrecuperar,bd=0,image=img_botao_recuperar,command=verificar_email_nome_recuperar)
        botao_recuperar_pag_recuperar.place(width=204,height=44,x=414,y=465)

        botao_voltar_recuperar = Button(masterrecuperar,bd=0,image=img_botao_voltar_recuperar,command=voltar_pagina_principal)
        botao_voltar_recuperar.place(width=204,height=44,x=170,y=465)

        masterrecuperar.mainloop()

    def janela_chat(): ##FAZER 
        master.destroy()
        masterchat = Tk()
        masterchat.title("FakeBook Whats")
        masterchat.geometry("1152x864+480+100")
        masterchat.iconbitmap(default="imagens\\ico.ico")
        masterchat.resizable(width=0,height=0)

        #defs
        def enviar_mensagem():
            mensagem = enviar_mensagem_para_amigo.get()
            print(mensagem)
            enviar_mensagem_para_amigo.delete(0,END)

        #importação de imagens
        img_fundo_chat = PhotoImage(file="imagens\\pagina fakebook chat.png")
        img_botao_dar_tchau = PhotoImage(file="imagens\\DAR TCHAU.png")
        img_botao_sair_conversa = PhotoImage(file="imagens\\SAIR DA CONVERSA.png")
        img_foto_perfil_diogo = PhotoImage(file="imagens\\foto perfil diogo.png")
        img_botao_enviar_mensagem = PhotoImage(file="imagens\\enviar mensagem.png")

        #label
        lab_fundo_chat = Label(masterchat,image=img_fundo_chat)
        lab_fundo_chat.pack()

        lab_foto_amigo = Label(masterchat,image=img_foto_perfil_diogo)
        lab_foto_amigo.place(width=205,height=163,x=882,y=203)
        
        #frame conversa
        frame_conversa = Frame(masterchat,bg='#FFFFFF')
        frame_conversa.place(width=765,height=697,x=49,y=167)


        #barra scroll conversa
        barra_lateral = Scrollbar(frame_conversa)
        barra_lateral.pack(side=RIGHT,fill=Y)

        #entrada de texto no frame da conversa
        #mensagens_conversa = Text(frame_conversa, font=("Calibri",11),selectbackground="#FFFFFF",selectforeground="black",wrap=WORD,undo=TRUE, yscrollcommand=barra_lateral.set)
        #mensagens_conversa.place(width=753,height=691,x=0,y=0)
        
        #configurando barra lateral
        #barra_lateral.config(command=mensagens_conversa.yview)

        #entradas de texto
        nomeamigo = 'Diogo Antonio'
        en_nome_amigo = Label(masterchat,text="{}".format(nomeamigo),bg="blue",fg="white",font=("Calibri",13))
        en_nome_amigo.place(width=160,height=43,x=905,y=437)

        enviar_mensagem_para_amigo = Entry(frame_conversa,bd=2,font=("Calibri",13),justify=LEFT)
        enviar_mensagem_para_amigo.place(width=753,height=100,x=0,y=600)

        #botoes
        botao_dar_tchau = Button(masterchat,bd=0,image=img_botao_dar_tchau) #comand vai ser um audio falando tchau 
        botao_dar_tchau.place(width=95,height=78,x=1020,y=765)

        botao_sair_conversa = Button(masterchat,bd=0,image=img_botao_sair_conversa)
        botao_sair_conversa.place(width=95,height=78,x=855,y=765)

        botao_enviar_mensagem = Button(masterchat,bd=0,image=img_botao_enviar_mensagem,command=enviar_mensagem)
        botao_enviar_mensagem.place(width=95,height=78,x=938,y=765)

        #fazer um botao p enviar a mensagem
        #fazer um checkbox para mudar a cor da fonte do seu cliente

        #loopagem da janela
        masterchat.mainloop()

    def janela_colocar_imagemperfil(): ##FAZER E DESCOBRIR COMO INSERIR IMAGEM NO BD 
        print("janela imagem")
    
    def janela_timeline():
        print("timeline")
    
    #variaveis globais
    esconder_senha_login = tkinter.StringVar()
    esconder_senha_cadastro = tkinter.StringVar()
    padrao_data_nascimento = tkinter.StringVar()
    padrao_data_nascimento.set("dd/mm/yyyy")

    #importação de imagens
    img_fundo = PhotoImage(file="imagens\\login cadastro fakebook.png")
    img_botao_cadastre = PhotoImage(file="imagens\\CADASTRE-SE.png")
    img_entrar = PhotoImage(file="imagens\\ENTRAR.png")
    img_recuperar_senha = PhotoImage(file="imagens\\RECUPERAR.png")

    #label
    lab_fundo = Label(master,image=img_fundo)
    lab_fundo.pack()

    # entrada de texto
    en_email_login = Entry(master,bd=2,font=("Calibri",13),justify=LEFT)
    en_email_login.place(width=181, height=51,x=680,y=33)

    en_senha_login = Entry(master,bd=2,font=("Calibri",13),justify=LEFT,textvariable=esconder_senha_login,show="*")
    en_senha_login.place(width=181,height=51,x=890,y=33)

    en_nome_cadastro = Entry(master,bd=2,font=("Calibri",13),justify=LEFT)
    en_nome_cadastro.place(width=180,height=51,x=685,y=249)

    en_sobrenome_cadastro = Entry(master,bd=2,font=("Calibri",13),justify=LEFT)
    en_sobrenome_cadastro.place(width=180,height=51,x=885,y=249)

    en_email_cadastro = Entry(master,bd=2,font=("Calibri",13),justify=LEFT)
    en_email_cadastro.place(width=380,height=54,x=685,y=345)

    en_senha_cadastro = Entry(master,bd=2,font=("Calibri",13),justify=LEFT,textvariable=esconder_senha_cadastro,show="*")
    en_senha_cadastro.place(width=380,height=54,x=685,y=440)

    en_datanascimento_cadstro = Entry(master,bd=2,font=("Calibri",13),justify=LEFT,textvariable=padrao_data_nascimento)
    en_datanascimento_cadstro.place(width=176,height=51,x=685,y=535)

    #botoes
    botao_entrar = Button(master,bd=0,image=img_entrar,command=pegar_login_senha_validar)
    botao_entrar.place(width=83,height=44,x=1072,y=36)

    botao_cadastrar = Button(master,bd=0,image=img_botao_cadastre,command=pegar_dados_cadastro)
    botao_cadastrar.place(width=244,height=66,x=680,y=711)

    botao_recuperar_senha = Button(master,bd=0,image=img_recuperar_senha,command=recuperar_senha)
    botao_recuperar_senha.place(width=112,height=44,x=125,y=805)

    master.mainloop()

janela_principal()