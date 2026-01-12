import requests
import json
from src.database.services.country_service import CountryService
from src.database.core.session import AsyncSessionLocal
import asyncio

async def get_geonames_countries():
    async with AsyncSessionLocal() as session:
        url_ru = "http://api.geonames.org/countryInfoJSON"
        params_ru = {'username': 'steal_pork', 'lang': 'ru'}
        
        response_ru = requests.get(url_ru, params=params_ru, timeout=30)
        
        if response_ru.status_code != 200:
            logger.error(f"Ошибка получения русских названий: {response_ru.status_code}")
            return []
        
        countries_ru = response_ru.json().get('geonames', [])
        

        params_en = {'username': 'steal_pork', 'lang': 'en'}
        response_en = requests.get(url_ru, params=params_en, timeout=30)
        
        if response_en.status_code != 200:
            logger.warning("Не удалось получить английские названия, используем русские")
            countries_en = countries_ru
        else:
            countries_en = response_en.json().get('geonames', [])
        
        countries_map = {}

        for country in countries_ru:
            code = country.get('countryCode', '')
            if code:
                countries_map[code] = {
                    'name_ru': country.get('countryName', ''),
                    'iso_code': code,
                    'iso3_code': country.get('isoAlpha3', ''),
                    'phone_code': country.get('phone', ''),
                    'capital_ru': country.get('capital', ''),
                    'continent': country.get('continentName', '')
                }

        for country in countries_en:
            code = country.get('countryCode', '')
            if code in countries_map:
                countries_map[code]['name_en'] = country.get('countryName', '')
            else:
                countries_map[code] = {
                    'name_en': country.get('countryName', ''),
                    'name_ru': country.get('countryName', ''),
                    'iso_code': code,
                    'iso3_code': country.get('isoAlpha3', '')
                }
        
        countries_list = list(countries_map.values())
        
        for country in countries_list:
            await CountryService.create(session=session, name_ru=country.get('name_ru'), name_en=country.get('name_en', ''), code=country.get('iso_code', ''))
            
        
if __name__ == "__main__":
    asyncio.run(get_geonames_countries())