from peewee import *

db = SqliteDatabase('example.db');

class GuestEntry(Model):
   name = CharField();
   date = DateField();
   msg  = CharField();
   cat  = CharField();

   class Meta:
      database = db;
