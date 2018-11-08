from his_from_csv import  history_from_csv as hfc

dbase1=hfc("EURUSD","60")
d="2018.01.14"
t='11:00'
d2="2010.03.11"
print (d>d2)
   
l=3
db=dbase1.get_history(d,t,l)
print (db)
