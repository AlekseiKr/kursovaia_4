from dataclasses import dataclass
from typing import List
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:

    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:

    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        return round(uniform(self.min_damage, self.max_damage), 2)

@dataclass
class EquipmentData:
    # TODO содержит 2 списка - с оружием и с броней
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name: str) -> Weapon:
        # TODO возвращает объект оружия по имени
        for weapon in self.equipment.weapons:
            if weapon_name in weapon.__dict__['name']:
                return weapon

    def get_armor(self, armor_name: str) -> Armor:
        # TODO возвращает объект брони по имени
        for armor in self.equipment.armors:
            if armor_name in armor.__dict__['name']:
                return armor

    def get_weapons_names(self) -> list:
        self.weapons_names = []
        for weapon in self.equipment.weapons:
            self.weapons_names.append(weapon.__dict__['name'])
        # TODO возвращаем список с оружием
        return self.weapons_names

    def get_armors_names(self) -> list:
        # TODO возвращаем список с броней
        self.armors_names = []
        for armor in self.equipment.armors:
            self.armors_names.append(armor.__dict__['name'])
        # TODO возвращаем список с оружием
        return self.armors_names

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        # TODO этот метод загружает json в переменную EquipmentData
        equipment_file = open("C:\\Users\\Aleksei\\PycharmProjects\\kursovaia_4\\data\\equipment.json", "r", encoding="utf-8")
        data = json.load(equipment_file)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError

# weapon = Weapon(id=1, name='топорик', min_damage=2.5, max_damage=4.1, stamina_per_hit=1.8)
# print(weapon.damage)


