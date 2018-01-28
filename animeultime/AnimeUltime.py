from .AnimeUltimeLink import AnimeUltimeLink

class AnimeUltime:

    def get_id(self, link):
        link = AnimeUltimeLink(link)
        if(link.is_valid()):
            return link.id
        return None
    
    def get_links(self, link):
        link = AnimeUltimeLink(link)
        if not link.is_valid():
            raise Exception('Invalid link')
        info = link.extract_info()
        if link.type == "episode":
            return {
                info["title"][:-16] : info["links"]["stream-hq"]
            }
        if link.type == "serie":
            serie_episodes = {}
            for key, value in info.items():
                tmp = AnimeUltimeLink(value["link"])
                if tmp.is_valid():
                    tmp_info = tmp.extract_info()
                    serie_episodes[tmp_info["title"][:-16]] = tmp_info["links"]["stream-hq"]
            return serie_episodes
