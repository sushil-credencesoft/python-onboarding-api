def get_business_subtype(property_name: str) -> str:
    """
    Determines the business subtype based on property name.
    If no conditions match, defaults to 'Hotels'.
    """

    if not property_name:
        return "Hotels"

    name = property_name.lower()

    if "resort" in name:
        return "Resorts"
    elif "homestay" in name or "home stay" in name or "homes" in name:
        return "Homestays"
    elif "farm house" in name:
        return "Farmstays"
    elif "apartment" in name or "residency" in name:
        return "Apartments"
    elif "lodge" in name:
        return "Lodges"
    elif "guest house" in name:
        return "Guest Houses"
    elif "villa" in name:
        return "Villas"
    elif "b&b" in name or "bed & breakfast" in name:
        return "Bed & Breakfasts"
    else:
        return "Hotels"


import logging
import uuid
from datetime import datetime

logger = logging.getLogger("transaction_logger")


class TransactionLogger:
    @staticmethod
    def start(endpoint: str, payload: dict) -> str:
        transaction_id = str(uuid.uuid4())
        start_time = datetime.now().isoformat()
        logger.info(
            f"Start ** TransactionID ** {transaction_id} API ** Endpoint ** {endpoint} ** at ** {start_time} ** received {payload}"
        )
        return transaction_id

    @staticmethod
    def finish(transaction_id: str, endpoint: str, payload: dict = None):
        finish_time = datetime.now().isoformat()
        logger.info(
            f"Finish ** TransactionID ** {transaction_id} API ** Endpoint ** {endpoint} ** at ** {finish_time} ** payload {payload}"
        )
