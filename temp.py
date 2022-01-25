class User:
    def __init__(self, name):
        self.name = name
        self.lst = []
    def notify(self, any_username):
        if any_username in self.lst:
            return True
        else:
            return False

user_mostafa = User('m-way')
print(user_mostafa.name)
user_mostafa.lst = ['Jibran', 'James', 'Rhyan']

print(user_mostafa.notify())


