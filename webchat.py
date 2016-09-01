import bottle
import json
import threading
import requests
import time
from message        import *
from sys            import argv

l_messages = []
m_messages = []
l_clients  = argv[2:]

@bottle.get('/')
@bottle.view('index')
def message():
     return {'list_messages': m_messages}

@bottle.post('/message')
def receive_message():
    source = bottle.request.forms.get("Remetente")
    target = bottle.request.forms.get("Destinatario")
    subjec = bottle.request.forms.get("Assunto")
    messag = bottle.request.forms.get("Mensagem")

    if source != "" and target != "":
        m_messages.append(Message(source, target, subjec, messag))
        l_messages.append([source, target, subjec, messag])
    bottle.redirect('/')

@bottle.route('/list_peers')
def search_peers():
    return json.dumps(l_clients)

@bottle.get('/list_messages')
def search_messages():
    return json.dumps(l_messages)


def t_messages():
    time.sleep(5)

    while True:
        time.sleep(3)

        for c in l_clients:
            r  = requests.get(c + '/list_messages')
            for m in json.loads(r.text):
                if m not in l_messages:
                    l_messages.append(m)

def t_clients():
    time.sleep(5)
    lst_p = []

    while True:
        time.sleep(2)

        for p in l_clients:
            peers = requests.get(p + '/list_peers')
            lst_p = l_clients  + json.loads(peers.text)
        l_clients[:]  = list(set(lst_p + l_clients))


def main():
    t = threading.Thread(target=t_clients)
    t.start()

    p = threading.Thread(target=t_messages)
    p.start()

    bottle.run(host="localhost", port=int(argv[1]))

if __name__ == '__main__':
    main()
