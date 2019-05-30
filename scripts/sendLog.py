import ujson
import urequests as requests
import btree
import machine

f = open("log_table", "r+b")
db = btree.open(f)

url = 'http://ptsv2.com/t/1gm7w-1559233557/post'

try:
    key = 100
    for key in range(100, 999):
        try:
            key = str(key)
            json = ujson.loads(db[key])
            if json["enviado"] == 0:
                requests.post(url, json=json)
                json["enviado"] = 1
                db[key] = ujson.dumps(json)
                db.flush()
                print(key, "enviado")
                print(db[key])
        except KeyError:
            print("Final do Arquivo, Limpando...")
            for key in db:
                del db[key]
                db.flush()
            print("Lista Limpa")
            break
except IndexError:
    print("Sem net")
except OSError:
    machine.reset()
