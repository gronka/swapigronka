import json
import random

import click
import mysql.connector
import requests


class DbTask:
    API = "https://swapi.co/api/"
    CHARACTER_COUNT = 15
    NUMBER_CHARACTERS = 87

    def __init__(self):
        self.db = "db_not_set"
        self.character_infos = "character_infos_not_set"

    def init_db(self):
        db = mysql.connector.connect(
            host="127.0.0.1",
            user="swapiuser",
            passwd="asdf",
            database="swapi",
            auth_plugin="mysql_native_password",
        )
        self.db = db

    def reset_tables(self):
        cursor = self.db.cursor()
        sql = "DELETE FROM characters;"
        cursor.execute(sql)
        self.db.commit()

        sql = "DELETE FROM films;"
        cursor.execute(sql)
        self.db.commit()

    def retrieve_characters(self):
        film_titles = {}
        self.character_infos = []
        querying = True
        while querying:
            _id = random.randint(1, self.NUMBER_CHARACTERS+1)
            if self.character_already_queried(_id):
                continue

            character_req = requests.get(self.API + "people/" + str(_id))
            character_info = character_req.json()
            if "detail" in character_info and \
                    character_info["detail"] == "Not found":
                # Note: The api returns a json object as:
                # {"detail": "Not found"}
                # When a requested ID is not available
                pass
            else:
                # useful for debugging
                # click.echo(_id)
                # click.echo(character_info)

                character_films = []
                for idx, film in enumerate(character_info["films"]):
                    if film not in film_titles:
                        film_req = requests.get(film)
                        film_titles[film] = film_req.json()["title"]
                    character_films.append(film_titles[film])

                # assumption: all characters have names and are in at least one film
                self.character_infos.append({
                    "extern_id": _id,
                    "name": character_info["name"],
                    "films": character_films,
                })

            if len(self.character_infos) == self.CHARACTER_COUNT:
                querying = False

    def character_already_queried(self, _id):
        # this is unoptimized, but the logic is more clear than other methods
        for character in self.character_infos:
            if _id == character["extern_id"]:
                return True
        return False

    def mysql_insert_films(self, character):
        cursor = self.db.cursor()
        for film in character["films"]:
            sql = "INSERT INTO films (charid, title) VALUES (%s, %s);"
            values = (
                character["extern_id"],
                film,
            )
            cursor.execute(sql, values)
            self.db.commit()

    def mysql_insert_character(self, character):
        cursor = self.db.cursor()
        sql = "INSERT INTO characters (charid, name) VALUES (%s, %s);"
        values = (
            character["extern_id"],
            character["name"],
        )
        cursor.execute(sql, values)
        self.db.commit()

    def query_films_join_characters(self):
        cursor = self.db.cursor()
        sql = ("SELECT films.title AS title, characters.name as name "
               "FROM films JOIN characters "
               "ON characters.charid = films.charid;")
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows


def task_one(ctx):
    db_task = DbTask()
    db_task.init_db()
    # This is sort of cheating? But saves time working with the database
    db_task.reset_tables()
    db_task.retrieve_characters()

    # We could easily transform the data here to get the film_title to
    # character mapping. However, I feel as though I'm supposed to use the
    # slighlty more interesting case of doing an SQL query
    for character in db_task.character_infos:
        db_task.mysql_insert_character(character)
        db_task.mysql_insert_films(character)

    data = {
        "len_character_infos": len(db_task.character_infos),
        "character_infos": db_task.character_infos,
    }

    rows = db_task.query_films_join_characters(ctx)
    characters_in_films = determine_chars_by_film(rows)
    click.echo(json.dumps(characters_in_films, indent=4, sort_keys=True))

    return data


def determine_chars_by_film(rows):
    # This might be better-handled by extending MutableMapping
    # TODO: I noticed a character name printed in unicode. I found it was
    # /people/61 (Corde, e with a mark). Is this an error in my code, or does
    # my terminal struggle with unicode?

    film_list = []
    for row in rows:
        title = row[0]
        character = row[1]

        film_idx = find_film_idx(film_list, title)
        if film_idx > -1:
            film = film_list[film_idx]
            film["character"].append(character)
        else:
            new_film = {
                "film": title,
                "character": [character],
            }
            film_list.append(new_film)
    return film_list


def find_film_idx(film_list, title):
    for idx, film in enumerate(film_list):
        if title == film["film"]:
            return idx
    return -1


if __name__ == "__main__":
    ctx = {
        "api_base_url": "https://swapi.co/api/",
    }
    res = task_one(ctx)
    # click.echo(json.dumps(res["character_infos"], indent=4, sort_keys=True))
