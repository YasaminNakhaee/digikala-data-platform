import pandas as pd
from src.db.database import engine

def run_import_pipeline():
    file_path = "data/digikala-comments.csv"
    chunk_size = 10000

    print("start")

    try:
        for chunk in pd.read_csv(file_path, chunksize=chunk_size):
            print(f"processing chunk with {len(chunk)} rows")

            chunk.to_sql("comments", engine , if_exists = "append", index = False)

            print("chunk inserted successfully")

            break

    except Exception as e:

        print(f"error: {e}")

if __name__ == "__main__" : 
    run_import_pipeline()