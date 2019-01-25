import json

import click
import requests


class FilmTask:
    API = "https://swapi.co/api/"
    ADDITIONAL_FIELDS = [
        "characters",
        "planets",
        "starships",
        "vehicles",
        "species",
    ]

    def __init__(self):
        # I like to use explicit statements instead of inferring None-types
        self.film = "film_not_set"
        self.film_etl = "film_etl_not_set"

    def query_film(self):
        guess = 1
        querying = True
        while querying:
            film_req = requests.get(self.API + "films/" + str(guess))
            film = film_req.json()
            if film["title"] == "A New Hope":
                querying = False
            else:
                guess += 1
        self.film = film

        # This could possible be done more succinctly, but, in the python way,
        # I like to avoid implicitness
        self.film_etl = {
            "title": film["title"],
            "episode_id": film["episode_id"],
            "opening_crawl": film["opening_crawl"],
            "director": film["director"],
            "producer": film["producer"],
            "release_date": film["release_date"],
            "created": film["created"],
            "edited": film["edited"],
            "url": film["url"],
            "characters": [],
            "planets": [],
            "starships": [],
            "vehicles": [],
            "species": [],
        }

    def process_fields(self):
        for field in self.ADDITIONAL_FIELDS:
            for item in self.film[field]:
                data = requests.get(item).json()
                if field == "characters":
                    # convert cm to in
                    height = data["height"].replace(",", "")
                    data["height"] = float(height) * 0.393701

                    mass = data["mass"].replace(",", "")
                    # convert kg to lbs
                    if data["mass"] != "unknown":
                        data["mass"] = float(mass) * 2.20462

                # import pdb; pdb.set_trace()
                self.film_etl[field].append(data)
            click.echo("Done processing " + field)

    def remove_cross_references(self):
        for grouping in self.ADDITIONAL_FIELDS:
            for item in self.film_etl[grouping]:
                keys_to_remove = []
                for key, field in item.items():
                    if self.field_is_only_references(key, field):
                        # import pdb; pdb.set_trace()
                        click.echo(field)
                        keys_to_remove.append(key)

                # import pdb; pdb.set_trace()
                for key in keys_to_remove:
                    del item[key]
                    # del self.film_etl[grouping][key]

                click.echo("keys removed: " + str(keys_to_remove))

    def field_is_only_references(self, key, field):
        # TODO: The url field is for the queries self-reference, so I
        # assume we want to keep it. (ask management)
        if key == "url":
            return False

        # TODO: Ask management if we want to keep fields which are empty lists
        # which might only be references but might not be. Is hardcoding
        # elements okay?
        if isinstance(field, list):
            if len(field) > 0 and "https://swapi" in field[0]:
                return True

        if isinstance(field, str):
            if "https://swapi" in field:
                return True

        return False

    def write_etl(self):
        # import pdb; pdb.set_trace()
        with open("task_two.json", "w") as f:
            json.dump(self.film_etl, f)


def task_two(ctx):
    film_task = FilmTask()
    film_task.query_film()
    film_task.process_fields()
    film_task.remove_cross_references()
    film_task.write_etl()


if __name__ == "__main__":
    ctx = {
        "api_base_url": "https://swapi.co/api/",
    }
    res = task_two(ctx)
