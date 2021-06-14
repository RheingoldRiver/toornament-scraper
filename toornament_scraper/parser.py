import requests
from bs4 import BeautifulSoup
from toornament_scraper.toornament_match import ToornamentMatch
from mwrogue.wiki_time_parser import time_from_str


class Parser(object):
    
    def __init__(self, base_url):
        self.base_url = base_url
    
    def run(self):
        match_list_final = []
        
        # we don't know how many pages long the list of tournaments is
        # so start at 1 and then go until we hit a 404
        page_index = 1
        while True:
            response = requests.get(self.base_url + str(page_index))
            # emergency fallback at 1000 just in case?
            if response.status_code == 404 or page_index > 1000:
                break
            
            page_soup = BeautifulSoup(response.text, features='html.parser')
            match_list_raw = page_soup.findAll('div', {'class': 'grid-flex vertical spaceless'})
            match_list_div = match_list_raw[0].find_all(lambda tag: tag.name == 'div' and
                                                                    tag.get('class') == ['size-content'])
            
            for i, html_match in enumerate(match_list_div):
                team1 = ''
                if html_match.findAll('div', {'class': 'name'})[0].text.strip() != 'To be determined':
                    team1 = html_match.findAll('div', {'class': 'name'})[0].text.strip()
                team2 = ''
                if html_match.findAll('div', {'class': 'name'})[1].text.strip() != 'To be determined':
                    team2 = html_match.findAll('div', {'class': 'name'})[1].text.strip()
                
                wiki_match = ToornamentMatch(
                    timestamp=time_from_str(html_match.find('datetime-view')['value']),
                    team1=team1,
                    team2=team2,
                    url=html_match.findAll('a', href=True)[0]['href'],
                    page=page_index,
                    index_in_page=i
                )
                if html_match.findAll('div', {'class': 'result forfeit'}) and \
                        not html_match.findAll('div', {'class': 'opponent win'}):
                    wiki_match.both_forfeit()
                else:
                    wiki_match.calculate_and_set_winner(
                        html_match.findAll('div', {'class': 'opponent win'})
                    )
                
                match_list_final.append(wiki_match)
            
            page_index += 1
        
        return match_list_final


if __name__ == '__main__':
    Parser('https://www.toornament.com/en_GB/tournaments/3543821601845821440/matches/schedule?page=').run()

# example single ff
# https://www.toornament.com/en_GB/tournaments/3543967453632937984/matches/schedule?page=1
# https://www.toornament.com/en_GB/tournaments/3543967453632937984/matches/3603330036821811312/
