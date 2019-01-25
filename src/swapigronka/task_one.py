import json
import random

import click
import mysql.connector
import requests


# TODO: implement classes for a more stable interface to these functions and
# film/character data
def task_one(ctx):
    base = ctx["api_base_url"]
    num_chars = 88
    character_count = 15

    db = get_db(ctx)
    ctx["db"] = db

    # This is sort of cheating? But makes this process much easier
    reset_tables(ctx)

    film_titles = {}
    character_infos = []
    querying = True
    while querying:
        _id = random.randint(1, num_chars)
        if character_already_queried(_id, character_infos):
            continue

        character_req = requests.get(base + "people/" + str(_id))
        character_info = character_req.json()
        if "detail" in character_info and \
                character_info["detail"] == "Not found":
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
            character_infos.append({
                "extern_id": _id,
                "name": character_info["name"],
                "films": character_films,
            })

        if len(character_infos) == character_count:
            querying = False

    # We could easily transform the data here to get the film_title to
    # character mapping. However, I feel as though I'm supposed to use the
    # slighlty more interesting case of doing an SQL query
    for character in character_infos:
        mysql_insert_character(ctx, character)
        mysql_insert_films(ctx, character)

    data = {
        "len_character_infos": len(character_infos),
        "character_infos": character_infos,
    }

    rows = query_films_join_characters(ctx)
    characters_in_films = determine_chars_by_film(rows)
    click.echo(json.dumps(characters_in_films, indent=4, sort_keys=True))

    return data

def character_already_queried(_id, character_infos):
    # this is unoptimized, but the logic is more clear than other methods
    for character in character_infos:
        if _id == character["extern_id"]:
            return True
    return False


def reset_tables(ctx):
    db = ctx["db"]
    cursor = db.cursor()
    sql = "DELETE FROM characters;"
    cursor.execute(sql)
    db.commit()

    sql = "DELETE FROM films;"
    cursor.execute(sql)
    db.commit()


def mysql_insert_films(ctx, character):
    db = ctx["db"]
    cursor = db.cursor()
    for film in character["films"]:
        sql = "INSERT INTO films (charid, title) VALUES (%s, %s);"
        values = (
            character["extern_id"],
            film,
        )
        cursor.execute(sql, values)
        db.commit()


def mysql_insert_character(ctx, character):
    db = ctx["db"]
    cursor = db.cursor()
    sql = "INSERT INTO characters (charid, name) VALUES (%s, %s);"
    values = (
        character["extern_id"],
        character["name"],
    )
    cursor.execute(sql, values)
    db.commit()


def query_films_join_characters(ctx):
    db = ctx["db"]
    cursor = db.cursor()
    sql = ("SELECT films.title AS title, characters.name as name "
           "FROM films JOIN characters "
           "ON characters.charid = films.charid;")
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


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


def get_db(ctx):
    # this connection could be established in the click interface instead of
    # here, but that would break the assignment requirements
    mysql.connector.connect(
        host="127.0.0.1",
        user="swapiuser",
        passwd="asdf",
        database="swapi",
        auth_plugin="mysql_native_password",
    )
    return db


if __name__ == "__main__":
    ctx = {
        "api_base_url": "https://swapi.co/api/",
    }
    res = task_one(ctx)
    # click.echo(json.dumps(res["character_infos"], indent=4, sort_keys=True))
