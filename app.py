import json

from flask import Flask, render_template, request, redirect, url_for
from classes import unit_classes
from equipment import Equipment
from base import Arena
from typing import TYPE_CHECKING, Any
from unit import PlayerUnit, EnemyUnit



app = Flask(__name__, template_folder='C:\\Users\\Aleksei\\PycharmProjects\\kursovaia_4\\templates')


heroes = {
    "player": Any,
    "enemy": Any
}

arena = Arena()
# TODO инициализируем класс арены


@app.route("/")
def menu_page():
    # TODO рендерим главное меню (шаблон index.html)
    return render_template('index.html')

@app.route("/choose-hero/", methods=['POST', 'GET'])
def choose_hero():

    if request.method == 'GET':

        not_json_result = {}

        all_players = [player for player in heroes]
        all_unit_classes = [item for item in unit_classes]
        all_weapons = Equipment().get_weapons_names()
        all_armors = Equipment().get_armors_names()

        not_json_result["header"] = all_players[0]
        not_json_result["classes"] = all_unit_classes
        not_json_result["weapons"] = all_weapons
        not_json_result["armors"] = all_armors

        return render_template('hero_choosing.html', result=not_json_result)

    if request.method == 'POST':

        player_name = request.form["name"]
        player_class_name = request.form["unit_class"]
        player_unit_class = unit_classes[player_class_name]
        player_weapon_name = request.form["weapon"]
        player_armor_name = request.form["armor"]
        player_weapon = Equipment().get_weapon(weapon_name=player_weapon_name)
        player_armor = Equipment().get_armor(armor_name=player_armor_name)

        player = PlayerUnit(name=player_name, unit_class=player_unit_class, weapon=player_weapon, armor=player_armor)
        heroes["player"] = player

        return redirect('/choose-enemy/', code=302)

    # TODO кнопка выбор героя. 2 метода GET и POST
    # TODO на GET отрисовываем форму.
    # TODO на POST отправляем форму и делаем редирект на эндпоинт choose enemy


@app.route("/choose-enemy/", methods=['POST', 'GET'])
def choose_enemy():

    if request.method == 'GET':

        not_json_result = {}

        all_players = [player for player in heroes]
        all_unit_classes = [item for item in unit_classes]
        all_weapons = Equipment().get_weapons_names()
        all_armors = Equipment().get_armors_names()

        not_json_result["header"] = all_players[1]
        not_json_result["classes"] = all_unit_classes
        not_json_result["weapons"] = all_weapons
        not_json_result["armors"] = all_armors

        return render_template('hero_choosing.html', result=not_json_result)

    if request.method == 'POST':

        enemy_name = request.form["name"]
        enemy_class_name = request.form["unit_class"]
        enemy_unit_class = unit_classes[enemy_class_name]
        enemy_weapon_name = request.form["weapon"]
        enemy_armor_name = request.form["armor"]
        enemy_weapon = Equipment().get_weapon(weapon_name=enemy_weapon_name)
        enemy_armor = Equipment().get_armor(armor_name=enemy_armor_name)

        enemy = EnemyUnit(name=enemy_name, unit_class=enemy_unit_class, weapon=enemy_weapon, armor=enemy_armor)
        heroes["enemy"] = enemy

        return redirect('/fight/', code=302)

    # TODO кнопка выбор соперников. 2 метода GET и POST
    # TODO также на GET отрисовываем форму.
    # TODO а на POST отправляем форму и делаем редирект на начало битвы


@app.route("/fight/", methods=['GET', 'POST'])
def start_fight():

    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])

    return render_template('fight.html', heroes=heroes)

    # TODO выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
    # TODO рендерим экран боя (шаблон fight.html)


@app.route("/fight/hit")
def hit():

    if arena.game_is_running == True:

        arena.player_hit()
        return render_template('fight.html', heroes=heroes)

    # TODO кнопка нанесения удара
    # TODO обновляем экран боя (нанесение удара) (шаблон fight.html)
    # TODO если игра идет - вызываем метод player.hit() экземпляра класса арены
    # TODO если игра не идет - пропускаем срабатывание метода (просто рендерим шаблон с текущими данными)
    else:
        return render_template('fight.html', heroes=heroes)


@app.route("/fight/use-skill")
def use_skill():
    # TODO кнопка использования скилла
    # TODO логика практикчески идентична предыдущему эндпоинту
    if arena.game_is_running == True:
        arena.player_use_skill()
        return render_template('fight.html', heroes=heroes)

    else:

        return render_template('fight.html', heroes=heroes)


@app.route("/fight/pass-turn")
def pass_turn():
    arena.next_turn()
    # TODO кнопка пропус хода
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    # TODO однако вызываем здесь функцию следующий ход (arena.next_turn())
    if arena.game_is_running == True:
        arena.next_turn()
        return render_template('fight.html', heroes=heroes)

    else:

        return render_template('fight.html', heroes=heroes)


@app.route("/fight/end-fight")
def end_fight():
    # TODO кнопка завершить игру - переход в главное меню
    return render_template("index.html", heroes=heroes)



if __name__ == "__main__":
    app.run(debug=True)
