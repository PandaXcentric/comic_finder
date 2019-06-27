import requests
import urllib
from ebay_api.constants import Constants


class FindItemsAdvanced(object):
    """
    For reference:
    https://developer.ebay.com/Devzone/finding/CallRef/findItemsAdvanced.html#Samples
    """
    operation_name = 'findItemsAdvanced'
    service_version = '1.9.0'
    app_name = Constants.ebay_app_name
    description_search = 'true'
    category_id = 63 #Collectibles:Comics
    default_entries_per_page = 2
    initial_page_number = 1

    generic_endpoint = f"http://svcs.ebay.com/services/search/FindingService/v1?" \
                       f"OPERATION-NAME={operation_name}&" \
                       f"SERVICE-VERSION={service_version}&" \
                       f"SECURITY-APPNAME={app_name}&" \
                       f"RESPONSE-DATA-FORMAT=JSON&" \
                       f"REST-PAYLOAD&" \
                       f"keywords={{query_string}}&" \
                       f"categoryId={category_id}&" \
                       f"descriptionSearch={description_search}&" \
                       f"paginationInput.entriesPerPage={{entries_per_page}}&" \
                       f"paginationInput.pageNumber={{{{page_number}}}}"

    def __init__(self, query_string, entries_per_page=None, page_number=None):
        self.original_query_string = str(query_string)
        self.url_encoded_query_string = urllib.parse.quote_plus(self.original_query_string)

        self.entries_per_page = self.default_entries_per_page
        if entries_per_page:
            self.entries_per_page = entries_per_page

        self.page_number = self.initial_page_number
        if page_number:
            self.page_number = page_number

        self.total_pages = None
        self.total_entries = None

        self.content = None
        self._content_page_number = None

        self._endpoint = self.generic_endpoint.format(
            query_string=self.url_encoded_query_string,
            entries_per_page=self.entries_per_page
        )

        self.load_content()

    def next_page(self):
        self.page_number += 1
        self.load_content()

    def previous_page(self):
        self.page_number -= 1
        self.load_content()

    def go_to_page(self, page_number):
        self.page_number=page_number
        self.load_content()

    def load_content(self):
        """
        Sample content:
            [
                {
                    'itemId': ['293111671424'],
                    'title': ['DCEASED #2 (OF 6) HORROR VARIANT COVER DC COMIC BOOK BATMAN WONDER WOMAN NEW 1'],
                    'globalId': ['EBAY-US'],
                    'primaryCategory': [{'categoryId': ['17076'], 'categoryName': ['Batman']}],
                    'galleryURL': ['http://thumbs1.ebaystatic.com/m/mEOqDyzdcjDyRIR2KQz8JKw/140.jpg'],
                    'viewItemURL': ['http://www.ebay.com/itm/DCEASED-2-OF-6-HORROR-VARIANT-COVER-DC-COMIC-BOOK-BATMAN-WONDER-WOMAN-NEW-1-/293111671424'],
                    'paymentMethod': ['PayPal'],
                    'autoPay': ['false'],
                    'location': ['USA'],
                    'country': ['US'],
                    'shippingInfo':
                        [
                            {
                                'shippingServiceCost':
                                    [
                                        {
                                          '@currencyId': 'USD',
                                           '__value__': '3.95'
                                        }
                                    ],
                                'shippingType': ['Flat'],
                                'shipToLocations': ['Worldwide'],
                                'expeditedShipping': ['true'],
                                'oneDayShippingAvailable': ['false'],
                                'handlingTime': ['1']
                            }
                        ],
                    'sellingStatus':
                        [
                            {
                                'currentPrice':
                                    [
                                        {
                                            '@currencyId': 'USD',
                                            '__value__': '3.95'
                                        }
                                    ],
                                'convertedCurrentPrice':
                                    [
                                        {
                                            '@currencyId': 'USD',
                                            '__value__': '3.95'
                                        }
                                    ],
                                'sellingState': ['Active'],
                                'timeLeft': ['P23DT17H35M35S']
                            }
                        ],
                    'listingInfo':
                        [
                            {
                                'bestOfferEnabled': ['false'],
                                'buyItNowAvailable': ['false'],
                                'startTime': ['2019-06-04T17:45:06.000Z'],
                                'endTime': ['2019-07-04T17:45:06.000Z'],
                                'listingType': ['FixedPrice'],
                                'gift': ['false'],
                                'watchCount': ['19']
                            }
                        ],
                    'returnsAccepted': ['true'],
                    'isMultiVariationListing': ['false'],
                    'topRatedListing': ['false']
                },
                ...
            ]
        """
        if self._content_page_number == self.page_number:
            return

        response = requests.get(self.endpoint).json()['findItemsAdvancedResponse'][0]

        self.total_pages = int(response['paginationOutput'][0]['totalPages'][0])
        self.total_entries = int(response['paginationOutput'][0]['totalEntries'][0])

        self.content = response['searchResult'][0]['item']
        self._content_page_number = self.page_number

    @property
    def endpoint(self):
        return self._endpoint.format(page_number=self.page_number)
