import os
import requests
import pymysql.cursors
import json

def lambda_handler(event, context):

    if "MARIADB_HOST" in os.environ:
        mariadb_host = os.environ["MARIADB_HOST"]
    else:
        mariadb_host = "localhost"

    if "MARIADB_USER" in os.environ:
        mariadb_user = os.environ["MARIADB_USER"]
    else:
        mariadb_user = "testuser"

    if "MARIADB_PASSWORD" in os.environ:
        mariadb_password = os.environ["MARIADB_PASSWORD"]
    else:
        mariadb_password = "testpass"

    if "MARIADB_DB" in os.environ:
        mariadb_db = os.environ["MARIADB_DB"]
    else:
        mariadb_db = "findaprotest"

    schema = """\
    DROP TABLE event CASCADE;
    DROP TABLE category CASCADE;
    DROP TABLE movement CASCADE;
    DROP TABLE organization CASCADE;

    CREATE TABLE category (
        id INT UNSIGNED PRIMARY KEY,
        name TEXT
    );

    CREATE TABLE movement (
        id INT UNSIGNED PRIMARY KEY,
        name TEXT,
        date BIGINT,
        description TEXT,
        link TEXT
    );

    CREATE TABLE organization (
        id INT UNSIGNED PRIMARY KEY,
        name TEXT,
        description TEXT,
        link TEXT
    );

    CREATE TABLE event (
        id INT UNSIGNED PRIMARY KEY,
        movement_id INT UNSIGNED,
        category_id INT UNSIGNED,
        organization_id INT UNSIGNED,
        name TEXT,
        event_time BIGINT,
        created_time BIGINT,
        updated_time BIGINT,
        city TEXT,
        state TEXT,
        location TEXT,
        description TEXT,
        tags TEXT,
        link TEXT,
        estimated_size INT,
        actual_size INT,
        CONSTRAINT fk_category_id FOREIGN KEY (category_id) REFERENCES category (id),
        CONSTRAINT fk_movement_id FOREIGN KEY (movement_id) REFERENCES movement (id),
        CONSTRAINT fk_organization_id FOREIGN KEY (organization_id) REFERENCES organization (id)
    );
    """

    db = pymysql.connect(host=mariadb_host,
                          user=mariadb_user,
                          passwd=mariadb_password,
                          db=mariadb_db,
                          local_infile=1)

    cursor = db.cursor()

    print "Recreating tables..."
    cursor.execute(schema)


    categories = requests.get('https://api.meetup.com/find/topic_categories?&sign=true&photo-host=public').json()

    insert_category = "INSERT INTO `category` (`id`, `name`) VALUES (%s, %s)"
    for category in categories:
        cursor.execute(insert_category, (category['id'], category['name']))

    db.commit()
    cursor.close()
