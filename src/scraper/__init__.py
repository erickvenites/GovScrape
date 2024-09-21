from src.scraper.get_auction_items.get_bid_items import get_bid_items
from src.scraper.get_id_omaps.save_data import save_data
from src.scraper.get_ug_auctions.get_ug_auction import get_auction_ug




def run_scraping_auction_ug_and_items(engine):

    get_auction_ug(engine)
    get_bid_items(engine)


def run_scraping_id_ug(engine):
    save_data(engine)