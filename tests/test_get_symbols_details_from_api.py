import requests
from assertpy import assert_that, soft_assertions
from .configs import *
import logging
import pandas as pd
import pytest

LOGGER = logging.getLogger('pytest.ini')

'''This fixture is getting url'''
@pytest.fixture()
def url():
    return get_url()


'''This fixture will get symbols from api  and return them into a list '''
@pytest.mark.smoke
def test_get_symbols_from_api(url):
    url_response = requests.get(url)
    LOGGER.info(f"url_response is {url_response}")
    json_data = url_response.json()
    assets_list = []
    for item in json_data:
        assets_list.append(item['symbol'])
    return assets_list


'''This fixture will get symbol details like -- symbol_name, priceInCUSD or priceInCUSDC and priceInRowan for that 
 particular symbol.If API is not able to fetch the  details of that  symbol then it will return that symbol  into a 
 csv file '''
@pytest.mark.smoke
def test_symbol_details_from_api(url):
    error_symbol_list = []
    for item in test_get_symbols_from_api(url):

        symbol_api_url = f"{url}/{item}"
        symbol_api_url_response = requests.get(symbol_api_url)
        symbol_api_url_json_data = symbol_api_url_response.json()

        for key in symbol_api_url_json_data:
            if key == "error":
                error_symbol_list.append(item)
                LOGGER.info(error_symbol_list)
            else:
                symbol = symbol_api_url_json_data['symbol']
                with soft_assertions():
                    assert_that(symbol).is_equal_to(item)
                    for key in symbol_api_url_json_data:
                        if key == "priceInCUSD":
                            price_in_usd = symbol_api_url_json_data[key]
                            assert_that(float(price_in_usd)).is_greater_than(0)
                        elif key == "priceInUSDC":
                            price_in_usdc = symbol_api_url_json_data[key]
                            assert_that(float(price_in_usdc)).is_greater_than(0)
                    price_in_rowan = symbol_api_url_json_data['priceInRowan']

                    assert_that(float(price_in_rowan)).is_greater_than(0)
    # df = pd.DataFrame(error_symbol_list, columns=['Symbols'])
    # file_path = "reports"
    # file_name = "/symbolss_error.csv"
    # df.to_csv(f"{file_path}{file_name}", index=False)
