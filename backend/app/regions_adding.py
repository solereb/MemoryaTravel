from src.database.services.country_service import CountryService
from src.database.core.session import AsyncSessionLocal
from src.database.services.region_service import RegionService
import asyncio
import aiohttp


    
    
async def get_regions_from_geonames(country_code, lang):
    try:
        url = "http://api.geonames.org/searchJSON"
        params = {
            'country': country_code,
            'featureClass': 'A',
            'featureCode': 'ADM1',
            'username': 'steal_pork',
            'lang': lang,
            'maxRows': 100
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('geonames', [])
                return []
    except:
        return []

def extract_region_code(region, country_code):
    admin_codes = region.get('adminCodes1', {})
    region_code = admin_codes.get('ISO3166_2', '')
    if region_code and region_code.startswith(f"{country_code}-"):
        region_code = region_code.replace(f"{country_code}-", "", 1)
    if not region_code:
        region_code = region.get('adminCode1', '')
    return region_code


async def main():
    async with AsyncSessionLocal() as session:
        countries = await CountryService.get_all(session=session)
        all_regions = {}
        processed = 0
        for country in countries:
                try:
                    country_code = country.code
                    regions_ru = await get_regions_from_geonames(country_code, 'ru')
                    regions_en = await get_regions_from_geonames(country_code, 'en')
                    en_dict = {}
                    for region in regions_en:
                        geoname_id = region.get('geonameId')
                        if geoname_id:
                            en_dict[geoname_id] = {
                                'name': region.get('name', ''),
                                'code': extract_region_code(region, country_code)
                            }
                    
                    country_data = {}
                    for region in regions_ru:
                        geoname_id = region.get('geonameId')
                        name_ru = region.get('name', '')
                        region_code = extract_region_code(region, country_code)
                        
                        if not region_code:
                            continue
                        
                        english_data = en_dict.get(geoname_id, {})
                        name_en = english_data.get('name', name_ru)
                        
                        country_data[region_code] = {
                            'name_ru': name_ru,
                            'name_en': name_en,
                            'region_code': region_code,
                            'country_code': country_code
                        }
                        c = await RegionService.create(session, name_ru, name_en, country_code, country.id)
                        print(c)
                    all_regions[country_code] = country_data
                    processed += 1
                except Exception as e:
                    print(f"Ошибка для страны {country_code}: {e}")
                    all_regions[country_code] = {}
                    continue
                
if __name__ == "__main__":
    asyncio.run(main())