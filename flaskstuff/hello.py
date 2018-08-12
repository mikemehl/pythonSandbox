from flask import Flask, render_template, flash, redirect, url_for, request
from flask import render_template
from peewee import *
from GuestEntry import GuestEntry
from EntryForm import EntryForm

app = Flask(__name__);
app.config.update(TESTING='true', SECRET_KEY=b'se09u23t9o4hx0-iuf-9');

db = SqliteDatabase('example.db');

if not db.connect(): assert(False);

@app.route('/', methods=['GET', 'POST'])
def hello_world():
   entries = GuestEntry.select()   
   names = [entry.name for entry in entries];
   form = EntryForm()
   if request.method == 'POST':
      app.logger.debug('POST made.');
      if form.validate_on_submit():
         app.logger.debug('Form was valid.');
         flash('Thanks for signing!');
         return redirect(url_for('hello_world'));
      else:
         app.logger.debug(form.errors);
   return render_template('hello.html', names=names, form=form);

@app.route('/thanks', methods=['GET'])
def thanks():
   return redirect(url_for('hello_world'));

if __name__ == '__main__':
   app.run(debug=True);
