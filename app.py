from flask import Flask, render_template, jsonify, request, Response
import psycopg2 as db, io, csv,json

app = Flask(__name__)

def query_db(query):
    conn = db.connect(host="localhost", user="postgres", password="admin", dbname="netflix")
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/datatable')
def datatable():
  
    return render_template('datatable.html')



@app.route('/get_filtered', methods=['GET'])
def get_filtered():
    filter_text = request.args.get('txt', '')
    filter_polje = request.args.get('polje', '')

    if(filter_polje.lower() != 'wildcard'):    
        query = f"""select title, genre, release_year, imdb_grade, creator,
            number_of_episodes, number_of_seasons, name,
            surname, year_of_birth, gender     
            from shows join actors on actors.show_id = shows.show_id
            where lower({filter_polje}) like lower('{filter_text}%')"""
    else:
        query = """select title, genre, release_year, imdb_grade, creator,
        number_of_episodes, number_of_seasons, name,
                 surname, year_of_birth, gender     
      from shows join actors on actors.show_id = shows.show_id """
    data = query_db(query)
    return jsonify(data)

@app.route('/download_csv', methods=['GET'])
def download_csv():
    filter_text = request.args.get('txt', '')
    filter_polje = request.args.get('polje', '')

    if(filter_polje.lower() != 'wildcard'):    
        query = f"""select title, genre, release_year, imdb_grade, creator,
            number_of_episodes, number_of_seasons, name,
            surname, year_of_birth, gender     
            from shows join actors on actors.show_id = shows.show_id
            where lower({filter_polje}) like lower('{filter_text}%')"""
    else:
        query = """select title, genre, release_year, imdb_grade, creator,
        number_of_episodes, number_of_seasons, name,
                 surname, year_of_birth, gender     
      from shows join actors on actors.show_id = shows.show_id """
    
    data = query_db(query)

    csv_data = io.StringIO()
    csv_writer = csv.writer(csv_data)
    csv_writer.writerow([
        "Title", "Genre", "Release Year", "IMDB Grade", "Creator",
        "Number of Episodes", "Number of Seasons", "Name", "Surname",
        "Year of Birth", "Gender"
    ])
    csv_writer.writerows(data)
    
    return Response(
        csv_data.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=table_filtered.csv"}
    )



@app.route('/download_json', methods=['GET'])
def download_json():
    filter_text = request.args.get('txt', '')
    filter_polje = request.args.get('polje', '')

    if(filter_polje.lower() != 'wildcard'):    
        query = f"""select title, genre, release_year, imdb_grade, creator,
            number_of_episodes, number_of_seasons, name,
            surname, year_of_birth, gender     
            from shows join actors on actors.show_id = shows.show_id
            where lower({filter_polje}) like lower('{filter_text}%')"""
    else:
        query = """select title, genre, release_year, imdb_grade, creator,
        number_of_episodes, number_of_seasons, name,
                 surname, year_of_birth, gender     
      from shows join actors on actors.show_id = shows.show_id """
    
    data = query_db(query)

    json_data = json.dumps(data, indent=4)
    
    return Response(
        json_data,
        mimetype="application/json",
        headers={"Content-disposition":
                 "attachment; filename=table_filtered.json"}
    )



if __name__ == "__main__":
    app.run(debug=True)