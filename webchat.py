from bottle import route, run, template, get, request, post, redirect, view
from sys import argv

list_messages = []

@get('/')
@view('index')
def message():
     return {'list_messages': list_messages}

@post('/message')
def receive_message():
    source = request.forms.get("Remetente")
    target = request.forms.get("Destinatario")
    subjec = request.forms.get("Assunto")
    messag = request.forms.get("Mensagem")

    if source != "" and target != "":
        list_messages.append((source, target, subjec, messag))
    redirect('/')

print(argv[1])
print(int(argv[1]))
run(host="localhost", port=int(argv[1]))
