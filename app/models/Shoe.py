from system.core.model import Model

class Shoe(Model):
    def __init__(self):
        super(Shoe, self).__init__()

    def front_page_reviews(self):
    	query = "SELECT users.username,shoes.category,shoes.id as shoe_id,shoes.name,shoes.brand,shoes.category,reviews.rating,reviews.user_id,reviews.content,reviews.created_at,reviews.id,reviews.fit,reviews.durability,reviews.comfort,reviews.size FROM reviews LEFT JOIN shoes ON shoes.id = reviews.shoe_id LEFT JOIN users ON users.id = reviews.user_id ORDER BY id DESC LIMIT 3"
    	return self.db.query_db(query)
    def get_reviews_by_id(self,shoe_id):
    	query = "SELECT users.username,shoes.category,shoes.id as shoe_id,shoes.name,shoes.brand,shoes.category,reviews.rating,reviews.user_id,reviews.content,reviews.created_at,reviews.id,reviews.fit,reviews.durability,reviews.comfort,reviews.size FROM reviews LEFT JOIN shoes ON shoes.id = reviews.shoe_id LEFT JOIN users ON users.id = reviews.user_id WHERE shoes.id = %s ORDER BY shoe_id DESC"
    	return self.db.query_db(query,[shoe_id])
    def get_reviews_by_user(self,user_id):
    	query = "SELECT shoes.category,shoes.id as shoe_id,shoes.name,shoes.brand,shoes.category,reviews.rating,reviews.user_id,reviews.content,reviews.created_at,reviews.id,reviews.fit,reviews.durability,reviews.comfort,reviews.size FROM reviews LEFT JOIN shoes ON shoes.id = reviews.shoe_id WHERE reviews.user_id = %s ORDER BY reviews.id DESC"
    	return self.db.query_db(query,[user_id])


    def get_all_shoes(self):
    	return self.db.query_db("SELECT * FROM shoes ORDER by brand ASC")
    def get_all_shoes_by_brand(self):
    	return self.db.query_db("SELECT * from shoes ORDER BY brand ASC")

    def add_review(self,info):
    	if 'shoe_id' in info:
    		query = "INSERT INTO reviews(rating,content,size,comfort,fit,durability,shoe_id,user_id,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NOW())"
    		data = [info['rating'],info['content'],info['size'],info['comfort'],info['fit'],info['durability'],info['shoe_id'],info['user_id']]
    		return self.db.query_db(query,data)
    	elif 'name' in info:
    		query = "INSERT INTO shoes(name,brand,category,pic) VALUES (%s,%s,%s,%s)"
    		data = [info['name'],info['brand'],info['category'],info['pic']]
    		self.db.query_db(query,data)
    		shoe = self.db.query_db("SELECT * from shoes WHERE name = %s",[info['name']])
    		query = "INSERT INTO reviews(rating,content,size,comfort,fit,durability,shoe_id,user_id,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NOW())"
    		data = [info['rating'],info['content'],info['size'],info['comfort'],info['fit'],info['durability'],shoe[0]['id'],info['user_id']]
    		return self.db.query_db(query,data)





    def get_shoe_by_id(self,shoe_id):
    	query = "SELECT * from shoes WHERE id = %s"
    	data = [shoe_id]
    	return self.db.query_db(query,data)

    # def get_shoe_by_id(self, course_id):
    #     # pass data to the query like so
    #     query = "SELECT * FROM courses WHERE id = %s"
    #     data = [course_id]
    #     return self.db.query_db(query, data)

    # def add_course(self, course):
    #   # Build the query first and then the data that goes in the query
    #   query = "INSERT INTO courses (title, description, created_at) VALUES (%s, %s, NOW())"
    #   data = [course['title'], course['description']] # Note that data must be an array
    #   return self.db.query_db(query, data)

    # def update_course(self, course):
    #   # Building the query for the update
    #   query = "UPDATE courses SET title=%s, description=%s WHERE id = %s"
    #   # we need to pass the necessary data
    #   data = [course['title'], course['description'], course['id']]
    #   # run the update
    #   return self.db.query_db(query, data)