nova_senha = ['2','7','/','0','9','/','2','0','0','2']

for j in range(0,2,1):
    for i in range(0,1):
        nova_senha.insert(i,'{}'.format(j))

#nova_senha = str(nova_senha).strip('[]')
nova_senha.pop(1)
nova_senha.pop(0)
nova_senha.pop(2)
nova_senha.pop(4)
nova_senha = "".join(nova_senha)
nova_senha.strip("/")
print("sua senha eh {}".format(nova_senha))


                    nova_senha.pop(1)
                    nova_senha.pop(0)
                    nova_senha.pop(2)
                    nova_senha.pop(4)