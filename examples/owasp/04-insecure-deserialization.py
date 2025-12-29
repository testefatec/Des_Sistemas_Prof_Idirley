"""
Exemplo comentado: Desserialização insegura (insecure deserialization).
O código está comentado para evitar execução acidental.

Remova os comentários apenas em ambiente controlado e explique o risco de executar dados não confiáveis.
"""

# import pickle
# from flask import Flask, request
#
# app = Flask(__name__)
#
# @app.route('/upload', methods=['POST'])
# def upload():
#     # Vulnerabilidade: desserializar dados vindos do usuário sem validação
#     data = request.data
#     obj = pickle.loads(data)  # <- inseguro: pode executar código arbitrário
#     return 'Objeto carregado: ' + str(type(obj))
#
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')
