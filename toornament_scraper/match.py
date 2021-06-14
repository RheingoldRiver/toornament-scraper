from mwparserfromhell.nodes import Template
from mwrogue.wiki_time import WikiTime


class Match(object):
    def __init__(self, timestamp: WikiTime = None, completed: bool = False, team1=None, team2=None,
                 team1score=None,team2score=None, winner=None, is_forfeit: bool = False, forfeit=None,
                 url=None, page=None, index_in_page=None):
        self.timestamp = timestamp
        self.completed = completed
        self.team1 = team1
        self.team2 = team2
        self.team1score = team1score
        self.team2score = team2score
        self.winner = winner
        self.is_forfeit = is_forfeit
        self.forfeit = forfeit
        self.url = url
        self.page = page
        
        # let's 1-index index_in_page because page_index urls are indexed, as are MediaWiki/Lua
        # also this index is *somewhat* user-facing, in that a user could attempt to add it themselves
        # so we may as well try and be somewhat editor-friendly
        # this is the only place the index is ever *set*, everywhere else we're comparing or reading it
        # from here so this isn't going to cause any burden to us (let's hope lol)
        self.index_in_page = index_in_page + 1

    def both_forfeit(self):
        self.is_forfeit = True
        self.forfeit = 'both'
        self.team1score = 0
        self.team2score = 0
        self.winner = 0

    def forefeit(self, team):
        self.is_forfeit = True
        self.forfeit = team
        if team == 1:
            self.winner = 2
        if team == 2:
            self.winner = 1

    def print(self):
        template = Template(name="MatchSchedule")
        self.add_field(template, 'date', self.timestamp.cet_date)
        self.add_field(template, 'time', self.timestamp.cet_time)
        self.add_field(template, 'timezone', 'CET')
        self.add_field(template, 'dst', self.timestamp.dst)
        self.add_field(template, 'stream', '  ')
        self.add_field(template, 'team1', self.team1)
        self.add_field(template, 'team2', self.team2)
        self.add_field(template, 'team1score', self.team1score)
        self.add_field(template, 'team2score', self.team2score)
        if self.is_forfeit:
            template.add('ff', self.forfeit)
        self.add_field(template, 'winner', self.winner)
        self.add_field(template, 'direct_link', self.url)
        self.add_field(template, 'page', self.page)
        self.add_field(template, 'n_in_page', self.index_in_page)
        return str(template)

    def merge_into(self, live_match: Template, overwrite_teams=False):
        self.add_field(live_match, 'team1score', self.team1score)
        self.add_field(live_match, 'team2score', self.team2score)
        self.add_field(live_match, 'winner', self.winner)
        if self.is_forfeit:
            self.add_field(live_match, 'ff', self.forfeit)
        if overwrite_teams:
            self.add_field(live_match, 'team1', self.team1)
            self.add_field(live_match, 'team2', self.team2)

    @staticmethod
    def add_field(template, field_name, field):
        if field is not None:
            template.add(field_name, str(field))
        else:
            template.add(field_name, ' ')
