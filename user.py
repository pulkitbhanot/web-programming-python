import hashlib

salt = "aswqwgz"

# class that converts that handles generation of salted hash for passwords and conversion of individual request variable to a user dict
class User:

    def create_from_form(self, form):
        self.email = form.get("email")
        db_password = form.get("password") + salt
        h = hashlib.md5(db_password.encode())
        self.password = h.hexdigest()
        self.firstname = form.get("firstname")
        self.lastname = form.get("lastname")

    def get_salted_password(self, password):
        db_password = password + salt
        h = hashlib.md5(db_password.encode())
        return h.hexdigest()
