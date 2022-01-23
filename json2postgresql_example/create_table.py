#!/usr/bin/python
import psycopg2
from .config import get_config


def create_tables():
    commands = (
        ('CREATE TABLE interface ('
            'id SERIAL PRIMARY KEY,'
            'connection INTEGER,'
            'name VARCHAR(255) NOT NULL,'
            'description VARCHAR(255),'
            'config json,'
            'type VARCHAR(50),'
            'infra_type VARCHAR(50),'
            'port_channel_id INTEGER,'
            'max_frame_size INTEGER)'),
        )
    conn = None
    try:
        params = get_config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        for command in commands:
            cur.execute(command)

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def main():
    create_tables()

if __name__ == '__main__':
    main()
