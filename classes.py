from dataclasses import dataclass
from skills import FuryPunch, HardShot, Skill
@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill

class WarriorClass(UnitClass):

    name = "warrior"
    max_health = 60
    max_stamina = 30
    attack = 0.8
    stamina = 0.9
    armor = 1.2
    skill = FuryPunch()


# TODO Инициализируем экземпляр класса UnitClass и присваиваем ему необходимые значения аттрибуотов

class ThiefClass(UnitClass):

    name = "thief"
    max_health = 50
    max_stamina = 25
    attack = 1.2
    stamina = 1.5
    armor = 1.0
    skill = HardShot()

# TODO действуем так же как и с войном

unit_classes = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass
}