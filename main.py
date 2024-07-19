from datetime import date, timedelta, datetime
import flask
from flask import Flask, abort, render_template, redirect, url_for, flash, request, send_from_directory, jsonify
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor

from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


import math
from notifications import*
from forms import*
from db_classes import*


ckeditor = CKEditor(app)
Bootstrap5(app)


with app.app_context():
    db.create_all()

login_managero = LoginManager()
login_managero.init_app(app)
login_managero.login_view = 'login'



# Ensure the upload directory exists
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'assets', 'photos')  # Directory to save uploaded files

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@login_managero.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login', error="Firstly, say who you are."))


@login_managero.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.id == 1:
                return f(*args, **kwargs)
        return redirect(url_for('login', error="Please log in as Admin first."))
    return decorated_function




@app.route("/")
def index():



    return render_template("index.html",  current_user=current_user)



        name = register_form.name.data

        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if user:
            error = "User with this e-mail address already exists. Log in instead"
            login_form = LoginForm()
            return redirect(url_for('login', form=login_form, error=error))

        elif password != confirm:
            error = "Given passwords do not match!"


        else:
            new_user = User(email=email,
                            password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8), name=name)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            return redirect(url_for('places'))

    
    return render_template("register.html", form=register_form, error=error)


# TODO: Retrieve a user from the database based on their email.
@app.route('/login', methods=['GET', 'POST'])
def login():

    error = request.args.get('error')

    login_form = LoginForm()
    if login_form.validate_on_submit():

        email = login_form.email.data
        password = login_form.password.data

        # Find user by email entered.
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        if not user:
            error = "User with this e-mail address does not exist."

        else:

            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('places'))

            else:
                error = "Password does not match with this e-mail address."



    return render_template("login.html", form=login_form, error=error, logged_in=current_user.is_authenticated)





@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))









@app.route("/students")
@admin_only
def students():

    series = db.session.execute(db.select(Series)).scalars().all()

    exercises = 0


    series_score = [0] * len(series)
    for index, ser in enumerate(series):

        exercises += len(ser.exercises)

        if len(ser.answers) != 0:
            points = 0
            for answer in ser.answers:
                points += answer.point
            points = math.floor(points/len(ser.answers)*100)
            
            series_score[index] = points


    pupils = db.session.execute(db.select(User)).scalars().all()

    pupil_score = [0] * len(pupils)
    pupil_series = [0] * len(pupils)
    for index, pup in enumerate(pupils):
        points = 0
        if len(pup.answers) != 0:


            for answer in pup.answers:
                points += answer.point


            points = math.floor(points / len(pup.answers) * 100)



        tests = 0
        for answer in pup.answers:

            tests += 1
        tests = math.floor(tests / exercises * 100)



        pupil_score[index] = points
        pupil_series[index] = tests

    series.reverse()
    series_score.reverse()

    return render_template("users.html", series=series, series_score=series_score,
                           pupils=pupils, pupil_score=pupil_score,
                           pupil_series=pupil_series)




@app.route('/get_url', methods=['POST'])
def get_url():
    data = request.json
    latitude = data['latitude']
    altitude = data['altitude']
    url = url_for('add_place_main', latitude=latitude, altitude=altitude)
    return jsonify({'url': url})

@app.route("/new_place", methods=["GET", "POST"])
@login_required
def add_new_place():


    return render_template("add_place_intro.html")


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400

    # Search for the place
    place_search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={GOOGLE_API_KEY}"
    place_search_response = requests.get(place_search_url).json()

    if 'results' not in place_search_response or not place_search_response['results']:
        return jsonify({'error': 'No results found'}), 404

    place = place_search_response['results'][0]
    place_id = place['place_id']

    # Get place details
    place_details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={GOOGLE_API_KEY}"
    place_details_response = requests.get(place_details_url).json()

    if 'result' not in place_details_response:
        return jsonify({'error': 'Failed to retrieve place details'}), 500

    result = place_details_response['result']

    # Extract required details
    place_details = {'name': result.get('name'), 'address': result.get('formatted_address'),
        'lat': result['geometry']['location']['lat'], 'lng': result['geometry']['location']['lng'],
        'photo': result['photos'][0]['photo_reference'] if 'photos' in result else None}

    if place_details['photo']:
        place_details[
            'photo'] = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={place_details['photo']}&key={GOOGLE_API_KEY}"

    return jsonify(place_details)












@app.route("/add_place_form", methods=["GET", "POST"])
@login_required
def add_place_main():
    latitude = request.args.get('latitude')
    altitude = request.args.get('altitude')

    form = AddPlaceForm()
    filename = ''
    if form.validate_on_submit():

        photo = form.photo.data
        if photo:
            filename = secure_filename(photo.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(filepath)

        new_place = Place(

            name=form.name.data, coordinate1=latitude, coordinate2=altitude, description=form.description.data,
            distance=form.distance.data, type=form.type.data, photo_address=filename, author=current_user,

            att_food= form.food.data,
            att_my_food=form.my_food.data,
            att_table= form.table.data,
            att_socket=form.socket.data,
            att_cultural=form.cultural.data,
            att_outdoor_activity= form.outdoor_activity.data,
            att_work_study= form.work_study.data


        )
        db.session.add(new_place)
        db.session.commit()





        db.session.commit()
        return redirect(url_for("places"))
    return render_template("add_place_form.html", form=form, altitude=altitude, latitude=latitude)


@app.route("/delete/<int:series_id>/<int:exercise_id>")
@admin_only
def delete_exercise(series_id, exercise_id):

    exercise_to_delete = db.get_or_404(Exercise, exercise_id)
    answers_to_delete = db.session.query(Answer).filter(Answer.series_id == series_id).all()
    db.session.delete(exercise_to_delete)
    for item in answers_to_delete:
        db.session.delete(item)
    db.session.commit()
    return redirect(url_for('show_series', series_id=series_id))




@app.route("/delete-student/<int:student_id>")
@admin_only
def delete_student(student_id):

    student_to_delete = db.get_or_404(User, student_id)
    answers_to_delete = db.session.query(Answer).filter(Answer.user_id == student_id).all()

    db.session.delete(student_to_delete)


    for item in answers_to_delete:
        db.session.delete(item)
    db.session.commit()
    return redirect(url_for('students'))






@app.route("/places")
@login_required
def places():

    your_places = db.session.query(Place).filter(Place.author_id == current_user.id).all()



    return render_template("places.html", logged_in=current_user.is_authenticated, places=your_places)


@app.route("/place/<int:place_id>")
@login_required
def place(place_id):

    your_place = db.get_or_404(Place, place_id)



    return render_template("place.html", logged_in=current_user.is_authenticated, place=your_place)




if __name__ == "__main__":
    app.run(debug=True)