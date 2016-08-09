from bottle import route, run, template, get, request, post, redirect, view

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

run(host="localhost", port=8080)
