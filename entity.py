# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 16:55:22 2025

@author: russ
@model: o4-mini-high

Sample JSON for
{
  "@context": "https://schema.org",
  "@type": "Thing",
  "name": "Entity",
  "description": "A generic entity representing a person, an animal, 
                  a non-biological intelligence, or a legal organization.",
  "subEntities": [
    {
      "@type": "Person",
      "name": "Jane Doe",
      "birthDate": "1980-01-15"
    },
    {
      "@type": "Animal",
      "name": "Fido",
      "animalType": "Dog"
    },
    {
      "@type": "SoftwareApplication",
      "name": "ChatGPT-o8",
      "applicationCategory": "Artificial Intelligence",
      "description": "Non-biological system exhibiting autonomous reasoning."
    },
    {
      "@type": "Corporation",
      "name": "Real Advantage Corporation",
      "legalName": "Real Advantage Corporation",
      "url": "https://realadvantage.ai"
    },
    {
      "@type": "Organization",
      "name": "Sterling Engle Family Trust",
      "legalName": "Sterling Engle Family Trust",
      "additionalType": "https://schema.org/Trust"
    }
  ]
}

    def __init__(self, name, entity_type, interests=None):
        self.name = name
        self.entity_type = entity_type
        self.interests = interests if interests else []

    def __repr__(self):
        return f"Entity(name={self.name}, entity_type={self.entity_type}, interests={self.interests})"

"""
import json
from typing import List
from snowflake import snowflake
from SurfaceLocation import SurfaceLocation

class Thing:
    # def __init__(self, id: int, name: str, description: str = None, 
    def __init__(self, name: str, description: str = None, 
                 birthPlace: SurfaceLocation = None, birthDate = None, 
                 deathPlace: SurfaceLocation = None, deathDate = None):
        self.id = snowflake()
        self.name = name
        self.description = description
        self.birthPlace = birthPlace
        self.birthDate = birthDate
        self.deathPlace = birthPlace
        self.deathDate = birthDate


    def to_jsonld(self) -> dict:
        data = {
            "id": self.id,
            "@type": self.__class__.__name__,
            "name": self.name
        }
        if self.description:
            data["description"] = self.description
        return data

class Person(Thing):
    def __init__(self, name: str, description: str = None, 
                 birthPlace: SurfaceLocation = None, birthDate = None, 
                 deathPlace: SurfaceLocation = None, deathDate = None, gender = None, interests = None):
        super().__init__(name, description, birthPlace, birthDate, deathPlace, deathDate, interests)
        self.interests = interests if interests else []

    def to_jsonld(self) -> dict:
        data = super().to_jsonld()
        data["birthDate"] = self.birthDate
        return data

class Animal(Thing):
    def __init__(self, name: str, animalType: str, description: str = None):
        super().__init__(name, description)
        self.animalType = animalType

    def to_jsonld(self) -> dict:
        data = super().to_jsonld()
        data["animalType"] = self.animalType
        return data

class SoftwareApplication(Thing):
    def __init__(self, name: str, applicationCategory: str, description: str = None):
        super().__init__(name, description)
        self.applicationCategory = applicationCategory

    def to_jsonld(self) -> dict:
        data = super().to_jsonld()
        data["applicationCategory"] = self.applicationCategory
        return data

class Corporation(Thing):
    def __init__(self, name: str, legalName: str, url: str, description: str = None):
        super().__init__(name, description)
        self.legalName = legalName
        self.url = url

    def to_jsonld(self) -> dict:
        data = super().to_jsonld()
        data["legalName"] = self.legalName
        data["url"] = self.url
        return data

class Organization(Thing):
    def __init__(self, name: str, legalName: str, additionalType: str = None, description: str = None):
        super().__init__(name, description)
        self.legalName = legalName
        self.additionalType = additionalType

    def to_jsonld(self) -> dict:
        data = super().to_jsonld()
        data["legalName"] = self.legalName
        if self.additionalType:
            data["additionalType"] = self.additionalType
        return data

class Entity(Thing):
    def __init__(self, name: str, description: str = None, subEntities: List[Thing] = None):
        super().__init__(name, description)
        self.subEntities = subEntities or []

    def to_jsonld(self) -> dict:
        data = {
            "@context": "https://schema.org",
            "@type": "Thing",
            "name": self.name
        }
        if self.description:
            data["description"] = self.description
        data["subEntities"] = [e.to_jsonld() for e in self.subEntities]
        return data

# Example usage
entity = Entity(
    name="Entity",
    description="A generic entity representing a person, an animal, a non-biological intelligence, or a legal organization.",
    subEntities=[
        Person(name="Sterling Jefferson Chiou Engle", birthDate="1995-07-04"),
        Animal(name="Fido", animalType="Dog"),
        SoftwareApplication(name="ChatGPT-o3", applicationCategory="Artificial Intelligence", description="Non-biological system exhibiting autonomous reasoning."),
        Corporation(name="REALagentic AI LLC", legalName="RealAgentic.ai LLC", url="https://REALagentic.ai"),
        Corporation(name="Real Advantage Corporation", legalName="Real Advantage Corporation", url="https://realadvantage.ai"),
        Organization(name="Sterling Engle Family Trust", legalName="Sterling Engle Family Trust", additionalType="https://schema.org/Trust")
    ]
)

# Serialize to JSON-LD and print
jsonld_output = entity.to_jsonld()
print(json.dumps(jsonld_output, indent=2))

