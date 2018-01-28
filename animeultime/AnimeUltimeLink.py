import re
from bs4 import BeautifulSoup
import requests

class AnimeUltimeLink:

    def __init__(self, link):
        self.link = link
        self.valid = self.verify(self.link)

    def verify(self, link):
        test = []
        if('file-0-1' in link):
            test = re.findall(
                r"http://www.anime-ultime.net/file-0-1/([0-9]+)/",
                self.link
            )
            self.type = 'serie'
        else:
            test = re.findall(
                r"http://www.anime-ultime.net/info-0-1/([0-9]+)/",
                self.link
            )
            self.type = 'episode'

        if(test == []):
            return False
        self.id = test[0]
        return True

    def is_valid(self):
        return self.valid

    def extract_info(self):
        if self.type == "episode":
            return self.extract_episode_info()
        elif self.type == "serie":
            return self.extract_serie_info()

    # TODO: Extract lowq and dl link + other infos
    def extract_episode_info(self):
        info = {}
        soup = BeautifulSoup(
            requests.get(self.link).text,
            'html.parser'
        )
        info['title'] = soup.find(
            "meta",
            attrs={"name":"title"}
        ).get('content')[:-16]
        info['links'] = {
            'stream-hq' : soup.find(
                "meta",
                attrs={"property":"og:video"}
            ).get('content')
        }
        return info

    def extract_serie_info(self):
        info = {}
        cnt = 1
        soup = BeautifulSoup(
            requests.get(self.link).text,
            'html.parser'
        )
        table = soup.find("table").find_all('tr')
        for tr in table[1:]:
            temp = {}
            x = tr.select('td')
            temp['date'] = x[1].text
            temp['title'] = x[2].text
            temp['link'] = "http://www.anime-ultime.net/" + x[5].find('a').get("href")
            info[str(cnt)] = temp
            cnt += 1
        return info
