from generic_crawler.core import GenericCrawler, ActionReader
from generic_crawler.config import Config

from dotenv import load_dotenv
load_dotenv()

config = Config(token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoidGVzdDFAdGVzdC5jb20iLCJleHBpcmVzIjoxNjYwODkxODkxLjUzMjQ1NzZ9.Jdj9sYJyPGDw-d5jKkgzfyZtMecWvmDJYGeYcYCJsNQ",
                endpoint_url="https://generic-crawler-service-ai-sensai.apps.gocpgp01.tcs.turkcell.tgc")

crawler = GenericCrawler(config=config)
reader = ActionReader(path_to_yaml="/Users/tcudikel/Dev/ace/reguletter-crawler/actions/tbmm/khk.yaml")


data, _ = crawler.retrieve(reader.action)

crawled_products = []
crawled_products.extend(data['static review str in item boxes'])
pagin_url = data["last pagination item url"][0]

while 'no url found' != pagin_url:
    reader.action["url"] = pagin_url
    data, response = crawler.retrieve(reader.action)
    pagin_url = data["last pagination item url"][0]
    crawled_products.extend(data['static review str in item boxes'])





print("ok")
