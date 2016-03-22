from system.core.controller import *

class Shoes(Controller):
    def __init__(self, action):
        super(Shoes, self).__init__(action)
        self.load_model('User')
        self.load_model('Shoe')


    def index(self):
    	reviews = self.models['Shoe'].front_page_reviews()
    	shoes = self.models['Shoe'].get_all_shoes()

    	return self.load_view('/shoes/index.html',reviews=reviews,shoes=shoes)

    def show(self,shoe_id):
    	reviews = self.models['Shoe'].get_reviews_by_id(shoe_id)
    	shoe = self.models['Shoe'].get_shoe_by_id(shoe_id)
    	return self.load_view('/shoes/show.html', shoe=shoe[0], reviews = reviews)

    def new_review(self):
    	shoes = self.models['Shoe'].get_all_shoes_by_brand()
    	nums = []
    	for x in range(6,16):
    		nums.append(float(x))
    		nums.append(x + 0.5)
    	return self.load_view('/shoes/add_review.html',nums=nums,shoes=shoes)

    def create_review(self):
    	info = {
    		'size' : request.form['size'],
    		'rating' : request.form['rating'],
    		'fit' : request.form['fit'],
    		'comfort' : request.form['comfort'],
    		'durability' : request.form['durability'],
    		'content' : request.form['content'],
    		'user_id' : session['id']
    	}

    	if request.form['shoe_id'] != "None":
    		info['shoe_id'] = request.form['shoe_id']
    	elif request.form['brand'] and request.form['name'] and request.form['pic']:
    		info['brand'] = request.form['brand']
    		info['name'] = request.form['name']
    		info['category'] = request.form['category']
    		info['pic'] = request.form['pic']
    	else:
    		flash("Invalid Shoe Input")
    		return redirect('/new_review')

    	self.models['Shoe'].add_review(info)
    	return redirect('/shoes')

    def profile(self,user_id):
    	user = self.models['User'].get_user_by_id(user_id)
    	reviews = self.models['Shoe'].get_reviews_by_user(user_id)
    	return self.load_view('/shoes/profile.html',user=user[0], reviews=reviews)



