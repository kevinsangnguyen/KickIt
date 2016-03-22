from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')

    def index(self):
        if 'logged_in' in session:
            return redirect('/shoes')
        else:
            return self.load_view('/users/main.html')

    def login_page(self):
        if 'logged_in' in session:
            return redirect('/shoes')
        else:
            return self.load_view('/users/login_page.html')


    def create(self):
        user_info = {
             "username" : request.form['username'],
             "first_name" : request.form['first_name'],
             "last_name" : request.form['last_name'],
             "email" : request.form['email'],
             "password" : request.form['password'],
             "pw_confirmation" : request.form['pw_confirmation']
        }

        create_status = self.models['User'].create_user(user_info)
        if create_status['status'] == True:
            session['id'] = create_status['user']['id']
            session['username'] = create_status['user']['username'] 
            session['name'] = create_status['user']['first_name'] + " " + create_status['user']['last_name']
            session['logged_in'] = True
            return redirect('/shoes')
        else:
            for message in create_status['errors']:
                flash(message, 'regis_errors')
            return redirect('/login_page')

    def login(self):
        user_info = {
            "email" : request.form['email'],
            "password" : request.form['password']
        }
        user = self.models['User'].login_user(user_info)
        if user['status'] == True:
            session['id'] = user['user']['id']
            session['username'] = user['user']['username'] 
            session['name'] = user['user']['first_name'] + " " + user['user']['last_name']
            session['logged_in'] = True
            return redirect('/shoes')
        else:
            for message in user['errors']:
                flash(message,'login_errors')
            return redirect('/login_page')

    def logout(self):
        session.clear()
        return redirect('/')

