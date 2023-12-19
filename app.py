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

@app.route('/addShow')
def addShow():
    return render_template('addShow.html')

@app.route('/deleteShow')
def deleteShow():
    return render_template('deleteShow.html')

@app.route('/updateShow')
def updateShow():
    return render_template('updateShow.html')

@app.route('/showsList')
def showsList():
    return render_template('showsList.html')

@app.route('/actorsList')
def showActorsList():
    return render_template('actorsList.html')

@app.route('/actors', methods=['GET'])
def getActorsList():
    try:
        conn = db.connect(host="localhost", user="postgres", password="admin", dbname="netflix")
        cursor = conn.cursor()

        select_actors_query = """
            SELECT name, surname, year_of_birth, gender, shows.Title
            FROM actors
            JOIN shows ON actors.Show_id = shows.Show_id
        """
        cursor.execute(select_actors_query)
        actors_list = [{'name': row[0], 'surname': row[1], 'year_of_birth': row[2], 'gender': row[3], 'show_title': row[4]} for row in cursor.fetchall()]
        if not actors_list:
          response_data = {"status": "Not Found", "message": "Actors list was not found", "actors": None}
          response = jsonify(response_data)
          response.headers['Content-Type'] = 'application/json'
          return response, 404

        response_data = {"status": "OK", "message": "Fetched actors list", "actors": actors_list}
        response = jsonify(response_data)
        response.headers['Content-Type'] = 'application/json'
        return response, 200

    except db.Error as e:
        response_data = {"status": "Internal Server Error", "message": f"Error fetching actors list: {e}", "actors": None}
        response = jsonify(response_data)
        response.headers['Content-Type'] = 'application/json'
        return response, 500
    finally:
        if 'conn' in locals():
            conn.close()



@app.route('/getShowDetails/<int:show_id>', methods=['GET'])
def getShowDetails(show_id):
    try:
        conn = db.connect(host="localhost", user="postgres", password="admin", dbname="netflix")
        cursor = conn.cursor()

    
        select_show_query = "SELECT * FROM shows WHERE Show_id = %s"
        cursor.execute(select_show_query, (show_id,))
        show_details = cursor.fetchone()

      
        if not show_details:
            return jsonify({"status": "Not Found", "message": "Show not found", "data": None}), 404

       
        select_actors_query = "SELECT * FROM actors WHERE Show_id = %s"
        cursor.execute(select_actors_query, (show_id,))
        actors = cursor.fetchall()

        show_data = {
            'title': f'"{show_details[1]}" Details',
            'genre': show_details[2],
            'release_year': show_details[3],
            'imdb_grade': show_details[4],
            'creator': show_details[5],
            'number_of_episodes': show_details[6],
            'number_of_seasons': show_details[7],
            'actors': ', '.join([f'{actor[0]} {actor[1]}' for actor in actors])
        }

  
        html_content = render_template('showDetails.html', **show_data)

 
        return Response(html_content, status=200, content_type='text/html')

    except db.Error as e:
       
        return jsonify({"status": "Error", "message": f"Error fetching show details: {e}", "data": None}), 500

    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/get_filtered', methods=['GET'])
def get_filtered():
    filter_text = request.args.get('txt', '')
    filter_polje = request.args.get('polje', '')

    if(filter_polje.lower() != 'wildcard'): 
        if(filter_polje != 'release_year' and filter_polje != 'imdb_grade' and filter_polje != 'number_of_seasons' and
           filter_polje != 'number_of_episodes' and filter_polje != 'year_of_birth'):   
         query = f"""select title, genre, release_year, imdb_grade, creator,
            number_of_episodes, number_of_seasons, name,
            surname, year_of_birth, gender     
            from shows join actors on actors.show_id = shows.show_id
            where lower({filter_polje}) like lower('%{filter_text}%')"""
        else:
            query = f"""select title, genre, release_year, imdb_grade, creator,
            number_of_episodes, number_of_seasons, name,
            surname, year_of_birth, gender     
            from shows join actors on actors.show_id = shows.show_id
            where cast({filter_polje} as text) like '%{filter_text}%'"""
    else:
           query = f"""select title, genre, release_year, imdb_grade, creator,
            number_of_episodes, number_of_seasons, name,
            surname, year_of_birth, gender     
            from shows join actors on actors.show_id = shows.show_id
            where lower(concat(title, genre, release_year, imdb_grade,
            creator, number_of_episodes, number_of_seasons, name, surname, year_of_birth, gender)) like lower('%{filter_text}%')  """
    data = query_db(query)
    return jsonify(data)

@app.route('/download_csv', methods=['GET'])
def download_csv():
    filter_text = request.args.get('txt', '')
    filter_polje = request.args.get('polje', '')

    if(filter_polje.lower() != 'wildcard'): 
        if(filter_polje != 'release_year' and filter_polje != 'imdb_grade' and filter_polje != 'number_of_seasons' and
           filter_polje != 'number_of_episodes' and filter_polje != 'year_of_birth'):   
           query = f"""select title, genre, release_year, imdb_grade, creator,
            number_of_episodes, number_of_seasons, name,
            surname, year_of_birth, gender     
            from shows join actors on actors.show_id = shows.show_id
            where lower({filter_polje}) like lower('%{filter_text}%')"""
        else:
            query = f"""select title, genre, release_year, imdb_grade, creator,
            number_of_episodes, number_of_seasons, name,
            surname, year_of_birth, gender     
            from shows join actors on actors.show_id = shows.show_id
            where cast({filter_polje} as text) like '%{filter_text}%'"""
    else:
           query = f"""select title, genre, release_year, imdb_grade, creator,
            number_of_episodes, number_of_seasons, name,
            surname, year_of_birth, gender     
            from shows join actors on actors.show_id = shows.show_id
            where lower(concat(title, genre, release_year, imdb_grade,
            creator, number_of_episodes, number_of_seasons, name, surname, year_of_birth, gender)) like lower('%{filter_text}%')  """
    
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
        if(filter_polje != 'release_year' and filter_polje != 'imdb_grade' and filter_polje != 'number_of_seasons' and
           filter_polje != 'number_of_episodes' and filter_polje != 'year_of_birth'):   
           query = f"""select title, genre, release_year, imdb_grade, creator,
            number_of_episodes, number_of_seasons, name,
            surname, year_of_birth, gender     
            from shows join actors on actors.show_id = shows.show_id
            where lower({filter_polje}) like lower('%{filter_text}%')"""
        else:
            query = f"""select title, genre, release_year, imdb_grade, creator,
            number_of_episodes, number_of_seasons, name,
            surname, year_of_birth, gender     
            from shows join actors on actors.show_id = shows.show_id
            where cast({filter_polje} as text) like '%{filter_text}%'"""
    else:
           query = f"""select title, genre, release_year, imdb_grade, creator,
            number_of_episodes, number_of_seasons, name,
            surname, year_of_birth, gender     
            from shows join actors on actors.show_id = shows.show_id
            where lower(concat(title, genre, release_year, imdb_grade,
            creator, number_of_episodes, number_of_seasons, name, surname, year_of_birth, gender)) like lower('%{filter_text}%')  """
    
    data = query_db(query)

    json_data = json.dumps(data, indent=4)
    
    return Response(
        json_data,
        mimetype="application/json",
        headers={"Content-disposition":
                 "attachment; filename=table_filtered.json"}
    )

@app.route('/addNewShow', methods=['POST'])
def addNewShow():
    title = request.form.get('title')
    genre = request.form.get('genre')
    release_year = int(request.form.get('release_year'))
    imdb_grade = float(request.form.get('imdb_grade'))
    creator = request.form.get('creator')
    number_of_episodes = int(request.form.get('number_of_episodes'))
    number_of_seasons = int(request.form.get('number_of_seasons'))


    actor_names = request.form.getlist('actor_name[]')
    actor_surnames = request.form.getlist('actor_surname[]')
    actor_birth_years = [int(year) for year in request.form.getlist('actor_birth_year[]')]
    actor_genders = request.form.getlist('actor_gender[]')

    try:
        conn = db.connect(host="localhost", user="postgres", password="admin", dbname="netflix")
        cursor = conn.cursor()

   
        insert_show_query = """INSERT INTO shows (Title, Genre, Release_year, IMDB_grade, Creator, Number_of_episodes, Number_of_seasons)
                               VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING show_id"""
        cursor.execute(insert_show_query, (title, genre, release_year, imdb_grade, creator, number_of_episodes, number_of_seasons))

        
        show_id = cursor.fetchone()[0] 
      
        insert_actor_query = """INSERT INTO actors (Name, Surname, Year_of_birth, Gender, Show_id)
                                VALUES (%s, %s, %s, %s, %s)"""

        actor_data = zip(actor_names, actor_surnames, actor_birth_years, actor_genders, [show_id] * len(actor_names))
        cursor.executemany(insert_actor_query, actor_data)

        conn.commit()
        msg = "New Show Added Successfully!"
        response_data = {"status": "OK", "message": msg}
        return jsonify(response_data), 200, {'Content-Type': 'application/json'}

    except db.Error as e:
        error_msg = f"Error adding show: {e}"
        response_data = {"status": "Error", "message": error_msg}
        return jsonify(response_data), 500, {'Content-Type': 'application/json'}

    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/getShowTitles', methods=['GET'])
def getShowTitles():
    try:
        conn = db.connect(host="localhost", user="postgres", password="admin", dbname="netflix")
        cursor = conn.cursor()

        select_titles_query = "SELECT Show_id, Title FROM shows"
        cursor.execute(select_titles_query)
        show_titles = [{'show_id': row[0], 'title': row[1]} for row in cursor.fetchall()]
        if not show_titles:
            return jsonify({"status": "Not Found", "message": "No shows found", "data": None}), 404

    
        return jsonify({"status": "OK", "message": "Fetched show titles", "data": show_titles}), 200

    except db.Error as e:
       
        return jsonify({"status": "Error", "message": f"Error fetching shows: {e}", "data": None}), 500

    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/delete_show/<int:show_id>', methods=['DELETE'])
def delete_show(show_id):
    try:
        conn = db.connect(host="localhost", user="postgres", password="admin", dbname="netflix")
        cursor = conn.cursor()

  
        delete_actors_query = "DELETE FROM actors WHERE show_id = %s"
        cursor.execute(delete_actors_query, (show_id,))
        delete_show_query = "DELETE FROM shows WHERE Show_id = %s"
        cursor.execute(delete_show_query, (show_id,))
        conn.commit()


        if cursor.rowcount == 0:   
            response = {'status': 'Not Found', 'message': 'Show not found'}
            return jsonify(response), 404


        response = {'status': 'OK', 'message': 'Show deleted successfully'}
        return jsonify(response), 200

    except db.Error as e:
        print(f"Error connecting to the database: {e}")
        response = {'status': 'Error', 'error': 'Failed to delete show'}
        return jsonify(response), 500

    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/updateShowDetails', methods=['PUT'])
def update_show_details_endpoint():
    show_title = request.form.get('show_title')  
    imdb_grade = request.form.get('imdb_grade')
    num_episodes = request.form.get('num_episodes')
    num_seasons = request.form.get('num_seasons')


    if imdb_grade:
        imdb_grade = float(imdb_grade)
    if num_episodes:
        num_episodes = int(num_episodes)
    if num_seasons:
        num_seasons = int(num_seasons)

    
    if imdb_grade == '':
        imdb_grade = None
    if num_episodes == '':
        num_episodes = None  
    if num_seasons == '':
        num_seasons = None  

    print(imdb_grade, num_episodes, num_seasons)


    try:
        conn = db.connect(host="localhost", user="postgres", password="admin", dbname="netflix")
        cursor = conn.cursor()

        get_show_id_query = "SELECT show_id FROM shows WHERE title = %s;"
        cursor.execute(get_show_id_query, (show_title,))
        result = cursor.fetchone()
        print(show_title)
        if result:
            show_id = result[0]

            update_query = """
                UPDATE shows
                SET IMDB_grade = COALESCE(%s, IMDB_grade),
                    Number_of_episodes = COALESCE(%s, Number_of_episodes),
                    Number_of_seasons = COALESCE(%s, Number_of_seasons)
                WHERE Show_id = %s;
            """

            cursor.execute(update_query, (imdb_grade, num_episodes, num_seasons, show_id))

     
            actor_name = request.form.get('actor_name')
            actor_surname = request.form.get('actor_surname')
            actor_year_of_birth = request.form.get('actor_birth_year')
            actor_gender = request.form.get('actor_gender')
            print(actor_name, actor_surname, actor_year_of_birth, actor_gender)
            if all([actor_name, actor_surname, actor_year_of_birth, actor_gender]):
             
                get_show_id_query = "SELECT show_id FROM shows WHERE title = %s;"
                cursor.execute(get_show_id_query, (show_title,))
                result = cursor.fetchone()
                if result:
                    show_id = result[0]
                    print(show_id)
          
                insert_actor_query = """
                    INSERT INTO actors (Name, Surname, Year_of_birth, Gender, Show_id)
                    VALUES (%s, %s, %s, %s, %s);
                """

                cursor.execute(insert_actor_query, (actor_name, actor_surname, actor_year_of_birth, actor_gender, show_id))

            conn.commit()
            response = jsonify({'status': 'OK','message': 'Show details updated successfully!'})
            response.headers['Content-Type'] = 'application/json'
            return response, 200

    except db.Error as e:
        print(f"Error updating show details: {e}")
        response = jsonify({'error': 'Failed to update show details.'})
        response.headers['Content-Type'] = 'application/json'
        return response, 500

    finally:
        if 'conn' in locals():
            conn.close()
    response = jsonify({'status': 'Bad Request' , 'message': 'Failed to update show details. Invalid input.'})
    response.headers['Content-Type'] = 'application/json'
    return response, 400

if __name__ == "__main__":
    app.run(debug=True)