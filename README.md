# Opensea Collection Activity / Events Scraper
### By ArgusAPI
#### To use this API / Scraper you can check it out on Apify for free here (https://apify.com/argusapi/opensea-collection-activity-scraper)
For further support we recommend joining our community discord, from support from Argus or the community. [Join our discord](https://discord.gg/m5psNeqkaQ)

### Examples 
- Use preset / prefill values in the Apify Actor
- For a programmatic example view `example.py` for a python example


# Tutorial / Guide
Below is the tutorial / guide, video tutorial will be coming soon. If you have further questions or need assistance join our discord above.

### Content:
1. Input Parameters
2. Output values 
3. Error responses

## 1. Input Parameters
Below is an image on how the input parameters will look from an Apify Actor input perspective
![actor_preview](https://i.imgur.com/bDZAxZf.png)
#### Input: Collection URL
This is the collection URL to an Opensea collection, it is important that you use a valid collection URL. Here are some examples:
- [https://opensea.io/collection/opepen-edition](https://opensea.io/collection/opepen-edition)
- [https://opensea.io/collection/vv-checks](https://opensea.io/collection/vv-checks)
- [https://opensea.io/collection/cryptopunks](https://opensea.io/collection/cryptopunks)
#### Input: Proxy configuration
This is optional, we only recommend using this option if you are planning on running concurrent tasks or if you getting ratelimited by Opensea (Which should not happen). Otherwise we also recommend not using proxies, since they are usually slower, and cause errors occasionally. 
##### If you are going to use proxies you can read more here, on how to use them:
[https://docs.apify.com/proxy](https://docs.apify.com/proxy)

#### Input: Scrape Event Types
There are 5 (6) event types on Opensea.
- Sale events (When an NFT gets sold)
- Listing events (When an NFT is listed on market)
- Transfer events (When an NFT is transfered between users)
- Collection Offer events (When a user/address makes an offer, collection wide)
- Trait Offer events (When a user/address makes an offer on a certain trait, collection wide - **A part of collection offer events, in the input parameters**)
- Offer events (When a user/address makes an offer on a specific listing)
When set to `True` or (ticked blue on the Apify Actor input page), the scraper will scrape events with selected event type. If you select none (`False`), the scraper will scrape all event types chronologically, as well if you tick them all.

#### Input: Cursor
This is the cursor for pagination of events. If you wish not to paginate through requests and only wish the newest `X` of events from a collection you can ignore this parameter and not set any value to it. If the scraper detects a faulty value, it will assume the cursor as `None` meaning it will not attempt to paginate.

Lets say you wanted to scrape all events for a collection, which had 3000 events in total, but the scraper returns max 1000 events each session, then you can utilize the cursor to fetch all 3000 events in 3 different requests. If you want to read more about how it works, read this: https://jsonapi.org/profiles/ethanresnick/cursor-pagination/

Each request, will return a key in the response called `pageData`, where there are 2 keys, as such:
```json
{
    "events": [...],
    "error": "None",
    "pageData": {
        "lastCursor": "YXJyYXljb25uZWN0aW9u...",
        "hasNextPage": true
    }
}
```
The `lastCursor` key is cursor for the next "page", so on requst 1, you are on page 1 - the on request 2 you can use the `lastCursor` from request 1, and then you are on page 2.

If `hasNextPage` is `false` there will still be a cursor but the next request will not have any events since you have scraped all the events. So there is not point continuing with pagination / the cursor if `hasNextPage` has the value `false`


Cursors on Opensea start with `YXJyYXljb25uZWN0aW9u`, for example a valid cursor can look like this: `YXJyYXljb25uZWN0aW9uOmV2ZW50X3RpbWVzdGFtcD1sdDoyMDIzLTAyLTA4IDA5OjUyOjExJmV2ZW50X3R5cGU9bHQ6c3VjY2Vzc2Z1bCZwaz1sdDo5ODM3NDE2NzAx`

#### Input: Event Scrape Count
This is the ammount of events to scrape each session, you have to scrape atleast 1 event and can scrape up to a 1000 events.

## 2. Output Values

### Introduction / General Notes
The response is structured below, it is pretty easy to understand - but one can never be certain so the here you can find the documentation for the response.
```
{
    "events": [...],
    "error": "None",
    "pageData": {
        "lastCursor": "YXJyYXljb25uZWN0aW9u...",
        "hasNextPage": true
    }
}
```
The `events` key is a list over events scraped. If there is some sort of error this list will be empty.

The `error` key is a string, with details if an error is present. If there is no error, the value will be `"None"`.

The `pageData` key is a object with cursor / pagination related data. Refer to Input Parameters part of the tutorial which goes over cursor, for more details. (Section 1. - Input: Cursor)


### Types of events
We will go through all different event responses and show what possible values and keys mean.

All responses are standardized with 2 keys: `eventType` & `eventTimestamp`

`eventType` - The type of Opensea event
This is what you want to use to differentiate between response types. Possible response types include:
- Sale events - `sale` (When an NFT gets sold)
- Listing events - `listing` (When an NFT is listed on market)
- Transfer events - `transfer` (When an NFT is transfered between users)
- Collection Offer events - `collection_offer` (When a user/address makes an offer, collection wide)
- Trait Offer events - `trait_offer` (When a user/address makes an offer on a certain trait, collection wide - A part of collection offer events, in the input parameters)
- Offer events - `offer` (When a user/address makes an offer on a specific listing)


`eventTimestamp` - When this event took place (everything is organized chronologically)

Below comments to the response data are made with `//` for example `{"foo": bar // baz}`

#### 1. Event Type: Sale
```
  {
    "eventType": "sale", // Type of event
    "eventTimestamp": "2023-02-08T03:30:23", // Timestamp of event
    "saleEventData": { // This object is only on **SALE** events
      "fromAccount": { // Object over user who made the sold the nft (seller)
        "address": "0x42c3c3bf1ab8edffeb7990f3f1645d34299451a5", // ERC20 address
        "username": "BHCVault", // Opensea Username
        "id": "VXNlclR5cGU6MTEzNzQyMg==", // Opensea ID
        "isCompromised": false // Wheather the address / wallet has been hacked / compromised
      },
      "toAccount": { // Object over user who made the sold the nft (buyer)
        "address": "0xa9fca334c431a00c13360adc1b4be9fbd7c7bf1a", / ERC20 address
        "username": null, // Opensea Username
        "id": "QWNjb3VudFR5cGU6MjQyNjU3Mzk3Nw==", // Opensea ID
        "isCompromised": false // Wheather the address / wallet has been hacked / compromised
      },
      "payment": { // Object with data regarding the payment / bid / sale
        "priceFormatted": "71.9 ETH", // formatted price, including unit and currency symbol
        "price": "71.9", // Payment in relative units
        "symbol": "ETH", // Payment symbol
        "ethValue": "71.9", // Value of the payment in ETH (useful if payment was done in SOL or another currency)
        "usdValue": "118463.8779999999921629", // Value of the payment in USD
        "quantity": "1" // How many of assets the offer is looking to purchase
        // Note that all prices are price PER asset, and not total price, so note the quantity field, if its for example 2, you should times price by quantity to find total price.

      },
      "item": { // Item data object
        "name": "8216", // Name of the NFT
        "tokenId": "8216", // Token ID of NFT
        "imageUrl": "https://i.seadn.io/gae/muo-lllyJy3aWJ-TGMeOtX-7MJ3WgVu_EMKsQGRxZ_FqSLp1kqXmIs2FBwBHscHNlDQX0lP-Fiegq9Ei6RH1JENlNs6qgxrLdOeaXA?w=500&auto=format", // Image of NFT
        "chain": "ETHEREUM" // NFT Chain
      }
    }
  }
```
#### 2. Event Type: Listing
```
  {
    "eventType": "listing", // Type of event
    "eventTimestamp": "2023-02-08T19:09:13.414161", // Timestamp of event
    "listingEventData": { // This object is only on **LISTING** events
      "fromAccount": {  // Object over user who made the listing (or made the event)
        "address": "0xc000a78a0573d1a31744bb2c58f35b91a47996d7", // ERC20 address
        "username": null, // Opensea username
        "id": "VXNlclR5cGU6NDA1MzE1NTE=", // Opensea ID
        "isCompromised": false // Wheather the address / wallet has been hacked / compromised
      },
      "payment": { // Object with data regarding the payment / bid / sale
        "priceFormatted": "0.86263 WETH", // formatted price, including unit and currency symbol
        "price": "0.8626321", // Payment in relative units
        "symbol": "WETH", // Payment symbol
        "ethValue": "0.8626321", // Value of the payment in ETH (useful if payment was done in SOL or another currency)
        "usdValue": "1444.6758568330000155273778", // Value of the payment in USD (useful if payment was done in SOL or another currency)
        "quantity": "1" // How many of assets the offer is looking to purchase
        // Note that all prices are price PER asset, and not total price, so note the quantity field, if its for example 2, you should times price by quantity to find total price.
      },
      "item": { // Item data object
        "name": "8216", // Name of the NFT
        "tokenId": "8216", // Token ID of NFT
        "imageUrl": "https://i.seadn.io/gae/muo-lllyJy3aWJ-TGMeOtX-7MJ3WgVu_EMKsQGRxZ_FqSLp1kqXmIs2FBwBHscHNlDQX0lP-Fiegq9Ei6RH1JENlNs6qgxrLdOeaXA?w=500&auto=format", // Image of NFT
        "chain": "ETHEREUM" // NFT Chain
      }
    }
  }
```
#### 3. Event Type: Transfer
```
  {
    "eventType": "transfer",
    "eventTimestamp": "2023-02-08T19:07:47",
    "transferEventData": {
      "fromAccount": { // Object over user who transffered the NFT
        "address": "0x42c3c3bf1ab8edffeb7990f3f1645d34299451a5", // ERC20 address
        "username": "BHCVault", // Opensea Username
        "id": "VXNlclR5cGU6MTEzNzQyMg==", // Opensea ID
        "isCompromised": false // Wheather the address / wallet has been hacked / compromised
      },
      "toAccount": { // Object over user who recieved the NFT
        "address": "0xa9fca334c431a00c13360adc1b4be9fbd7c7bf1a", / ERC20 address
        "username": null, // Opensea Username
        "id": "QWNjb3VudFR5cGU6MjQyNjU3Mzk3Nw==", // Opensea ID
        "isCompromised": false // Wheather the address / wallet has been hacked / compromised
      },
      "payment": {
        "quantity": "1"
      },
      "item": { // Item data object
        "name": "2808", // Name of NFT
        "tokenId": "2808", // Token ID of NFT
        "imageUrl": "https://i.seadn.io/gae/p1uVwpDrDBuTHwdKMRF1tPKFiksG2yS18EVUOZO-birNppPM1XIZ50T6KP-39kQCKtyxq-MmE-tp4ztXdY7QFsaOjksBm5Aq3590fA?w=500&auto=format", // Image of NFT
        "chain": "ETHEREUM" // NFT chain
      }
    }
  }
```

#### 4. Event Type: Collection Offer 
```
  {
    "eventType": "collection_offer", // Type of event
    "eventTimestamp": "2023-02-08T13:36:36.697053", // Timestamp of event
    "offerEventData": { // This object is only on **OFFER (and other offer)** events
      "fromAccount": { // Object over user who made the collection offer (or made the event)
        "address": "0x668b78ce9308c5859ed3c2958b0d71de9c2cc2a4", // ERC 20 address
        "username": "NFTinitcom_12345", // Opensea Username
        "id": "VXNlclR5cGU6Mjg0NjczMzA=", // Opensea ID
        "isCompromised": false // Wheather the address / wallet has been hacked / compromised
      },
      "payment": { // Object with data regarding the payment / bid / sale
        "priceFormatted": "0.86263 WETH", // formatted price, including unit and currency symbol
        "price": "0.8626321", // Payment in relative units
        "symbol": "WETH", // Payment symbol
        "ethValue": "0.8626321", // Value of the payment in ETH (useful if payment was done in SOL or another currency)
        "usdValue": "1444.6758568330000155273778", // Value of the payment in USD (useful if payment was done in SOL or another currency)
        "quantity": "1" // How many of assets the offer is looking to purchase
        // Note that all prices are price PER asset, and not total price, so note the quantity field, if its for example 2, you should times price by quantity to find total price.
      }
    }
  }
```

#### 5. Event Type: Trait Offer
```
  {
    "eventType": "trait_offer", // Type of event
    "eventTimestamp": "2023-02-08T20:13:13.435141", // Timestamp of event
    "offerEventData": {  // This object is only on **OFFER (and other offer)** events
      "fromAccount": { // Object over user who made the collection offer (or made the event)
        "address": "0x668b78ce9308c5859ed3c2958b0d71de9c2cc2a4", // ERC 20 address
        "username": "NFTinitcom_12345", // Opensea Username
        "id": "VXNlclR5cGU6Mjg0NjczMzA=", // Opensea ID
        "isCompromised": false // Wheather the address / wallet has been hacked / compromised
      },
      "payment": { // Object with data regarding the payment / bid / sale
        "priceFormatted": "0.86263 WETH", // formatted price, including unit and currency symbol
        "price": "0.8626321", // Payment in relative units
        "symbol": "WETH", // Payment symbol
        "ethValue": "0.8626321", // Value of the payment in ETH (useful if payment was done in SOL or another currency)
        "usdValue": "1444.6758568330000155273778", // Value of the payment in USD (useful if payment was done in SOL or another currency)
        "quantity": "1" // How many of assets the offer is looking to purchase
        // Note that all prices are price PER asset, and not total price, so note the quantity field, if its for example 2, you should times price by quantity to find total price.
      },
      "traitCriteria": { // Exists only on trait offer, data about trait offer (Uses metadata)
        "traitType": "Eyes", // Trait type
        "traitTypeValue": "Wide Eyed" // Trait value
      }
    }
```

#### 6. Event Type: Offer
```
  {
    "eventType": "offer", // Type of event
    "eventTimestamp": "2023-02-08T20:21:13.244292", // Timestamp of event
    "offerEventData": { // This object is only on **OFFER (and other offer)** events
      "fromAccount": { // Object over user who made the collection offer (or made the event)
        "address": "0x668b78ce9308c5859ed3c2958b0d71de9c2cc2a4", // ERC 20 address
        "username": "NFTinitcom_12345", // Opensea Username
        "id": "VXNlclR5cGU6Mjg0NjczMzA=", // Opensea ID
        "isCompromised": false // Wheather the address / wallet has been hacked / compromised
      },
      "payment": { // Object with data regarding the payment / bid / sale
        "priceFormatted": "0.86263 WETH", // formatted price, including unit and currency symbol
        "price": "0.8626321", // Payment in relative units
        "symbol": "WETH", // Payment symbol
        "ethValue": "0.8626321", // Value of the payment in ETH (useful if payment was done in SOL or another currency)
        "usdValue": "1444.6758568330000155273778", // Value of the payment in USD (useful if payment was done in SOL or another currency)
        "quantity": "1" // How many of assets the offer is looking to purchase
        // Note that all prices are price PER asset, and not total price, so note the quantity field, if its for example 2, you should times price by quantity to find total price.
      },
      "item": { // Item data object
        "name": "8216", // Name of the NFT
        "tokenId": "8216", // Token ID of NFT
        "imageUrl": "https://i.seadn.io/gae/muo-lllyJy3aWJ-TGMeOtX-7MJ3WgVu_EMKsQGRxZ_FqSLp1kqXmIs2FBwBHscHNlDQX0lP-Fiegq9Ei6RH1JENlNs6qgxrLdOeaXA?w=500&auto=format", // Image of NFT
        "chain": "ETHEREUM" // NFT Chain
      }
    }
  }
```
### Notes & Exceptions

#### Standardized Objects
The following keys are standardized, as you may have noticed after reading above:
- `payment`
- `fromAccount`
- `toAccount`
- `item`

#### Exceptions
In very occurrences NFT's will be sold for 0 in value which can mess up a response. Here is how the `payment` object will look if so.
```
{
    "priceFormatted": '0',
    "price": 0,
    "symbol": None,
    "ethValue": 0,
    "usdValue": 0,
    "quantity": {QUANTITY_OF_ASSET_SOLD}
}
```
## Errors 
You should never get error, since everything is safe proof, but we do have error handling. These are the errors we have handled.

1. Invalid collection URL - `"error": "Invalid opensea collection url"` | Appears when using a improper collection URL
2. Failed request - `"error": "Request failed to go through, check proxies"` | Appears when requests fail to go through, generally happens because of faulty proxies 
3. Invalid cursor - `"error": "Invalid cursor"` | Appears when using a valid cursor on the wrong collectiton.
4. Unknown Error - `"error": f'Unknown error: {ERROR...}, report to ArgusAPI'}` | Appears when an unknown response is detected from Opensea
5. Ratelimit - `"error": "Ratelimited, use proxies"` | Appears when ratelimited, should not happen, but it can happen
6. Signature Fail - `"error": "Signature fail, report to ArgusAPI"` | Should never happen, server side related error 
7. Malformed Response - `"error": "Unknown response, report to ArgusAPI"` | Should never happen, but it can happen 

**If you experience any of these errors, please do report them in our discord**
