from flask_app.config.mysqlconnnection import connectToMySQL
from flask_app.models import users_model
from flask import flash

class Plant:
    db = "plant_haven"

    def __init__(self,data):
        self.id = data['id']
        self.plant_name = data['plant_name']
        self.type = data['type']
        self.info = data['info']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner = None

#CREATE
    @classmethod
    def new_plant(cls,data):
        query="""INSERT INTO plants(plant_name, type, info, user_id)
        VALUES (%(plant_name)s, %(type)s, %(info)s, %(user_id)s);"""
        results = connectToMySQL(cls.db).query_db(query,data)
        return results

#READ
    @classmethod
    def get_all_plants(cls):
        query="SELECT * FROM plants LEFT JOIN users ON plants.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        if not results:
            return []
        print("**********************")
        print(results)
        plants = [] 
        this_plant = None
        for row in results:
            if this_plant == None or this_plant.id != row['id']:
                this_plant = cls(row)
                data = {
                    'id':row["users.id"],
                    'first_name':row["first_name"],
                    'last_name':row["last_name"],
                    'email':row["email"],
                    'password':row["password"],
                    'created_at':row["users.created_at"],
                    'updated_at':row["users.updated_at"]
                }
                this_plant.owner = users_model.User(data)
                plants.append(this_plant)
        print("Get All")
        return plants

    @classmethod
    def view_plant(cls,id):
        data = {"id":id}
        query = """SELECT * FROM plants
        LEFT JOIN users ON plants.user_id = users.id
        WHERE plants.id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query,data)
        this_plant = cls(results[0])
        data = {
            'id':results[0]["users.id"],
            'first_name':results[0]["first_name"],
            'last_name':results[0]["last_name"],
            'email':results[0]["email"],
            'password':results[0]["password"],
            'created_at':results[0]["users.created_at"],
            'updated_at':results[0]["users.updated_at"]
        }
        this_owner = users_model.User(data)
        this_plant.owner = this_owner
        print(this_plant)
        return this_plant
    
#validiate plant
    @staticmethod
    def validate_plant(plant):
        print(plant)
        is_valid=True
        if len(plant['plant_name']) < 3:
            flash("Plant name must contain at least 3 characters.")
            is_valid = False
        if len(plant['type']) < 3:
            flash("Plant type must contain at least 3 characters.")
            is_valid = False
        return is_valid
    

#    @staticmethod
#    def validate_plant(plant):
#        print(plant)
#        is_valid = True
#        if len(plant.get('plant_name', '')) < 3:
#            flash("Plant name must contain at least 3 characters.")
#            is_valid = False
#        if len(plant.get('type', '')) < 3:
#            flash("Plant type must contain at least 3 characters.")
#            is_valid = False
#        return is_valid

#UPDATE
    @classmethod
    def update_plant(cls,data):
        query = """UPDATE plants SET
        plant_name = %(plant_name)s,
        type = %(type)s,
        info = %(info)s
        WHERE id = %(id)s
        AND plants.user_id = %(user_id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    
#DELETE
    @classmethod
    def delete_plant(cls,id):
        data = {'id':id}
        query = "DELETE FROM plants WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    