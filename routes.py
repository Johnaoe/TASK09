from flask import redirect, request, render_template, flash, url_for
from flask_login import logout_user, login_user, login_required, current_user
from flask_bcrypt import Bcrypt
from . import mod
from flask_login import logout_user, login_user, login_required, current_user
from . import User, Admin, Cars, CarService, forms, db, admin

admin.add_view(Admin(User, db.session))
admin.add_view(Admin(Cars, db.session))
admin.add_view(Admin(CarService, db.session))
bcrypt = Bcrypt(mod)

@mod.route("/admin")
@login_required
def admin():
    return redirect(url_for(admin))

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

@mod.route("/admin")
@login_required
def admin():
    return redirect(url_for(admin))


@mod.route('/')
def home():
    db.session.rollback()
    return render_template('base.html', current_user=current_user)


@mod.route('/registracija', methods=['GET', 'POST'])
def registracija():
    if current_user.is_authenticated:
        flash('Priregistruoti naują vartotoją.')
        return redirect(url_for('home'))
    form = forms.RegForm()
    if form.validate_on_submit():
        New_user = User.query.filter_by(email=form.email.data).first()
        if New_user is None:
            koduotas_slaptazodis = bcrypt.generate_password_hash(form.passw.data).decode('utf-8')
            pirmo_vartotojo_tikrinimas = not User.query.first()
            naujas_vartotojas = User(
                vardas = form.name.data,
                el_pastas = form.email.data,
                slaptazodis1 = koduotas_slaptazodis,
                is_admin = pirmo_vartotojo_tikrinimas
            )
            db.session.add(naujas_vartotojas)
            db.session.commit()
            flash('Sėkmingai prisiregistravote', 'success')
        else:
            flash('Toks vartotojas jau egzistuoja')
        return redirect(url_for('home'))
    return render_template('registracija.html', form=form, current_user=current_user)


@mod.route('/prisijungimas', methods=['GET', 'POST'])
def prisijungimas():
    if current_user.is_authenticated:
        flash('Prisijungęs')
        return redirect(url_for('home'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.passw, form.passw.data):
            login_user(user, remember=form.stay.data)
            return redirect(url_for('home'))
        else:
            flash('Prisijungti nepavyko, neteisingas el.paštas arba slaptažodis.', 'danger')
    return render_template('prisijungimas.html', form=form, current_user=current_user)


@mod.route('/automobilio_registracija', methods=['GET', 'POST'])
@login_required
def automobilio_registracija():
    form = forms.CarRegister()
    if form.validate_on_submit():
        naujas_automobilis = Cars(
            marke = form.brand.data,
            modelis = form.model.data,
            pagaminimo_metai = form.years.data,
            variklis = form.engin.data,
            valstybinis_nr = form.number.data,
            vin_kodas = form.vin_nr.data,
            vartotojo_id = current_user.id
        )
        try:
            db.session.add(naujas_automobilis)
            db.session.commit()
        except:
            flash(' VIN kodas jau egzistuoja', 'danger')
        else:
            flash('Sėkmingai užregistravote', 'success')
        return redirect(url_for('automobilio_registracija'))
    return render_template('automobilio_registracija.html', form=form, current_user=current_user)


@mod.route('/manoautomobiliai', methods=['GET', 'POST'])
@login_required
def manoautomobiliai():
    mano_automobiliai = Cars.query.filter_by(user=current_user)
    return render_template('manoautomobiliai.html', mano_automobiliai=mano_automobiliai, current_user=current_user)


@mod.route('/remonto_darbai', methods=['GET', 'POST'])
@login_required
def remonto_darbai():
    form = forms.RepairOrderForm()
    mano_automobiliai = Cars.query.filter_by(user=current_user)
    if form.validate_on_submit():
        nauja_registracija_remontui = CarService(
            statusas = "NAUJAS",
            remonto_kaina = int(),
            gedimo_aprasymas = form.issues.data,
            automobilio_id = request.form.get('pasirinkimas'),
            vartotojo_id = current_user.id
        )
        db.session.add(nauja_registracija_remontui)
        db.session.commit()
        flash('Automobilus užregistruotas', 'success')
        return redirect(url_for('home'))
    return render_template('remonto_darbai.html', form=form, mano_automobiliai=mano_automobiliai, current_user=current_user)


@mod.route('/remontuojami_automobiliai', methods=['GET', 'POST'])
@login_required
def remontuojami_automobiliai():
    if current_user.is_staf:
        remontuojami_automobiliai = CarService.query.filter(CarService.statusas != 'ATIDUOTAS')
        return render_template('remontuojami_automobiliai_redagavimui.html', remontuojami_automobiliai=remontuojami_automobiliai, current_user=current_user)
    else:
        remontuojami_automobiliai = CarService.query.filter_by(user=current_user)
        return render_template('remontuojami_automobiliai.html', remontuojami_automobiliai=remontuojami_automobiliai, current_user=current_user)

@mod.route('/atsijungimas')
def atsijungimas():
    logout_user()
    return redirect(url_for('home'))

@mod.route('/darbu_statusas', methods=['GET', 'POST'])
@login_required
def darbu_statusas(id):
    return render_template('darbu_statusas.html')

@mod.route('/atnaujinti_irasa/<int:id>', methods=['GET', 'POST'])
@login_required
def atnaujinti_irasa(id):
    form = forms.ServiceSatus()
    updated_data = CarService.query.get_or_404(id)
    if request.method == 'POST':
        try:
            updated_data.price = form.price.data
            updated_data.status = form.status.data
            updated_data.issue = form.issue.data
            db.session.commit()
            flash('Atnaujinta info')
            return redirect('/remontuojami_automobiliai')
        except:
            flash('Įvyko klaida')
            return redirect('/remontuojami_automobiliai')
    else:
        form.price.data = updated_data.price
        form.status.data = updated_data.status
        form.issue.data = updated_data.issue
        return render_template('/darbu_statusas.html', form=form, id=id, updated_data=updated_data, current_user=current_user)

@mod.route('/profilis', methods=['GET', 'POST'])
@login_required
def profilis():
    form = forms.ProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Atnaujinta', 'success')
        return redirect(url_for('profilis'))
    elif request.method == "GET":
        form.name.data = current_user.name
        form.email.data = current_user.email
    return render_template('profilis.html', current_user=current_user, form=form)