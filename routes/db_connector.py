import sqlite3 as sq


def connect():
    return sq.connect("teachers_db.sqlite")


def create_table():
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS teachers_table
(
    teacher_name     text,
    class_name       text,
    teacher_vk_id    text,
    teacher_email    text,
    next_answer_time integer,
    reminder         integer
)""")
        conn.commit()
    finally:
        cur.close()
        conn.close()


def execute_select(query):
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(query)
        conn.commit()
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def execute_upd_ins(query):
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(query)
        conn.commit()
    finally:
        cur.close()
        conn.close()
