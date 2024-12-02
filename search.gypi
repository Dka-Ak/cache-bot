from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Search Countries</title>
            <style>
                .search-result {
                    margin-top: 10px;
                    padding: 5px;
                    border-bottom: 1px solid #ccc;
                }
            </style>
        </head>
        <body>
            <h1>Search Countries</h1>
            <input type="text" id="searchBar" placeholder="Search..." onkeyup="searchFunction()">
            <div id="results"></div>

            <script>
                async function searchFunction() {
                    const input = document.getElementById('searchBar').value.toLowerCase();
                    const response = await fetch('/search?query=' + input);
                    const countries = await response.json();
                    const resultsContainer = document.getElementById('results');
                    resultsContainer.innerHTML = '';

                    countries.forEach(country => {
                        const div = document.createElement('div');
                        div.className = 'search-result';
                        div.textContent = `Name: ${country['name']}, Capital: ${country['capital']}, Population: ${country['population']}, Area: ${country['area']}, Currency: ${country['currency']}`;
                        resultsContainer.appendChild(div);
                    });
                }
            </script>
        </body>
        </html>
    ''')

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify([])

    response = requests.get('https://restcountries.com/v3.1/all')
    countries_data = response.json()

    filtered_countries = []
    for country in countries_data:
        name = country['name']['common']
        capital = country['capital'][0] if 'capital' in country and country['capital'] else 'N/A'
        population = country['population']
        area = country['area']
        currency = list(country['currencies'].keys())[0] if 'currencies' in country else 'N/A'
        
        if query in name.lower():
            filtered_countries.append({
                'name': name,
                'capital': capital,
                'population': population,
                'area': area,
                'currency': currency
            })

    return jsonify(filtered_countries)

if __name__ == '__main__':
    app.run(debug=True)
