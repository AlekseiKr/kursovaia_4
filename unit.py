from __future__ import annotations

import random
from abc import ABC, abstractmethod
from equipment import Weapon, Armor
from classes import UnitClass
from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass, weapon: Weapon, armor: Armor):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = weapon
        self.armor = armor
        self._is_skill_used = False

    @property
    def health_points(self):
        return f"Здоровье {self.hp}"
        # TODO возвращаем аттрибут hp в красивом виде

    @property
    def stamina_points(self):
        return f"Энергия {self.stamina}"
        # TODO возвращаем аттрибут hp в красивом виде

    def equip_weapon(self): # убрал аргумент weapon
        # TODO присваиваем нашему герою новое оружие
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self): # убрал аргумент armor
        # TODO одеваем новую броню
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> float:
        # TODO Эта функция должна содержать:
        #  логику расчета урона игрока
        #  логику расчета брони цели
        #  здесь же происходит уменьшение выносливости атакующего при ударе
        #  и уменьшение выносливости защищающегося при использовании брони
        #  если у защищающегося не хватает выносливости - его броня игнорируется
        #  после всех расчетов цель получает урон - target.get_damage(damage)
        #  и возвращаем предполагаемый урон для последующего вывода пользователю в текстовом виде

        damage = round(random.uniform(self.weapon.min_damage, self.weapon.max_damage), 2)

        self.stamina -= self.weapon.stamina_per_hit

        if target.stamina < target.armor.stamina_per_turn:

            target.get_damage(damage, target)

        return damage

    def get_damage(self, damage: float, target: BaseUnit) -> Optional[float]:

        target.hp -= damage
        if target.hp < 0:
            target.hp = 0

        return target.hp

        # TODO получение урона целью
        #      присваиваем новое значение для аттрибута self.hp


    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        Этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        Метод использования умения.
        Если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернем нам строку, которая характеризует выполнение умения
        """
        if self._is_skill_used == True:

            return f"Навык использован ранее"
        else:
            return self.unit_class.skill.use(user=self, target=target)

class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        Вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """

        if self.stamina >= self.weapon.stamina_per_hit:

            damage = self._count_damage(target)
            print(damage, self.name)

            if damage > target.armor.defence:

                damage = abs(target.armor.defence - damage)
                target.armor.defence = 0
                target.get_damage(damage, target)

                return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."

            else:

                target.armor.defence -= damage

                return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."

        else:

            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        # TODO результат функции должен возвращать следующие строки:


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target
        """

        if self._is_skill_used == True:

            if self.stamina >= self.weapon.stamina_per_hit:

                damage = self._count_damage(target)
                print(damage, self.name)

                if damage > target.armor.defence:

                    damage = abs(target.armor.defence - damage)
                    target.armor.defence = 0
                    target.get_damage(damage, target)

                    return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона."

                else:

                    target.armor.defence -= damage
                    return f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его останавливает."

            else:

                return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        else:

            return self.use_skill(target=target)
