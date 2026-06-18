from enum import Enum as pyEnum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship


db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped [str] = mapped_column (String (20), nullable = False)
    surname: Mapped [str] = mapped_column (String (20), nullable = False)
    username: Mapped [str] = mapped_column (String (10), unique = True, nullable = False)
    email: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String (20), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "username": self.username,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped [str] = mapped_column (String (20), nullable = False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class Gender (pyEnum):
    Female = 1
    Male = 2

class Species (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped [str] = mapped_column (String (20), nullable = False)
    language: Mapped [str] = mapped_column (String(20))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "language": self.language
        }

class People (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped [str] = mapped_column (String (20), nullable = False)
    description: Mapped [str] = mapped_column (String ())

    planet_id: Mapped [int]= mapped_column (ForeignKey ("planet.id"))
    planet: Mapped [Planet] = relationship ()

    species_id: Mapped [int]= mapped_column (ForeignKey ("species.id"))
    species: Mapped [Species] = relationship ()

    gender: Mapped [Gender] = mapped_column (Enum (Gender))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "descripcion": self.description,
            "planet": {
                "id": self.planet.id,
                "name": self.planet.name,
            } if self.planet else None,
            "specie": {
                "id": self.specie.id,
                "name": self.specie.name
            } if self.specie else None,
            "gender": self.gender.value
        }

class Vehicle (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped [str] = mapped_column (String (20), nullable = False)
    description: Mapped [str] = mapped_column (String ())

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

class Favorite (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped [int]= mapped_column (ForeignKey ("user.id"))
    user: Mapped [User] = relationship ()

    people_id: Mapped [int] = mapped_column (ForeignKey ("people.id"))
    people: Mapped [People] = relationship ()

    planet_id: Mapped [int] = mapped_column (ForeignKey ("planet.id"))
    planet: Mapped [Planet] = relationship ()

    vehicle_id: Mapped [int] = mapped_column (ForeignKey ("vehicle.id"))
    vehicle: Mapped [Vehicle] = relationship ()

    def serialize(self):
        return {
            "id": self.id,
            "user": {
                "id":self.user.id,
                "name": self.user.name,
            } if self.user else None,
            "people": {
                "id": self.people.id,
                "name": self.people.name
            } if self.people else None,
            "planet": {
                "id": self.planet.id,
                "name": self.planet.name
            } if self.planet else None,
            "vehicle": {
                "id": self.vehicle.id,
                "name": self.vehicle.name
            } if self.vehicle else None,
        }