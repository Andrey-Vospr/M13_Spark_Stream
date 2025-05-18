# ─── CONFIGURATION ────────────────────────────────────────────────────────────
container_name    = "data"
local_root_folder = "/mnt/c/Users/HP/Documents/m13sparkstreaming"
delay_seconds     = 3  # seconds between days

# ─── CLIENT SETUP ──────────────────────────────────────────────────────────────
import os, time
from azure.storage.blob import BlobServiceClient

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
if not connection_string:
    raise RuntimeError("AZURE_STORAGE_CONNECTION_STRING is not set")

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client    = blob_service_client.get_container_client(container_name)

# ─── UPLOAD LOOP ───────────────────────────────────────────────────────────────
for year in sorted(os.listdir(local_root_folder)):
    year_path = os.path.join(local_root_folder, year)
    if not os.path.isdir(year_path): continue

    for month in sorted(os.listdir(year_path)):
        month_path = os.path.join(year_path, month)
        if not os.path.isdir(month_path): continue

        for day in sorted(os.listdir(month_path)):
            day_path = os.path.join(month_path, day)
            if not os.path.isdir(day_path): continue

            print(f"Uploading data for: {day_path}")
            for fn in os.listdir(day_path):
                if not fn.endswith(".parquet"): continue
                lp = os.path.join(day_path, fn)
                rel = os.path.relpath(lp, local_root_folder)
                blob = rel.replace(os.sep, "/")
                print(f"  → {blob}")
                with open(lp, "rb") as f:
                    container_client.upload_blob(name=blob, data=f, overwrite=True)

            print(f"Finished {day_path}\n")
            time.sleep(delay_seconds)

print("All weather data successfully uploaded day by day!")
