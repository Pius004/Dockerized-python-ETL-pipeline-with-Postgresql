# import pandas as pd
# import requests
# from db_connection import get_connection

# # --- Helper to clean text safely ---
# def clean_text(text):
#     if text is None:
#         return None
#     # Remove problematic unicode (like U+2028, U+2029) and ensure utf-8 safe
#     return (
#         str(text)
#         .encode("utf-8", "ignore")
#         .decode("utf-8")
#         .replace("\u2028", " ")
#         .replace("\u2029", " ")
#     )

# # Read raw JSON (already downloaded previously)
# raw_df = pd.read_json("raw_files/raw_data.json", lines=True)

# # Filter data
# secure_startups_df = (
#     raw_df.loc[
#         (raw_df['link'].str.contains("https")) & (raw_df['city'] == "New York")
#     ]
#     .sort_values("name")
#     .reset_index(drop=True)
# )

# # --- Database work ---
# conn = get_connection()   # <--- this was missing!
# cur = conn.cursor()

# cur.execute("""
#     CREATE TABLE IF NOT EXISTS SECURE_STARTUPS (
#     id bigserial PRIMARY KEY,
#     name varchar(400),
#     images varchar(400),
#     alt varchar(1000),
#     description varchar(4000),
#     link varchar(400) UNIQUE,
#     city varchar(100)
#     );

# """)

# for row in secure_startups_df.itertuples():
#    cur.execute("""
#     INSERT INTO SECURE_STARTUPS (name, images, alt, description, link, city)
#     VALUES (%s,%s,%s,%s,%s,%s)
#     ON CONFLICT (link) DO NOTHING
# """, (clean_text(row.name), clean_text(row.images), clean_text(row.alt),
#       clean_text(row.description), clean_text(row.link), clean_text(row.city)))

# conn.commit()
# cur.close()
# conn.close()





import pandas as pd
import requests
from db_connection import get_connection


# Read raw JSON (already downloaded previously)
# raw_df = pd.read_json("raw_files/raw_data.json", lines=True)

# --- Helper to clean text safely ---
def clean_text(text):
    if text is None:
        return None
    # Remove problematic unicode (like U+2028, U+2029) and ensure utf-8 safe
    return (
        str(text)
        .encode("utf-8", "ignore")
        .decode("utf-8")
        .replace("\u2028", " ")
        .replace("\u2029", " ")
    )

# --- Load raw JSON into DataFrame ---
raw_df = pd.read_json("raw_files/raw_data.json", lines=True)

# Filter secure startups in New York
secure_startups_df = (
    raw_df.loc[
        (raw_df["link"].str.contains("https")) & (raw_df["city"] == "New York")
    ]
    .sort_values("name")
    .reset_index(drop=True)
)

# --- Database work ---
conn = get_connection()
cur = conn.cursor()

# Create table if not exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS SECURE_STARTUPS (
        id bigserial PRIMARY KEY,
        name varchar(400),
        images varchar(400),
        alt varchar(1000),
        description varchar(4000),
        link varchar(400),
        city varchar(100)
    )
""")

# Insert rows safely with parameterized query
for row in secure_startups_df.itertuples(index=False):
    cur.execute("""
        INSERT INTO SECURE_STARTUPS (name, images, alt, description, link, city)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        clean_text(row.name),
        clean_text(row.images),
        clean_text(row.alt),
        clean_text(row.description),
        clean_text(row.link),
        clean_text(row.city),
    ))

conn.commit()
cur.close()
conn.close()

print("Data successfully inserted into SECURE_STARTUPS")

