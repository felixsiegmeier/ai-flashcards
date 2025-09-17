import sqlite3

con = sqlite3.connect("flashcards.db")
cur = con.cursor()
cur.execute("CREATE TABLE flashcards(_id, question, answer, difficulty, lastvisit)")

def main():
    print("Hello from ai-flashcard!")

# Base.metadata.create_all(engine)
## wird später benutzt, um die Modelle in die DB zu schreiben 
## (diese dafür hier einmal importieren => können danach 
## wieder gelöscht werden; geht nur um die DB-Initiation)

if __name__ == "__main__":
    main()
