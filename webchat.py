import bottle
import json
import threading
import requests
import time
from sys import argv

l_messages = []
l_clients  = argv[2:]

@bottle.get('/')
@bottle.view('index')
def message():
     return {'list_messages': l_messages}

@bottle.post('/message')
def receive_message():
    source = bottle.request.forms.get("Remetente")
    target = bottle.request.forms.get("Destinatario")
    subjec = bottle.request.forms.get("Assunto")
    messag = bottle.request.forms.get("Mensagem")

    if source != "" and target != "":
        l_messages.append([source, target, subjec, messag])
    bottle.redirect('/')

@bottle.route('/list_peers')
def search_peers():
    return json.dumps(l_clients)

@bottle.route('/list_messages')
def search_messages():
    return json.dumps(l_messages)


def t_messages():
    time.sleep(4)
    lst_m = []

    while True:
        for p in l_clients:
            messg = requests.get(p + '/list_messages')
            lst_m = json.loads(messg.text)

            time.sleep(1)


        if lst_m in l_messages == False:
            l_messages[:] = lst_m + l_messages
        print(l_messages)
        print(lst_m)


def t_clients():
    time.sleep(4)
    lst_p = []

    while True:
        for p in l_clients:
            peers = requests.get(p + '/list_peers')
            lst_p = l_clients  + json.loads(peers.text)

            time.sleep(1)

        l_clients[:]  = list(set(lst_p + l_clients))
        print(l_clients)


def main():
    t = threading.Thread(target=t_clients)
    p = threading.Thread(target=t_messages)
    t.start()
    p.start()

    bottle.run(host="localhost", port=int(argv[1]))

if __name__ == '__main__':
    main()
