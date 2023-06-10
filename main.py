import aiohttp
import asyncio
from datetime import datetime, timedelta

class ExchangeRateService:
    def __init__(self, api_url):
        self.api_url = api_url

    async def get_exchange_rates(self, session, date):
        url = f"{self.api_url}/p24api/exchange_rates"
        params = {"json": "", "date": date}
        async with session.get(url, params=params) as response:
            data = await response.json()
            if "exchangeRate" in data:
                return data["exchangeRate"]
            else:
                return []

class ExchangeRateAnalyzer:
    def __init__(self, exchange_rate_service):
        self.exchange_rate_service = exchange_rate_service

    async def analyze_exchange_rates(self, days, target_currencies):
        days = min(days, 10)
        exchange_rates_list = []
        async with aiohttp.ClientSession() as session:
            tasks = [self.exchange_rate_service.get_exchange_rates(session, (datetime.now() - timedelta(days=i)).strftime("%d.%m.%Y")) for i in range(days)]
            results = await asyncio.gather(*tasks)
            for i, exchange_rates in enumerate(results):
                date = (datetime.now() - timedelta(days=i)).strftime("%d.%m.%Y")
                exchange_rates_dict = {date: {}}
                for rate in exchange_rates:
                    currency = rate["currency"]
                    if currency in target_currencies:
                        sale_rate = rate["saleRateNB"]
                        purchase_rate = rate["purchaseRateNB"]
                        exchange_rates_dict[date][currency] = {
                            "sale": sale_rate,
                            "purchase": purchase_rate
                        }
                if exchange_rates_dict[date]:
                    exchange_rates_list.append(exchange_rates_dict)
        return exchange_rates_list

async def main():
    api_url = "https://api.privatbank.ua"

    num_days = int(input("Введіть кількість днів (не більше 10): "))
    if num_days > 10:
        print("Кількість днів перевищує максимальне значення (10).")
        return

    currency = str(input("Введіть валюту (наприклад: USD): ")).upper()
    list_currency = ["USD", "EUR", "CHF", "GBP", "PLZ", "SEK", "XAU", "CAD"]
    if currency not in list_currency:
        print("Такої валюти немає. Доступні валюти:", ", ".join(list_currency))
        return

    exchange_rate_service = ExchangeRateService(api_url)
    exchange_rate_analyzer = ExchangeRateAnalyzer(exchange_rate_service)

    exchange_rates = await exchange_rate_analyzer.analyze_exchange_rates(num_days, [currency])

    print(exchange_rates)

if __name__ == "__main__":
    asyncio.run(main())
