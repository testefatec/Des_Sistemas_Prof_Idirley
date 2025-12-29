"""
Exemplo ativo: Command Injection em Python (Flask) — detectável por ferramentas estáticas.
ATENÇÃO: código intencionalmente vulnerável. Execute apenas em ambiente de laboratório isolado.
"""

from flask import Flask, request
import subprocess

app = Flask(__name__)


@app.route('/ping')
def ping():
    # Vulnerabilidade: uso de entrada do usuário em comando de shell
    host = request.args.get('host', '127.0.0.1')
    # unsafe: passing user input directly to shell command
    try:
        output = subprocess.check_output(f"ping -c 1 {host}", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return f"Resultado:\n<pre>{output}</pre>"
    except subprocess.CalledProcessError as e:
        return f"Erro ao executar ping:\n<pre>{e.output}</pre>", 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# Mitigação: não use shell=True; valide/whitelist a entrada ou use argumentos sem shell.
