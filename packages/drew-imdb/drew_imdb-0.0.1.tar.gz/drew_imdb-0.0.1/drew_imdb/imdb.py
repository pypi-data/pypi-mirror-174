import requests
import lxml.html

def get_rating(tid: str) -> float:
    """
    Given an imdb title id, return the title's rating.
    """
    resp = requests.get(f"https://www.imdb.com/title/{tid}", stream=True)
    resp.raw.decode_content = True
    tree = lxml.html.parse(resp.raw)
    element = tree.xpath("//div[@data-testid='hero-rating-bar__aggregate-rating__score']/span")[0]
    return float(element.text)