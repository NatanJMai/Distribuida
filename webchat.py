import bottle
import json
import threading
import requests
import time
from message        import *
from sys            import argv

global localhost, port

localhost, port = 'localhost', int(argv[1])
l_messages      = []
m_messages      = []
l_clients       = argv[2:]
d_clients       = {}

@bottle.get('/')
@bottle.view('index')
def message():
     st = 'http://' + localhost + ':' + str(port)
     return {'list_messages': l_messages}

@bottle.post('/message')
def send_message():
    source = bottle.request.forms.get("Remetente")
    target = bottle.request.forms.get("Destinatario")
    subjec = bottle.request.forms.get("Assunto")
    messag = bottle.request.forms.get("Mensagem")

    if source != "" and target != "":
        st = 'http://' + localhost + ':' + str(port)
        d_clients[st] += 1
        d_client_aux = {}

        for i in l_clients:
            d_client_aux[i] = d_clients[i]

        # d_clients[st]
        #l_messages.append([source, target, subjec, messag, localhost, port, d_clients[st]])
        l_messages.append([source, target, subjec, messag, localhost, port, d_client_aux])
    bottle.redirect('/')

@bottle.route('/list_peers')
def search_peers():
    return json.dumps(l_clients)

@bottle.get('/list_messages')
def search_messages():
    return json.dumps(l_messages)


@bottle.get('/time')
def get_time():
    st = 'http://' + localhost + ':' + str(port)
    #print(st, d_clients[st])
    return json.dumps(d_clients[st])
    #return json.dumps(d_clients[st])


def t_messages():
    time.sleep(5)

    while True:
        time.sleep(3)

        for c in l_clients:
            r  = requests.get(c + '/list_messages')
            #t  = requests.get(c + '/time')
            #print(json.loads(t.text))
            for m in json.loads(r.text):
                if m not in l_messages:
                    new_d = m[-1]
                    st    = 'http://' + localhost + ':' + str(port)
                    d_clients[st] += 1

                    print("Antigo -> %s\n" % str(d_clients))
                    print("Recebi -> %s\n" % str(new_d))

                    for cl in l_clients:
                        d_clients[cl] = max(d_clients[cl], new_d[cl])
                    #d_clients[c]  = max(d_clients[c], json.loads(t.text))
                    
                    print("Novo -> %s\n" % str(d_clients))
                    
                    #print("Aqui -> %d\n" % d_clients[c])
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
        for i in l_clients:
            if not i in d_clients:
                d_clients[i] = 0


def main():
    t = threading.Thread(target=t_clients)
    t.start()

    p = threading.Thread(target=t_messages)
    p.start()

    bottle.run(host=localhost, port=port)

if __name__ == '__main__':
    main()
