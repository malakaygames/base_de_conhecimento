from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Caminho da pasta onde os arquivos txt estão localizados
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dados')

# Função para pesquisar os termos nos arquivos txt
def search_terms_in_files(terms):
    results = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.txt'):
            file_path = os.path.join(DATA_DIR, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if all(term.lower() in line.lower() for term in terms):
                        # Dividir por '|' para criar colunas
                        columns = line.strip().split('|')
                        results.append(columns)
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        search_query = request.form.get('query', '')
        if search_query:
            terms = search_query.split()  # Permite pesquisar múltiplos termos
            results = search_terms_in_files(terms)
    return render_template('index.html', results=results)

if __name__ == '__main__':
    # O servidor Flask ficará disponível na rede local
    app.run(host='0.0.0.0', port=5000)
