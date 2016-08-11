import bottle
import json
import threading
import requests
import time
from sys import argv

l_messages = [argv[-1]]
l_clients  = argv[2:-1]

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
        l_messages.append((source, target, subjec, messag))
    redirect('/')

@bottle.route('/list_peers')
def search_peers():
    return json.dumps(l_clients)

@bottle.route('/list_messages')
def search_messages():
    return json.dumps(l_messages)


def t_run():
    time.sleep(4)
    lst_p = []
    lst_m = []

    while True:
        for p in l_clients:
            peers = requests.get(p + '/list_peers')
            messg = requests.get(p + '/list_messages')

            lst_p = l_clients  + json.loads(peers.text)
            lst_m = l_messages + json.loads(messg.text)

            time.sleep(1)
            
        l_clients[:]  = list(set(lst_p + l_clients))
        l_messages[:] = list(set(lst_m + l_messages))
        print(l_clients, l_messages)


def main():
    t = threading.Thread(target=t_run)
    t.start()
    #print(list_clients)
    bottle.run(host="localhost", port=int(argv[1]))

if __name__ == '__main__':
    main()
