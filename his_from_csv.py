import csv 
    
class history_from_csv:
    
    def __init__(self, symbol, tf):

        self.file="history//"+symbol+tf+".csv"

    def get_history(self, date, time, len_bar):
        
        self.date=str(date)
        self.time=str(time)
        self.len_bar=len_bar

        with open(self.file,"r") as f_obj:

            self.db=self.csv_reader(f_obj)
            return self.db

    def csv_reader(self, file_obj):
        self.reader = csv.reader(file_obj)
        
        self.data_read = []
        self.cou=0
        self.w_cou=0
        self.cl=False
        for self.row in self.reader:
            
            if self.row[0]==self.date and self.row[1]==self.time:
                self.w_cou=self.len_bar
                self.cl=True
                
            if self.cl==False and self.row[0]>self.date:
                self.w_cou=self.len_bar
                self.cl=True
                
            if self.cl==True and self.w_cou!=0:
                self.data_read.append(self.row)
                self.w_cou=self.w_cou-1
                
            if self.cl==True and self.w_cou==0:
                break
        return self.data_read


    