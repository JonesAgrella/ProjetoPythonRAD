import sqlite3

DB_PATH = "pesquisa_estacio.db"

def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS respostas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL,
            email TEXT NOT NULL,
            curso TEXT NOT NULL,
            turno TEXT NOT NULL,
            presenca TEXT NOT NULL,
            sat_geral INTEGER NOT NULL,
            sat_clareza INTEGER NOT NULL,
            sat_infra INTEGER NOT NULL,
            sat_material INTEGER NOT NULL,
            sat_suporte INTEGER NOT NULL,
            avisos INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    con.commit()
    con.close()

def insert_resposta(d):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        INSERT INTO respostas
        (nome, idade, email, curso, turno, presenca,
         sat_geral, sat_clareza, sat_infra, sat_material, sat_suporte, avisos)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        d["nome"], d["idade"], d["email"], d["curso"], d["turno"], d["presenca"],
        d["sat_geral"], d["sat_clareza"], d["sat_infra"], d["sat_material"], d["sat_suporte"],
        1 if d["avisos"] else 0
    ))
    con.commit()
    con.close()

def fetch_all():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT * FROM respostas ORDER BY id ASC")
    rows = cur.fetchall()
    con.close()
    return rows

def count_rows():       #num resgistro
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM respostas")
    n = cur.fetchone()[0]
    con.close()
    return n