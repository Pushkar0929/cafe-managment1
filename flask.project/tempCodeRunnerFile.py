from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "xyz"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    special_requests = db.Column(db.Text, nullable=True)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

@app.route("/")
def home():
    return render_template("projectt.html")

@app.route("/reserve", methods=["POST"])
def reserve():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        date = request.form.get("date")
        time = request.form.get("time")
        guests = request.form.get("guests", type=int)
        special_requests = request.form.get("special_requests", "")

        if not name or not email or not date or not time or not guests:
            flash("All fields are required!", "error")
            return redirect(url_for("home"))

        new_reservation = Reservation(name=name, email=email, date=date, time=time, guests=guests, special_requests=special_requests)
        db.session.add(new_reservation)
        db.session.commit()

        flash("Reservation saved successfully!", "success")
        return redirect(url_for("home"))
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for("home"))

@app.route("/contact", methods=["POST"])
def contact():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if not name or not email or not message:
            flash("All fields are required!", "error")
            return redirect(url_for("home"))

        new_contact = Contact(name=name, email=email, message=message)
        db.session.add(new_contact)
        db.session.commit()

        flash("Message sent successfully!", "success")
        return redirect(url_for("home"))
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
