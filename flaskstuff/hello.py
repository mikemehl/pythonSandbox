from flask import Flask, render_template, flash, redirect, url_for, request
from flask import render_template
from peewee import *
from GuestEntry import GuestEntry
from EntryForm import EntryForm
import datetime 

app = Flask(__name__);
app.config.update(TESTING='true', SECRET_KEY=b'se09u23t9o4hx0-iuf-9');

db = SqliteDatabase('example.db');

if not db.connect(): assert(False);

def sign_guestbook(form):
   now = datetime.datetime.now();
   if form.errors:
      flash('An error occured.');
      return False; 
   else:
       try:
          #Add the entry to the guestbook.
          new_entry = GuestEntry(name = form.name.data, \
                                 date = now, \
                                 msg  = form.msg.data,   \
                                 cat  = form.cat.data);
          new_entry.save();
          #Let them know it was good.
          flash('Thanks for signing!');
       except Exception as e:
          app.logger.debug(e);
          flash('An error occured.');
          return False;
   return True;

@app.route('/', methods=['GET'])
def index():
   return redirect(url_for('guestbook'));

@app.route('/guestbook', methods=['GET', 'POST'])
def guestbook():
   entries = GuestEntry.select().order_by(GuestEntry.date);
   form = EntryForm()
   if request.method == 'POST':
      if form.validate_on_submit():
         if sign_guestbook(form):
            return redirect(url_for('guestbook'));
      else:
         flash('There was an error validating the form. Did you fill out all fields?');
   return render_template('hello.html', entries=entries, form=form);

if __name__ == '__main__':
   app.run(debug=True);


