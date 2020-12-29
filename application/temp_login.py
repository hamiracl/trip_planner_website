from werkzeug.security import generate_password_hash, check_password_hash
class User():
    def __init__(self):
        self.users = {}

    def check(self, username, password):
        if self.users.get(username):
            if check_password_hash(self.users.get(username), password):
                return True
        return False

    def add(self, username, password):
        if self.users.get(username):
            return False
        else:
            self.users[username] = generate_password_hash(password)
            return True
    