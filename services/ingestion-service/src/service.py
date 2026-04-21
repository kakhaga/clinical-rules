import os
import time
import argparse
import logging
import signal
import sys
from dotenv import load_dotenv  # Ensure dotenv is loaded
from migrate import run_migrations
from loader import load_csvs_to_raw
from run_etl import run_ingestion_etl

# Initialize environment variables
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Graceful shutdown handler
def handle_exit(sig, frame):
    logging.info("🛑 Shutdown signal received. Closing service...")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

def start_service(monitor_path):
    # Fetch interval from .env, cast to int, default to 60 if not found
    poll_interval = int(os.getenv("POLL_INTERVAL", 60))
    
    logging.info(f"🚀 Service Started.")
    logging.info(f"📂 Monitoring: {monitor_path}")
    logging.info(f"⏱️  Interval: {poll_interval} seconds")
    
    try:
        run_migrations()
    except e:
        logging.error(f"Failed to run initial migrations: {e}")
        return

    while True:
        logging.info("✅ Cycle started.")
        if not os.path.exists(monitor_path):
            logging.error(f"Directory {monitor_path} not found!")
        else:
            required_files = ["patients.csv", "diagnoses.csv", "labs.csv", "encounters.csv"]
            found_files = [f for f in required_files if f in os.listdir(monitor_path)]
            
            if found_files:
                logging.info(f"📦 Processing: {found_files}")
                try:
                    load_csvs_to_raw(csv_directory=monitor_path)
                    run_ingestion_etl()
                    logging.info("✅ Cycle complete.")
                except Exception as e:
                    logging.error(f"❌ Cycle failed: {e}")
            else:
                logging.info("😴 No files found.")

        # Use the variable from .env here
        time.sleep(poll_interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clinical Data Ingestion Service")
    parser.add_argument("path", type=str, help="Folder path to monitor")
    args = parser.parse_args()
    
    try:
        start_service(args.path)
    except KeyboardInterrupt:
        logging.info("🛑 Service stopped.")