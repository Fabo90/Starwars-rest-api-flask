from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False, unique=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    favorites = db.relationship('Favorites', backref='user')
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "user_name": self.user_name
            # do not serialize the password, its a security breach
        }

   


class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True) 
   # user = db.relationship('User', back_populates='favorites')
   # character = db.relationship('Character', back_populates='favorites')
   # planet = db.relationship('Planet', back_populates='favorites')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
            # do not serialize the password, its a security breach
        }
   



class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    height = db.Column(db.Integer, nullable=False, unique=False)
    mass = db.Column(db.Integer, nullable=False, unique=False)
    hair_color = db.Column(db.String(15), nullable=False, unique=False)
    skin_color = db.Column(db.String(15), nullable=False, unique=False)
    eye_color = db.Column(db.String(15), nullable=False, unique=False)
    birth_year = db.Column(db.String(15), nullable=False, unique=False)
    gender = db.Column(db.String(15), nullable=False, unique=False)
   # favorite_id = db.Column(db.Integer, db.ForeignKey('favorites.id'))
   # favorite = db.relationship('Favorites')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
           # "favorite_id": self.favorite_id,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    rotation_period = db.Column(db.Integer, nullable=False, unique=False)
    orbital_period = db.Column(db.Integer, nullable=False, unique=False)
    diameter = db.Column(db.Integer, nullable=False, unique=False)
    climate = db.Column(db.String(15), nullable=False, unique=False)
    gravity = db.Column(db.String(15), nullable=False, unique=False)
    terrain = db.Column(db.String(15), nullable=False, unique=False)
    population = db.Column(db.Integer, nullable=False, unique=False)
    # favorite_id = db.Column(db.Integer, db.ForeignKey('favorites.id'))
    # favorite = db.relationship('Favorites', back_populates='planet')
    

    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "population": self.population,
            # "favorite_id": self.favorite_id,
            # do not serialize the password, its a security breach
        }