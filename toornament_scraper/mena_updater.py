import mwparserfromhell
from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from toornament_scraper.parser import Parser
from toornament_scraper.match import Match
from mwparserfromhell.nodes import Template


class MenaUpdater(object):
    def __init__(self, site: EsportsClient, title: str):
        self.site = site
        self.event = self.site.target(title).strip()
        self.data_pages = self.site.data_pages(self.event)
        self.toornament = self.site.cargo_client.query_one_result(
            tables='Tournaments',
            where='OverviewPage="{}"'.format(self.event),
            fields='ScrapeLink'
        )
        self.summary = "Edit made by web scraping!"
        self.parser = Parser(self.toornament)

    def run(self):
        matches = self.parser.run()
        i = 0
        match = matches[i]
        match: Match
        cur_page = None  # trailing index for printing at the end
        for page in self.data_pages:
            cur_page = page
            text = page.text()
            wikitext = mwparserfromhell.parse(text)
            for template in wikitext.filter_templates():
                template: Template
                if template.name.matches('MatchSchedule'):
                    if i >= len(matches):
                        break
                    
                    # allow for the possibility of partially updating an event
                    # that starts in the latter half of a toornament scrape, e.g. playoffs
                    # n.b. we can only do this if we added correct page and n_in_page tagging
                    # when we first created the event
                    if template.has('page', ignore_empty=True) and \
                            template.has('n_in_page', ignore_empty=True):
                        if int(template.get('page').value.strip()) < match.page:
                            continue
                        if int(template.get('n_in_page').value.strip()) < match.index_in_page:
                            continue
                    team1 = template.get('team1').value.strip()
                    team2 = template.get('team2').value.strip()
                    # TODO: some team validation? however remember there can be disambiguation
                    # TODO: so parse out anything in () when doing validation
                    if match.completed:
                        match.merge_into(template)
                    i += 1
                    match = matches[i]
                    match: Match
            page.save(str(wikitext), summary=self.summary)
        return 'https://lol.gamepedia.com/' + cur_page.name.replace(' ', '_')


if __name__ == "__main__":
    credentials = AuthCredentials(user_file='me')
    site = EsportsClient('lol', credentials=credentials)  # Set wiki
    scraper = MenaUpdater(site, 'Intel Arabian Cup 2020/Egypt/Split 1')
    scraper.run()
