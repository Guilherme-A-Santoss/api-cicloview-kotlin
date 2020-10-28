from flask import Flask, jsonify, request
import json
import urllib.request
import random

app = Flask(__name__)

pecas = [
    {
        "id": 1,
        "nome": "Selim em gel",
        "marca": "Shimano",
        "imagem": "https://http2.mlstatic.com/D_NQ_NP_628501-MLB43189727805_082020-O.webp",
        "codigo": "C2904L1",
        "valor": "71.90"
    },
    {
        "id": 2,
        "nome": "Catraca Roda Livre Bike 18 Dentes Esferada Dourada",
        "marca": "Paco",
        "imagem": "https://http2.mlstatic.com/D_NQ_NP_781848-MLB43105592528_082020-O.webp",
        "codigo": "C3934D2",
        "valor": "23.90"
    },
    {
        "id": 3,
        "nome": "Câmbio Traseiro Com Gancheira 7 Velocidades Index P/bike Mtb",
        "marca": "Yamada",
        "imagem": "https://http2.mlstatic.com/D_NQ_NP_994456-MLB43473857848_092020-O.webp",
        "codigo": "S2414W6",
        "valor": "33.90"
    },
    {
        "id": 4,
        "nome": "Par Pneu Pirelli Speed 700x25 Tornado + 2 Camara+ 2 Fita A/f",
        "marca": "Pirelli",
        "imagem": "https://http2.mlstatic.com/D_NQ_NP_920616-MLB31778384975_082019-O.webp",
        "codigo": "J4546P9",
        "valor": "189.90"
    },
    {
        "id": 5,
        "nome": "Quadro Bike Mtb Aro 29 Absolute Nero Alumínio Disc Amarelo",
        "marca": "Absolute",
        "imagem": "https://http2.mlstatic.com/D_NQ_NP_600911-MLB43846632034_102020-O.webp",
        "codigo": "C4565Q2",
        "valor": "599.49"
    },
]

@app.route("/pecas", methods=['GET'])
def get():
    return jsonify(pecas)

@app.route("/pecas/<int:id>", methods=['GET'])
def get_one(id):
    filtro = [e for e in pecas if e["id"] == id]
    if filtro:
        return jsonify(filtro[0])
    else:
        return jsonify({})

@app.route("/pecas", methods=['POST'])
def post():
    global pecas
    try:
        content = request.get_json()

        # gerar id
        ids = [e["id"] for e in pecas]
        if ids:
            nid = max(ids) + 1
        else:
            nid = 1
        content["id"] = nid
        pecas.append(content)
        return jsonify({"status":"OK", "msg":"Peça adicionada do estoque com sucesso"})
    except Exception as ex:
        return jsonify({"status":"ERRO", "msg":str(ex)})

@app.route("/pecas/<int:id>", methods=['DELETE'])
def delete(id):
    global pecas
    try:
        pecas = [e for e in pecas if e["id"] != id]
        return jsonify({"status":"OK", "msg":"Peça removida do estoque com sucesso"})
    except Exception as ex:
        return jsonify({"status":"ERRO", "msg":str(ex)})

@app.route("/push/<string:key>/<string:token>", methods=['GET'])
def push(key, token):
	b = random.choice(pecas)
	data = {
		"to": token,
		"notification" : {
			"title":b["nome"],
			"body":"Você tem nova peca registrada"+b['nome']
		},
		"data" : {
			"pecaId":b['id']
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
