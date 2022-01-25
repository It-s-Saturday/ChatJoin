
from curses.ascii import US
from re import U


class User:
    def  __init__(self,name):
        self.name = name
        self.notify_list = []

    
    def notify(self, any_username):
        if any_username in self.notify_list:
            return True
        else:
            return False
    


    





    








