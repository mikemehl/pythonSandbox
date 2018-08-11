from peewee import *
import csv
import time
from datetime import date
from GuestEntry import *

def main():
   print("Creating database...");
   db = SqliteDatabase('example.db')
   if not db.connect(): assert(False);
   db.drop_tables([GuestEntry]);
   db.create_tables([GuestEntry]);
   with open('sample.csv', 'r') as samplecsv:
      samples = csv.reader(samplecsv);
      next(samples); #Skip the header.
      for line in samples:
         try:
            name  = line[0];
            year  = int(line[1][0:4]);
            month = int(line[1][4:6]);
            day   = int(line[1][6:8]);
            msg   = line[2];
            cat   = 'T';
            entry = GuestEntry(name=name, date=date(year, month, day), msg=msg, cat=cat);
            entry.save()
         except:
            continue
   for entry in GuestEntry.select():
      print('Name: %5s\t Date: %s' % (entry.name, entry.date));
   return;

if __name__ == "__main__":
   main()
