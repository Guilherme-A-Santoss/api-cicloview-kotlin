from flask import Flask, jsonify, request
import json
import urllib.request
import random

app = Flask(__name__)

bicicletas = [
    {
        "id": 1,
        "nome": "Bicicleta Mountain",
        "tipo": "Manutenção",
        "imagem": "https://images.unsplash.com/photo-1572111504021-40abd3479ddb?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=634&q=80",
        "Proprietário": "Kauê"
    },
    {
        "id": 2,
        "nome": "Bicicleta de trilha",
        "tipo": "Manutenção",
        "imagem": "https://images.unsplash.com/photo-1566480047210-b10eaa1f8095?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80",
        "Proprietário": "Lucas Rangel"
    },
    {
        "id": 3,
        "nome": "Bicicleta Speed",
        "tipo": "Pintura",
        "imagem": "https://images.unsplash.com/photo-1532298229144-0ec0c57515c7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1308&q=80",
        "Proprietário": "Guilherme M."
    },
    {
        "id": 4,
        "nome": "Bicicleta Mountain",
        "tipo": "Manutenção",
        "imagem": "https://images.unsplash.com/photo-1530173235220-f6825c107a77?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1267&q=80",
        "Proprietário": "Fernando Henrique"
    },
    {
        "id": 5,
        "nome": "Bicicleta Mountain",
        "tipo": "Manutenção",
        "imagem": "https://images.unsplash.com/photo-1575585269294-7d28dd912db8?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80",
        "Proprietário": "Paulo Castro"
    },
]

@app.route("/bicicletas", methods=['GET'])
def get():
    return jsonify(bicicletas)

@app.route("/bicicletas/<int:id>", methods=['GET'])
def get_one(id):
    filtro = [e for e in bicicletas if e["id"] == id]
    if filtro:
        return jsonify(filtro[0])
    else:
        return jsonify({})

@app.route("/bicicletas", methods=['POST'])
def post():
    global bicicletas
    try:
        content = request.get_json()

        # gerar id
        ids = [e["id"] for e in bicicletas]
        if ids:
            nid = max(ids) + 1
        else:
            nid = 1
        content["id"] = nid
        bicicletas.append(content)
        return jsonify({"status":"OK", "msg":"Bicicleta adicionada a fila com sucesso"})
    except Exception as ex:
        return jsonify({"status":"ERRO", "msg":str(ex)})

@app.route("/bicicletas/<int:id>", methods=['DELETE'])
def delete(id):
    global bicicletas
    try:
        bicicletas = [e for e in bicicletas if e["id"] != id]
        return jsonify({"status":"OK", "msg":"Bicicleta removida da fila com sucesso"})
    except Exception as ex:
        return jsonify({"status":"ERRO", "msg":str(ex)})

@app.route("/push/<string:key>/<string:token>", methods=['GET'])
def push(key, token):
	b = random.choice(bicicletas)
	data = {
		"to": token,
		"notification" : {
			"title":b["nome"],
			"body":"Você tem nova ordem de serviço em "+b['nome']
		},
		"data" : {
			"biscicletaId":b['id']
		}
	}
	req = urllib.request.Request('http://fcm.googleapis.com/fcm/send')
	req.add_header('Content-Type', 'application/json')
	req.add_header('Authorization', 'key='+key)
	jsondata = json.dumps(data)
	jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
	req.add_header('Content-Length', len(jsondataasbytes))
	response = urllib.request.urlopen(req, jsondataasbytes)
	print(response)
	return jsonify({"status":"OK", "msg":"Push enviado"})


if __name__ == "__main__":
    app.run(host='0.0.0.0')
