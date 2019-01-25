# SWAPI

To install in editable mode for testing:
- mkvirtualenv swapi
- pip install -r requirements.txt
- pip install -e .

Scripts to get up and running are in the scripts folder
- package.sh: Packages myswapi and uploads it to the pypi tests repo, where it can be installed from

Scripts to run the database:
- build-mysql.sh: Uses the dockerfile and sql file to create the mysql database in a docker container. Will generate the container and start it.
- stop-mysql.sh: Stops the mysql docker container
- start-mysql.sh: Starts the mysql docker container


# Notes
- pytest on ubuntu 16 was segfaulting for me. Not sure if this is reproducable. pytest works on macos
- I thought the Click interface would be helpful to structuring this assessment. I quickly realized that the requirement of executing the file directly deprecated that assumption. The cli is deprecated and may not function as intended
- If the cli works, it should be executable with the command `swa`
