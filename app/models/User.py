from system.core.model import Model
import re

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def create_user(self,info):
        users = self.db.query_db("SELECT * FROM users")
        for user in users:
            if user['username'] == info['username']:
                errors.append('Username already exists')
            if user['email'] == info['email']:
                errors.append('Email already exists')
        EMAIL_REGEX = re.compile(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        if not info['username']:
            errors.append('Username cannot be blank')
        elif len(info['username']) < 5:
            errors.append('Username must be at least 5 characters long')
        if not info['first_name'] or not info['last_name']:
            errors.append('Name cannot be blank')
        elif len(info['first_name']) < 2 or len(info['last_name']) < 2:
            errors.append('Name must be at least 2 characters long')
        if not info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid!')
        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8 or len(info['pw_confirmation'])<8:
            errors.append('Password must be at least 8 characters long')
        elif info['password'] != info['pw_confirmation']:
            errors.append('Password and confirmation must match!')
        if errors:
            return {"status": False, "errors": errors}
        else:
            hashed_pw = self.bcrypt.generate_password_hash(info['password'])

            query = "INSERT INTO users (username,first_name,last_name,email,password,created_at) VALUES (%s,%s,%s,%s,%s,NOW())"
            data = [info['username'],info['first_name'],info['last_name'],info['email'],hashed_pw]
            self.db.query_db(query,data)

            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(get_user_query)
            return { "status": True, "user": users[0] }

    def login_user(self, info):
        EMAIL_REGEX = re.compile(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        if not info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid!')
        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        password = info['password']
        user_query = "SELECT * FROM users WHERE email = %s LIMIT 1"
        user_data = [info['email']]
        users = self.db.query_db(user_query, user_data)
        if users:
            if self.bcrypt.check_password_hash(users[0]['password'], password):
                return {'status': True, 'user' : users[0] }
            else:
                errors.append('Email/Password does not match')
        else:
            errors.append('Email not found. Register please!')
        if errors:
            return {'status': False, "errors": errors}

        return False

    def get_user_by_id(self,user_id):
        return self.db.query_db("SELECT * FROM users WHERE id = %s",[user_id])
