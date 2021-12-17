import sqlite3
from tabulate import tabulate

conn = sqlite3.connect("msgstore.db")
cur = conn.cursor()

attachWaDatabase = "ATTACH DATABASE ? AS wa"
waDB  = ("wa.db",)
cur.execute(attachWaDatabase, waDB)

conversations = []

def get_conversations():
    global conversations

    query = '''SELECT chat._id, chat.jid_row_id, w.jid, w.number, w.display_name, last_message_row_id, display_message_row_id, last_message_row_id, m.data, m.received_timestamp FROM chat LEFT JOIN wa.wa_contacts AS w ON chat._id = w._id LEFT JOIN messages AS m ON m._id = last_message_row_id'''
    result = cur.execute(query)
    results = result.fetchall()
    conversations = [row[2] for row in results]
    formatted_result = "\n" + tabulate(results, headers=[field[0] for field in result.description], tablefmt='orgtbl')
    formatted_result += "\n\nNumero totale di conversazioni: " + str(len(results))
    return formatted_result

def get_contacts():
    query = '''SELECT _id, jid, status, status_timestamp, number, display_name, unseen_msg_count, given_name, family_name FROM wa.wa_contacts'''
    result = cur.execute(query)
    formatted_result = "\n" + tabulate(result.fetchall(), headers=[field[0] for field in result.description], tablefmt='orgtbl')
    return formatted_result

def get_messages():

    if conversations == []:
        response = get_conversations()
        print(response)

    c = int(input("\nInserisci l'ID della conversazione: "))

    if c > len(conversations):
        return "ID della conversazione invalido"

    query = '''SELECT _id, key_remote_jid, key_from_me, data, timestamp, media_mime_type, media_size, media_name, media_caption FROM messages WHERE key_remote_jid=:conversation ORDER BY timestamp'''
    result = cur.execute(query, {"conversation": conversations[c - 1]})
    formatted_result = "\n" + tabulate(result.fetchall(), headers=[field[0] for field in result.description], tablefmt='orgtbl')
    return formatted_result

while True:
    print("\n1 - Visualizza le conversazioni")
    print("2 - Visualizza i contatti whatsapp")
    print("3 - Visualizza i messaggi relativi a una conversazione")
    print("0 - Esci")

    c = input("\nScegli: ")

    if c == "0": break
    elif c == "1":
        response = get_conversations()
    elif c == "2":
        response = get_contacts()
    elif c == "3":
        response = get_messages()
    else:
        print("\nValore inatteso.... riprova")
        continue

    print(response)


detachWaDatabase = "DETACH DATABASE wa"
cur.execute(detachWaDatabase)
conn.close()
