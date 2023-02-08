from apify_client import ApifyClient
import json

apify_client = ApifyClient('apify_api_XXXXXXXXXXXXX....')
# Find your Apify Client Key here:
# https://console.apify.com/account/integrations

body = {
    "collectionURL": "https://opensea.io/collection/clonex",
    "scrapeEventCount": 2,
    "scrapeEventTypeAuctionCreated": False,
    "scrapeEventTypeAuctionSuccess": False,
    "scrapeEventTypeCollectionOffer": False,
    "scrapeEventTypeOffer": False,
    "scrapeEventTypeTransfer": False,
    "selectedCursor": ""
}
# Start an actor and wait for it to finish
actor_call = apify_client.actor('argusapi/opensea-collection-activity-scraper').call(
    run_input=json.dumps(body, indent=4),
    content_type="application/json"
)

store_id = actor_call["defaultDatasetId"]

# Fetch results from the actor's default dataset
dataset_items = apify_client.dataset(store_id).list_items().items[0]["events"]
print(dataset_items)
