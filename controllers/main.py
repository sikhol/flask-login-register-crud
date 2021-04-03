
import os
import sys
from flask import jsonify,render_template,send_file, request,flash, redirect ,url_for,session,send_file, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

from sqlalchemy.orm import sessionmaker
import argparse
from datatables import ColumnDT, DataTables
import time
import datetime
from datetime import datetime
from helpers.forms import RegisterForm, LoginForm, addBarangForm
import json
from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextAreaField, IntegerField
from wtforms.widgets import TextArea
from sqlalchemy.exc import InvalidRequestError
from flask_login import login_required, current_user,logout_user

from config.settings import db

from model.Models import Users, Users_Barang, Users_Barang


index = Blueprint('index', __name__)

@index.route('/result', methods=['GET'])
@login_required
def result():
    try:
        return render_template('frontend.html')
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()


@index.route('/page_test', methods=['GET', 'POST'])
@login_required
def page_test():
    try:
        columns = [
            ColumnDT(Users_Barang.nama_barang),
            ColumnDT(Users_Barang.berat),
            ColumnDT(Users_Barang.jenis_barang),
            ColumnDT(Users_Barang.harga_beli),
            ColumnDT(Users_Barang.harga_jual),
            ColumnDT(Users_Barang.stok),

        ]

        query = db.session.query(Users_Barang).filter_by(user_id=session['id'])
        params = request.args.to_dict()
        rowTable = DataTables(params, query, columns)
        array=[]
        for item in rowTable.output_result()['data']:
            item['0'] = item['0'].serialized
            array.append(item['0'])
        return jsonify(array)
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()

@index.route('/create',methods=['GET','POST'])
@login_required
def create():
    try:
        form = addBarangForm(request.form)

        if request.method == 'POST' and form.validate():
            print('dd')
            new_barang=Users_Barang(
                user_id= session['id'],
                nama_barang= form.name.data,
                berat= form.berat_barang.data,
                jenis_barang= form.jenis_barang.data,
                harga_beli= form.harga_beli.data,
                harga_jual= form.harga_jual.data,
                stok= form.stok.data
            )
            db.session.add(new_barang)
            db.session.commit()

            flash('data successfully input', 'success')
            return redirect(url_for('index.result'))
        elif request.method == 'GET':

            return render_template('add-file.html')
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()


@index.route('/update/<int:id>/', methods = ['GET', 'POST'])
@login_required
def update(id):
    try:
        data=db.session.query(Users_Barang).filter_by(user_id=session['id']).first()
        my_data = db.session.query(Users_Barang).filter_by(id=id).first()
        if request.method == 'POST' and data and my_data:
            my_data.nama_barang = request.form.get("name")
            my_data.berat = request.form.get("berat_barang")
            my_data.jenis_barang = request.form.get("jenis_barang")
            my_data.harga_beli= request.form.get("harga_beli")
            my_data.harga_jual=request.form.get("harga_jual")
            my_data.stok=request.form.get("stok")

            db.session.commit()
            flash("Data  Successfully Updated", "success")
            return redirect(url_for('index.result'))

        return render_template('edit.html',my_data=my_data)
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()

@index.route('/delete/<id>/', methods = ['GET', 'POST'])
@login_required
def delete(id):
    try:
        data=db.session.query(Users_Barang).filter_by(user_id=session['id']).first()
        if data:
            my_data = Users_Barang.query.get(id)
            db.session.delete(my_data)
            db.session.commit()
            flash("Data Successfully Deleted")
            return redirect(url_for('index.result'))
        else:
            flash("something went wrong", "Danger")
            return redirect(url_for('index.update'))
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()

@index.route('/', methods=['GET', 'POST'])
def login():
    try:

        form = LoginForm(request.form)

        if request.method == 'POST' and form.validate:

            user = db.session.query(Users).filter_by(username=form.username.data).first()

            if user:

                if check_password_hash(user.password, form.password.data):

                    flash('You have successfully logged in.', "success")
                    session['logged_in'] = True
                    session['id'] = user.id
                    session['email'] = user.email
                    session['username'] = user.username
                    session['name'] = user.name
                    login_user(user, remember=True)
                    return redirect(url_for('index.result'))
                else:
                    flash('Username or Password Incorrect', "Danger")
            else:
                flash('Username or Password Incorrect', "Danger")

                return redirect(url_for('index.login'))

        return render_template('login.html', form=form)

    except InvalidRequestError:
        db.session.rollback()
        raise
    finally:
        db.session.close()

@index.route('/register/', methods = ['GET', 'POST'])
def register():
    try:
        form = RegisterForm(request.form)
        if request.method == 'POST' and form.validate():

            type_akun= request.form.get("type_akun") or None
            email= db.session.query(Users).filter_by(email=form.email.data).first()
            if email:
                flash('Your email already registered', 'danger')
                return redirect(url_for('index.register'))
            username= db.session.query(Users).filter_by(email=form.username.data).first()
            if username:
                flash('Your email already exist', 'danger')
                return redirect(url_for('index.register'))
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = Users(
                name = form.name.data,
                username = form.username.data,
                email = form.email.data,
                password = hashed_password,
                phone = form.phone.data,
                domisili = form.domisili.data,
                industry = form.industry.data,
                upgrade_status = 0,
                type_akun=type_akun
            )
            db.session.add(new_user)
            db.session.commit()
            flash('You have successfully registered', 'success')
            return redirect(url_for('index.login'))
        else:
            return render_template('register.html', form = form)
    except :
        db.session.rollback()
        raise
    finally:
        db.session.close()

@index.route('/logout/')
@login_required
def logout():
    # Tell Flask-Login to destroy the
    # session->User connection for this session.
    try:
        logout_user()
        return redirect(url_for('index.login'))
    except :
        db.session.rollback()
        raise
    finally:
        db.session.close()

@index.route('/profile/',methods=['POST', 'GET'])
@login_required
def profile():
    profile=db.session.query(Users).filter_by(id=session['id']).first_or_404()
    try:
        if request.method == 'POST':
            email = request.form.get("email")
            name =request.form.get('name')
            username = request.form.get('username')
            password = request.form.get('password') or None
            industry = request.form.get('industry')
            phone = request.form.get('phone')
            domisili = request.form.get('domisili')

            profile.email= email
            profile.name=name
            profile.industry=industry
            profile.username=username
            profile.phone=phone
            profile.domisili=domisili
            if password is not None:
                profile.password= generate_password_hash(password, method='sha256')
            db.session.commit()
            flash('update data berhasil', "success")
            return redirect(url_for('index.result'))
        return render_template('profile.html',profile=profile)

    except:

        db.session.rollback()
        raise
    finally:
        db.session.close()




