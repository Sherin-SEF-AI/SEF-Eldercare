from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from flask_socketio import emit
from . import db, login_manager, socketio
from .models import User, HealthMetric, Alert, Message, Location, Medication, Activity
from .forms import LoginForm, RegistrationForm, HealthMetricForm, AlertForm, LocationForm, MedicationForm, ActivityForm, MessageForm
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/')
@login_required
def home():
    return render_template('home.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@bp.route('/profile')
@login_required
def profile():
    health_metrics = HealthMetric.query.filter_by(user_id=current_user.id).all()
    alerts = Alert.query.filter_by(user_id=current_user.id).all()
    locations = Location.query.filter_by(user_id=current_user.id).all()
    medications = Medication.query.filter_by(user_id=current_user.id).all()
    activities = Activity.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', health_metrics=health_metrics, alerts=alerts, locations=locations, medications=medications, activities=activities)

@bp.route('/health_metrics', methods=['GET', 'POST'])
@login_required
def health_metrics():
    if request.method == 'POST':
        data = request.get_json()
        health_metric = HealthMetric(user_id=current_user.id, heart_rate=data['heart_rate'], steps=data['steps'])
        db.session.add(health_metric)
        db.session.commit()
        return jsonify({'success': True}), 201
    form = HealthMetricForm()
    return render_template('health_metrics.html', form=form)

@bp.route('/alerts', methods=['GET', 'POST'])
@login_required
def alerts():
    form = AlertForm()
    if form.validate_on_submit():
        alert = Alert(user_id=current_user.id, message=form.message.data)
        db.session.add(alert)
        db.session.commit()
        socketio.emit('alert', {'type': 'alert', 'message': form.message.data}, broadcast=True)
        flash('Alert sent successfully!', 'success')
        return redirect(url_for('main.profile'))
    return render_template('alerts.html', form=form)

@bp.route('/location', methods=['GET', 'POST'])
@login_required
def location():
    form = LocationForm()
    if form.validate_on_submit():
        location = Location(user_id=current_user.id, latitude=form.latitude.data, longitude=form.longitude.data)
        db.session.add(location)
        db.session.commit()
        flash('Location updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    return render_template('location.html', form=form)

@bp.route('/medication', methods=['GET', 'POST'])
@login_required
def medication():
    form = MedicationForm()
    if form.validate_on_submit():
        medication = Medication(user_id=current_user.id, name=form.name.data, dose=form.dose.data, time=form.time.data)
        db.session.add(medication)
        db.session.commit()
        flash('Medication added successfully!', 'success')
        return redirect(url_for('main.profile'))
    return render_template('medication.html', form=form)

@bp.route('/activities', methods=['GET', 'POST'])
@login_required
def activities():
    form = ActivityForm()
    if form.validate_on_submit():
        activity = Activity(user_id=current_user.id, description=form.description.data)
        db.session.add(activity)
        db.session.commit()
        flash('Activity logged successfully!', 'success')
        return redirect(url_for('main.profile'))
    return render_template('activities.html', form=form)

@bp.route('/messaging', methods=['GET', 'POST'])
@login_required
def messaging():
    form = MessageForm()
    if form.validate_on_submit():
        recipient = User.query.filter_by(username=form.recipient.data).first()
        if recipient:
            message = Message(sender_id=current_user.id, recipient_id=recipient.id, content=form.content.data)
            db.session.add(message)
            db.session.commit()
            flash('Message sent successfully!', 'success')
        else:
            flash('Recipient not found.', 'danger')
        return redirect(url_for('main.profile'))
    return render_template('messaging.html', form=form)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
