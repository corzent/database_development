import pandas as pd
import psycopg2

conn = psycopg2.connect(
    dbname="terms_db",
    user="postgres",
    password="kod1601370",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

df = pd.read_excel("my_terms.xlsx")

for _, row in df.iterrows():
    cursor.execute("INSERT INTO terms (term, definition) VALUES (%s, %s)", (row[0], row[1]))

conn.commit()
cursor.close()
conn.close()
print("Terms loaded successfully!")