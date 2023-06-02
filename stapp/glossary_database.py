import mysql.connector

def get_database():
    # Replace placeholder values with your actual database information
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="a123456789",
        database="mydb"
    )
    return connection

def add_entry(korean_word, english_word):
    db = get_database()
    cursor = db.cursor()
    query = "INSERT INTO glossary (korean, english) VALUES (%s, %s)"
    values = (korean_word, english_word)
    cursor.execute(query, values)
    db.commit()

def remove_entry(korean_word):
    db = get_database()
    cursor = db.cursor()
    query = "DELETE FROM glossary WHERE korean = %s"
    values = (korean_word,)
    cursor.execute(query, values)
    db.commit()

def get_glossary():
    db = get_database()
    cursor = db.cursor()
    query = "SELECT * FROM glossary"
    cursor.execute(query)
    results = cursor.fetchall()
    glossary = {korean: english for (korean, english) in results}
    return glossary