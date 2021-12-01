from assertpy import assert_that
from configs import *
import pandas as pd
import logging

LOGGER = logging.getLogger('pytest.ini')

'''This fixture is getting url response i.e in json format  '''
@pytest.fixture()
def url_response():
    return requests.get(get_url())


'''This fixture is checking url_response status_code and header content-type as well as 
content-length '''
@pytest.mark.smoke
def test_response_status_and_headers(url_response):
    assert_that(url_response.status_code).is_equal_to(200)
    assert_that(url_response.headers['content-type']).is_equal_to('application/json')
    assert_that(int(url_response.headers['content-length'])).is_between(7000, 8000)


'''This fixture is getting symbols from a csv file'''
@pytest.mark.smoke
def test_symbols_from_csv_file():
    file_path = "../input_data"
    file = "/symbols_from_csv_file.csv"
    df = pd.read_csv(f"{file_path}/{file}", header=None, skiprows=1, index_col=0)
    return df.index


'''This fixture is getting symbols from API  '''
@pytest.mark.smoke
def test_symbols_from_api(url_response):
    newassetslist = []
    for item in url_response.json():
        newassetslist.append(item["symbol"])

    return newassetslist


'''This fixture is comparing the length of baseline_assets and  newline_assets '''
@pytest.mark.regression
def test_compare_baseline_assets_and_newline_assets_length(url_response):
    baseline_assets = test_symbols_from_csv_file()
    newline_assets = test_symbols_from_api(url_response)

    length1 = len(baseline_assets)
    LOGGER.info(f"The length of baseline_assets is:= {length1}")
    length2 = len(newline_assets)
    LOGGER.info(f"The length of newline_assets is: = {length2}")

    if length1 == length2:
        LOGGER.info(f"The length of baseline_assets and newline_assets matches")
    else:
        LOGGER.info(f"The length of baseline_assets and newline_assets doesn't matches")



'''This fixture is comparing the data of csv file and API response data, 1st it will sort whole data and then compare 
  the content if the content is not same then it will also return unmatched content '''
@pytest.mark.regression
def test_compare_content_of_baseline_assets_and_newline_assets(url_response):
    baseline_assets = sorted(test_symbols_from_csv_file())
    newline_assets = sorted(test_symbols_from_api(url_response))

    if baseline_assets == newline_assets:
        LOGGER.info(f"The content of baseline_assets and newline_assets are same ")

    else:

        list1 = list(set(baseline_assets) - set(newline_assets))
        list2 = list(set(newline_assets) - set(baseline_assets))

        LOGGER.info(f"The different symbols in baseline_assets are= {list1}")
        LOGGER.info(f"The different symbols in newline_assets are= {list2}")
