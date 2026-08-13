import pandas as pd
import logging
from src.db.database import engine

logging.basicConfig(
    filename="logs/import_errors.log" , 
    level=logging.ERROR , 
    format="%(asctime)s - %(levelname)s - %(massage)s"
)

def run_import_pipeline():
    file_path = "data/digikala-comments.csv"
    chunk_size = 50000

    print("start")

    try:
        total_rows = 0

        for i, chunk in enumerate ( pd.read_csv(file_path, chunksize=chunk_size)): 

            try: 

                chunk = chunk.drop_duplicates()

                if "body" in chunk.columns:
                    chunk = chunk.dropna(subset={"body"})
                    chunk = chunk[chunk["body"].astype(str).str.len() >= 5]
                    chunk["rate"] = chunk["rate"].fillna(0)

                chunk.to_sql("comments", engine , if_exists = "append", index = False)
                total_rows += len(chunk)
                print(f"chunk {i+1} inserted . total_rows : {total_rows} ")

            except Exception as e:
            
                    logging.error(f"error in chunk {i+1} : {e}")
                    print("fatalerror check : logs/import_errors.log ")
            
        print(f"finish inserted : {total_rows}")
    except Exception as e:

        print("fatalerror check : logs/import_errors.log ")
        logging.critical(f"fatalerror durig inport : {e}")

if __name__ == "__main__" : 
    run_import_pipeline()