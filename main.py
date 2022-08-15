import psycopg2
def create_tables(cursor, ):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            id SERIAL PRIMARY KEY,
                name VARCHAR(40),
                surname VARCHAR(40),
                email VARCHAR (60) UNIQUE
                );
                """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS phones(
        id SERIAL PRIMARY KEY,
        phone VARCHAR,
        client_id INTEGER NOT NULL REFERENCES clients(id)
        );
        """)
    return conn.commit()

def get_client_id(cursor, name: str, surmane: str, email: str) -> int:
    cursor.execute("""
        SELECT id FROM clients WHERE name=%s and surname=%s and email=%s;
        """, (name, surmane, email))
    return cur.fetchone()

def add_client_info (cursor, name, surname, email):
    if get_client_id(cursor, name, surname, email) is None:
        cursor.execute("""
            INSERT INTO clients(name, surname, email) 
            VALUES(%s, %s, %s);""", (name, surname, email))
        conn.commit()
        print(f'данные по клиенту добавлены id клиента = {get_client_id(cursor, name, surname, email)[0]}')
    else:
        print(f'Такой клиент уже есть в базе с id = {get_client_id(cursor, name, surname, email)[0]}')


def add_phone_number(cursor, name, surname, email, phone):
    cursor.execute("""
        INSERT INTO phones(phone, client_id)
        VALUES(%s, %s);""", (phone, get_client_id(cursor, name, surname, email)))
    conn.commit()


def update_client_data(cursor, client_id, name=None, surname=None, email=None, phones=None):
    if name is not None:
        cursor.execute("""
    UPDATE clients SET name=%s 
    WHERE id=%s;""", (name, client_id))
    if surname is not None:
        cursor.execute("""
            UPDATE clients SET surname=%s 
            WHERE id=%s;""", (surname, client_id))
    if email is not None:
        cursor.execute("""
            UPDATE clients SET email=%s 
            WHERE id=%s;""", (email, client_id))
    if phones is not None:
        cursor.execute("""
            SELECT phone from phones
            WHERE client_id = %s;""", (client_id))
        if phones not in cursor.fetchall()[0]:
            cursor.execute("""
                    UPDATE phones SET phone=%s 
                    WHERE client_id=%s;""", (phones, client_id))
        else:
            print('данный телефон уже есть в базе у этого клиента')
    conn.commit()


def del_phone(cursor, client_id, phone):
    cursor.execute("""
    SELECT phone from phones
    WHERE client_id = %s;""", (client_id))
    if len(cursor.fetchall()) > 0 and phone in cursor.fetchall()[0]:
        cursor.execute("""
        DELETE FROM phones WHERE phone = %s;""", (phone,))
        conn.commit()
        return 'телефон удален'
    else:
        return 'телефон не найден'

def del_client(cursor, client_id):
    cursor.execute("""
        SELECT phone from phones
        WHERE client_id = %s;""", (client_id))
    if len(cursor.fetchall()) > 0:
        cursor.execute("""
        DELETE FROM phones WHERE client_id = %s;""",
                       (client_id,))
    cursor.execute("""
        SELECT id from clients
        WHERE id = %s;""", (client_id))
    if int(client_id) == cursor.fetchall()[0][0]:
        cursor.execute("""
        DELETE FROM clients
        WHERE id=%s;""",(client_id,))
        conn.commit()
        return 'клиент удален'
    else:
        return 'клиент не существует'


def find_client(cursor, name=None, surname=None, email=None, phone=None):
    if name is not None and surname is not None and email is not None:
        cursor.execute("""
            SELECT c.id, c.name, c.surname, p.phone from clients c
            JOIN phones p on c.id = p.client_id
            WHERE name=%s and surname=%s and email=%s;""", (name, surname, email))
    elif phone is not None:
        cursor.execute("""
        SELECT c.id, c.name, c.surname, p.phone from clients c
            JOIN phones p on c.id = p.client_id
            WHERE p.phone=%s;""",(phone,))
    return cursor.fetchall()


conn = psycopg2.connect(database = "netology_sql", user="postgres", password="Pass50word!")

with conn.cursor() as cur:
    # create_tables(cur)
    # add_client_info(cur, 'Ivan', 'Sidorov', 'iva2n@sid.ru')
    # add_phone_number(cur, 'Ivan', 'Sidorov', 'iva2n@sid.ru','9855543322')
    # print(get_client_id(cur, 'Ivan', 'Sidorov', 'ivan@sid.ru'))
    # update_client_data(cur, '6', phones='978854756876')
    # print(del_phone(cur, client_id='4', phone='78854756876'))
    # print(del_client(cur,'6'))
    #print(find_client(cur,'Ivan', 'Sidorov', 'iva2n@sid.ru'))
    print(find_client(cur, phone='9855543322'))



conn.close()