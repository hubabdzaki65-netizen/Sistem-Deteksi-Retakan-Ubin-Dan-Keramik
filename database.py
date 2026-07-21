import sqlite3
from datetime import datetime


DATABASE_NAME = "inspection.db"


# ======================================
# Membuat Database
# ======================================

def create_database():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS inspections (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            filename TEXT,

            status TEXT,

            percentage REAL,

            inspection_date TEXT

        )

    """)

    conn.commit()

    conn.close()


# ======================================
# Menyimpan Hasil
# ======================================

def save_result(filename, status, percentage):

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO inspections

        (filename,status,percentage,inspection_date)

        VALUES (?,?,?,?)

    """,

    (

        filename,

        status,

        percentage,

        datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    )

    )

    conn.commit()

    conn.close()


# ======================================
# Menampilkan Semua Data
# ======================================

def get_all_data():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM inspections

        ORDER BY id DESC

    """)

    data = cursor.fetchall()

    conn.close()

    return data


# ======================================
# Menghapus Riwayat
# ======================================

def delete_all_data():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""

        DELETE FROM inspections

    """)

    conn.commit()

    conn.close()


# ======================================
# Menghapus Data Berdasarkan ID
# ======================================

def delete_data(id_data):

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""

        DELETE FROM inspections

        WHERE id=?

    """,

    (id_data,)

    )

    conn.commit()

    conn.close()


# ======================================
# Statistik
# ======================================

def get_statistics():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM inspections

    """)

    total = cursor.fetchone()[0]

    cursor.execute("""

        SELECT COUNT(*)

        FROM inspections

        WHERE status='NORMAL'

    """)

    normal = cursor.fetchone()[0]

    cursor.execute("""

        SELECT COUNT(*)

        FROM inspections

        WHERE status LIKE 'RETAK%'

    """)

    crack = cursor.fetchone()[0]

    conn.close()

    return total, normal, crack

