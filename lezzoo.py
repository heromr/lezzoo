import httpx
import asyncio
import logging

class LezzooAPI:
    API_BASE_URL = 'https://production.customerapi.lezzoodevs.com/app/v2.81'
    DEFAULT_PARAMS = {
        'language': 'en',
        'city': 'Erbil',
        'appVersion': '2.995',
    }

    COLOR_CODES = {
        'reset': '\033[0m',
        'bright_cyan': '\033[1;36m',
        'bright_yellow': '\033[1;33m',
        'bright_green': '\033[1;32m',
        'bright_magenta': '\033[1;35m',
        'bright_red': '\033[1;31m',
        'bright_blue': '\033[1;34m',
        'dark_gray': '\033[1;30m'
    }

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = httpx.AsyncClient()

    async def search_merchants(self, query: str):
        search_params = {
            'pageSize': '25',
            'currentPage': '1',
            'vertical': 'All',
            'parentId': '0',
            'tag': '',
            'query': query,
            **self.DEFAULT_PARAMS
        }

        try:
            response = await self.client.get(f"{self.API_BASE_URL}/elasticSearch", params=search_params)
            return response.json()
        except httpx.HTTPError as e:
            self.logger.error(f"Search Error: {e}")
            return None

    async def fetch_merchant_info(self, merchant_id: str, branch_id: str):
        info_params = {
            'branchId': branch_id,
            'orderType': '1',
            **self.DEFAULT_PARAMS
        }

        try:
            response = await self.client.get(f"{self.API_BASE_URL}/merchants/{merchant_id}", params=info_params)
            return response.json()
        except httpx.HTTPError as e:
            self.logger.error(f"Merchant Info Error: {e}")
            return None

    async def fetch_merchant_products(self, merchant_id: str):
        try:
            response = await self.client.get(f"{self.API_BASE_URL}/merchants/{merchant_id}/all-products", params=self.DEFAULT_PARAMS)
            return response.json()
        except httpx.HTTPError as e:
            self.logger.error(f"Fetch Products Error: {e}")
            return None

    async def main(self):
        query = input("Enter search query: ")
        search_result = await self.search_merchants(query)

        if not search_result:
            exit("Search request failed.")

        merchants_list = search_result.get("merchants", [])
        for i, merchant in enumerate(merchants_list, start=1):
            print(f"Merchant Index: {i}")
            print(f"Merchant Name: {merchant.get('merchant_name', '')}")
            print(f"Merchant ID: {merchant.get('merchant_id', '')}")
            print(f"Merchant Logo: {merchant.get('merchant_logo', '')}")
            print(f"Merchant Distance: {merchant.get('merchant_distance', '')} km")
            print("-" * 30)

        index = input("Enter merchant index: ")
        try:
            selected_merchant_id = merchants_list[int(index) - 1]['merchant_id']
        except (ValueError, IndexError):
            exit("Invalid index.")

        merchant_info = await self.fetch_merchant_info(merchant_id=selected_merchant_id, branch_id='0')

        print()
        print(f"Merchant ID: {merchant_info.get('merchant_id', '')}")
        print(f"Merchant Name: {merchant_info.get('merchant_name', '')}")
        print(f"Merchant Longitude: {merchant_info.get('merchant_longitude', '')}")
        print(f"Merchant Latitude: {merchant_info.get('merchant_latitude', '')}")
        print(f"Merchant Min Order: {merchant_info.get('merchant_min_order', '')}")
        print(f"Merchant Logo: {merchant_info.get('merchant_logo', '')}")
        print(f"Merchant Image: {merchant_info.get('merchant_image', '')}")
        print(f"Merchant Rate: {merchant_info.get('merchant_rate', '')}")
        print(f"Merchant Rated Orders: {merchant_info.get('merchant_rated_orders', '')}")
        print(f"Merchant Working Status: {merchant_info.get('merchant_working_status', '')}")
        print(f"Merchant City: {merchant_info.get('merchant_city', '')}")
        print(f"Merchant Delivery Time: {merchant_info.get('merchant_delivery_time', '')}")
        print(f"Merchant Type: {merchant_info.get('merchant_type', '')}")
        print(f"Merchant Vertical: {merchant_info.get('merchant_vertical', '')}")
        print(f"Merchant Has Lezzoo Delivery: {'Yes' if merchant_info.get('merchant_has_lezzoo_delivery', '') else 'No'}")
        print(f"Merchant Open Time: {merchant_info.get('merchant_open_time', '')}")
        print(f"Merchant Close Time: {merchant_info.get('merchant_close_time', '')}")
        print(f"Voucher Data: {merchant_info.get('voucherData', [])}")

        merchant_details = merchant_info.get("merchantInfo", [])
        for detail in merchant_details:
            print(f"{detail.get('title')}: {detail.get('data')}")

        print()

        choice = input("Do you want to get merchant products (y/n): ")
        if choice.lower() == 'y':
            products_data = await self.fetch_merchant_products(merchant_id=selected_merchant_id)
            products_list = products_data.get("products", [])
            for product in products_list:
                print(self.COLOR_CODES['bright_yellow'] + f"Product Name:", product.get('product_name'))
                print(self.COLOR_CODES['bright_green'] + f"Product Price:", product.get('product_price'))
                print(self.COLOR_CODES['bright_magenta'] + f"Product Image:", product.get('product_image_url'))
                print(self.COLOR_CODES['bright_red'] + f"Date Added:", product.get('product_date_added'))
                print(self.COLOR_CODES['bright_blue'] + "-" * 30 + self.COLOR_CODES['reset'])

if __name__ == "__main__":
    lezzoo_api = LezzooAPI()
    asyncio.run(lezzoo_api.main())
