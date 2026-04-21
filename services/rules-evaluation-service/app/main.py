import time
import logging
import signal
import sys
from app.core.config import settings
from app.db.session import SessionLocal
from app.services.evaluation_service import EvaluationService

# Setup logging to be informative but clean
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("evaluation-service")

# Graceful shutdown handler
def handle_exit(sig, frame):
    logger.info("🛑 Shutdown signal received. Closing service...")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

def run_service():
    """Main service loop"""
    logging.info(f"🚀 Evaluation Service Started.")
    logger.info(f"⏱️ Polling interval: {settings.POLL_INTERVAL} seconds.")
    
    # Initialize service once
    service = EvaluationService()

    while True:
        db = SessionLocal()
        start_time = time.time()
        
        try:
            logger.info("✅ Evaluation cycle started.")
            
            # 0. Re-read dim tables
            service.cache_dimension_lookups(db)

            # 1. Process Rules
            results = service.process_rules(db)
            
            # 2. Prepare Data (including ID lookups)
            eval_dicts = service.prepare_evaluations_for_db(results)
            
            # 3. Bulk Upsert (with internal de-duplication)
            if eval_dicts:
                service.bulk_upsert_evaluations(db, eval_dicts)
                logger.info(f"✅ Successfully processed {len(eval_dicts)} evaluations.")
            else:
                logger.info("☑️ No evaluations to process this cycle.")

        except Exception as e:
            logger.error(f"❌ Error during evaluation cycle: {str(e)}", exc_info=True)
            # We don't exit on error; we wait for the next interval to try again
            
        finally:
            db.close()
            
        # Calculate sleep time
        elapsed = time.time() - start_time
        sleep_time = max(0, settings.POLL_INTERVAL - elapsed)
        
        logger.info(f"✅ Cycle complete in {elapsed:.2f}s. 💤 Sleeping for {sleep_time:.2f}s...")
        time.sleep(sleep_time)

if __name__ == "__main__":
    run_service()