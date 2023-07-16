from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unit import BaseUnit

class Skill(ABC):

    """
    Базовый класс умения
    """

    user = None
    target = None

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamina(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass

    @abstractmethod
    def skill_effect(self) -> str:
        pass

    def _is_stamina_enough(self) -> bool:
        return self.user.stamina > self.stamina

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        """
        Проверка, достаточно ли выносливости у игрока для применения умения.
        Для вызова скилла везде используем просто use
        """
        self.target = target
        self.user = user

        if self._is_stamina_enough() == True:
            return self.skill_effect()
        else:
            return f"{self.user.name} попытался использовать {self.name} но у него не хватило выносливости."


class FuryPunch(Skill):

    name = "furypunch"
    stamina = 6
    damage = 12

    def skill_effect(self) -> str:
        # TODO логика использования навыка -> return str
        # TODO в классе нам доступны экземпляры user и target - можно использовать любые их методы
        # TODO именно здесь происходит уменьшение стамины у игрока применяющего умение и
        # TODO уменьшение здоровья цели.
        # TODO результат применения возвращаем строкой

        print('yes')

        self.user.stamina -= self.stamina
        if self.user.stamina < 0:
            self.user.stamina = 0

        if self.target.stamina <= 0:

            self.target.hp = self.target.hp - self.damage
            if self.target.hp < 0:
                self.target.hp = 0

        else:

            self.target.hp = self.target.hp + self.target.armor.defence - self.damage

        return f'Выносливость {self.user.name} уменьшается до {self.user.stamina}, здоровье {self.target.name} уменьшается до {self.target.hp}'


class HardShot(Skill):
    name = "hardshot"
    stamina = 5
    damage = 15

    def skill_effect(self) -> str:

        print('no')

        self.user.stamina -= self.stamina
        if self.user.stamina < 0:
            self.user.stamina = 0

        if self.target.stamina <= 0:

            self.target.hp = self.target.hp - self.damage
            if self.target.hp < 0:
                self.target.hp = 0

        else:

            self.target.hp = self.target.hp + self.target.armor.defence - self.damage

        return f'Выносливость {self.user.name} уменьшается до {self.user.stamina}, здоровье {self.target.name} уменьшается до {self.target.hp}'

