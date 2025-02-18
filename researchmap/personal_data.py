import pandas as pd
import openpyxl
import time

class ResearchmapPersonalData:
    def __init__(self):
        self.family_name_en = ''
        self.given_name_en = ''
        self.family_name_ja = ''
        self.given_name_ja = ''
        self.family_name_kana = ''
        self.given_name_kana = ''
        self.achievement_stats = None
        self.research_field = ''
        self.research_keyword = ''
        self.permalink = ''
        self.affiliations = []
        self.degrees = []
        self.awards = []
        self.research_experiences = []
        self.education_history = []
        self.commitee_memberships = []
        self.published_papers = []
        self.misc_items = []
        self.presentations = []
        self.books = []
        self.patents = []

    def get_name_ja(self):
        return f"{self.family_name_ja} {self.given_name_ja}"
    
    def get_name_en(self):
        return f"{self.family_name_en} {self.given_name_en}"
    
    def get_name_kana(self):
        return f"{self.family_name_kana} {self.given_name_kana}"

    def get_permalink(self):
        return self.permalink

    def parse_json(self, json_data):
        if json_data is None:
            return

        self.__parse_personal_info__(json_data)
        self.__parse_affiliations__(json_data)
        self.__parse_degrees__(json_data)

        for graph_entry in json_data.get('@graph', []):
            item_type = graph_entry.get('@type', None)

            if item_type == 'awards':
                self.__parse_award__(graph_entry)
            elif item_type == 'research_areas':
                self.__parse_research_research_areas__(graph_entry)
            elif item_type == 'research_experience':
                self.__parse_research_experiences__(graph_entry)
            elif item_type == 'education':
                self.__parse_education_history__(graph_entry)
            elif item_type == 'committee_memberships':
                self.__parse_commitee_memberships__(graph_entry)
            elif item_type == 'industrial_property_rights':
                self.__parse_patent__(graph_entry)
            elif item_type == 'misc':
                self.__parse_misc_items__(graph_entry)
            elif item_type == 'books_etc':
                self.__parse_books__(graph_entry)

    def __parse_personal_info__(self, json_data):
        self.family_name_en = json_data.get('family_name', {}).get('en', None)
        self.given_name_en = json_data.get('given_name', {}).get('en', None)
        self.family_name_ja = json_data.get('family_name', {}).get('ja', None)
        self.given_name_ja = json_data.get('given_name', {}).get('ja', None)
        self.family_name_kana = json_data.get('family_name', {}).get('ja-Kana', None)
        self.given_name_kana = json_data.get('given_name', {}).get('ja-Kana', None)
        self.permalink = json_data.get('permalink', None)

    def __parse_research_research_areas__(self, graph_entry):
        research_field_list = []
        research_keyword_list = []

        for item in graph_entry.get('items', []):
            research_field = self.get_ja_or_en(item.get('research_field', {}))
            if research_field != '':
                research_field_list.append(research_field)
            research_keyword = self.get_ja_or_en(item.get('research_keyword', {}))
            if research_keyword != '':
                research_keyword_list.append(research_keyword)

        self.research_field = ';'.join(research_field_list)
        self.research_keyword = ';'.join(research_keyword_list)

    def __parse_research_experiences__(self, graph_entry):
        for item in graph_entry.get('items', []):
            self.research_experiences.append({
                '研究機関': self.get_ja_or_en(item.get('affiliation', {})),
                '部署': self.get_ja_or_en(item.get('section', {})),
                '職位': self.get_ja_or_en(item.get('job', {})),
                '開始時期': self.date_formatter(item.get('from_date', None)),
                '終了時期': self.date_formatter(item.get('to_date', None))
            })

    def __parse_education_history__(self, graph_entry):
        for item in graph_entry.get('items', []):
            self.education_history.append({
                '教育機関': self.get_ja_or_en(item.get('affiliation', {})),
                '教育部署': self.get_ja_or_en(item.get('department', {})),
                '教育課程': self.get_ja_or_en(item.get('course', {})),
                '開始時期': self.date_formatter(item.get('from_date', None)),
                '終了時期': self.date_formatter(item.get('to_date', None))
            })

    def __parse_commitee_memberships__(self, graph_entry):
        for item in graph_entry.get('items', []):
            self.commitee_memberships.append({
                '組織': self.get_ja_or_en(item.get('association', {})),
                '役職': self.get_ja_or_en(item.get('committee_name', {})),
                '開始時期': self.date_formatter(item.get('from_date', None)),
                '終了時期': self.date_formatter(item.get('to_date', None))
            })

    def __parse_award__(self, graph_entry):
        for item in graph_entry.get('items', []):
            winners = [d.get('name', None) for d in item.get('winners', {}).get('ja', item.get('winners', {}).get('en', []))]
            if len(winners) == 0:
                winners = [self.get_name_ja()]

            is_first_authored = winners[0].startswith(self.family_name_ja) or winners[0].lower().startswith(self.family_name_en.lower()) or winners[0].lower().startswith(self.given_name_en.lower())

            self.awards.append({
                '受賞者': winners,
                '受賞名': self.get_ja_or_en(item.get('award_name', {})),
                '受賞内容': self.get_ja_or_en(item.get('description', {})),
                '授与機関': self.get_ja_or_en(item.get('association', {})),
                '主著': is_first_authored,
                '受賞年月': self.date_formatter(item.get('award_date', None))
            })

    def parse_published_papers(self, graph_entry):
        if graph_entry is None:
            return
        
        for item in graph_entry.get('items', []):
            publication_name = self.get_ja_or_en(item.get('publication_name', {}))
            paper_type = self.get_paper_type(item.get('published_paper_type', None), publication_name)
            language_type = self.get_paper_language_type(item.get('languages', [None])[0], publication_name)
            author_list = self.get_name_list(item.get('authors', {}), 'name', language_type)
            is_first_authored = self.is_first_authored(author_list, language_type)

            self.published_papers.append({
                '著者': author_list,
                '論文名': self.get_ja_or_en(item.get('paper_title', {})),
                '掲載誌': publication_name,
                '掲載種別': paper_type,
                '言語': language_type,
                '主著': is_first_authored,
                '掲載年月': self.date_formatter(item.get('publication_date', None))
            })

    def parse_presentations(self, graph_entry):
        if graph_entry is None:
            return
        
        for item in graph_entry.get('items', []):
            presenter_list = [d.get('name', None) for d in item.get('presenters', {}).get('en', item.get('presenters', {}).get('ja', []))]

            self.presentations.append({
                '著者': presenter_list,
                '発表名': self.get_ja_or_en(item.get('presentation_title', {})),
                '会議名': self.get_ja_or_en(item.get('event', {})),
                '発表年月': self.date_formatter(item.get('from_event_date', None))
            })

    def __parse_misc_items__(self, graph_entry):
        for item in graph_entry.get('items', []):
            author_list = [d.get('name', None) for d in item.get('authors', {}).get('en', item.get('authors', {}).get('ja', []))]
            language_type = item.get('languages', [None])[0]
            is_first_authored = self.is_first_authored(author_list, language_type)
            publication_name = self.get_ja_or_en(item.get('publication_name', {}))

            self.misc_items.append({
                '著者': author_list,
                '論文名': self.get_ja_or_en(item.get('paper_title', {})),
                '掲載誌': publication_name,
                '言語': self.get_language_type(language_type, publication_name),
                '主著': is_first_authored,
                '掲載年月': self.date_formatter(item.get('publication_date', None))
            })

    def __parse_books__(self, graph_entry):
        for item in graph_entry.get('items', []):
            author_list = [d.get('name', None) for d in item.get('authors', {}).get('ja', item.get('authors', {}).get('en', []))]
            language_type = item.get('languages', [None])[0]
            is_first_authored = self.is_first_authored(author_list, language_type)
            publisher = self.get_ja_or_en(item.get('publisher', {}))

            self.books.append({
                '著者': author_list,
                '書籍名': self.get_ja_or_en(item.get('book_title', {})),
                '出版社': publisher,
                '言語': self.get_language_type(language_type, publisher),
                '主著': is_first_authored,
                '出版年月': self.date_formatter(item.get('publication_date', None))
            })
    
    def __parse_patent__(self, json_item):
        for item in json_item.get('items', []):
            self.patents.append({
                '特許名': self.get_ja_or_en(item.get('industrial_property_right_title', {})),
                '出願番号': item.get('application_number', None),
                '特許番号': item.get('patent_number', None),
                '出願年月': self.date_formatter(item.get('application_date', None)),
                '登録年月': self.date_formatter(item.get('registration_date', None)),
                '特許権者': self.get_ja_or_en(item.get('right_holder', {}))
            })

    def __parse_affiliations__(self, json_data):
        for item in json_data.get('affiliations', []):
            self.affiliations.append({
                '所属': self.get_ja_or_en(item.get('affiliation', {})),
                '部署': self.get_ja_or_en(item.get('section', {})),
                '職位': self.get_ja_or_en(item.get('job', {}))
            })

    def __parse_degrees__(self, json_data):
        for item in json_data.get('degrees', []):
            self.degrees.append({
                '学位': self.get_ja_or_en(item.get('degree', {})),
                '授与機関': self.get_ja_or_en(item.get('degree_institution', {})),
                '取得年月': self.date_formatter(item.get('degree_date', None))
            })

    def summarize_achievement_stats(self):
        self.achievement_stats = {'国際雑誌': 0, '主著国際雑誌': 0, '和文雑誌': 0, '主著和文雑誌': 0, '国際会議': 0, '主著国際会議': 0, '受賞': 0, '主著受賞': 0}

        for paper in self.published_papers:
            self.achievement_stats['国際雑誌'] += 1 if paper['掲載種別'] == '雑誌論文' and paper['言語'] == '英語' else 0
            self.achievement_stats['主著国際雑誌'] += 1 if paper['掲載種別'] == '雑誌論文' and paper['言語'] == '英語' and paper['主著'] else 0
            self.achievement_stats['和文雑誌'] += 1 if paper['掲載種別'] == '雑誌論文' and paper['言語'] == '日本語' else 0
            self.achievement_stats['主著和文雑誌'] += 1 if paper['掲載種別'] == '雑誌論文' and paper['言語'] == '日本語' and paper['主著'] else 0
            self.achievement_stats['国際会議'] += 1 if paper['掲載種別'] == '国際会議' else 0
            self.achievement_stats['主著国際会議'] += 1 if paper['掲載種別'] == '国際会議' and paper['主著'] else 0
        
        for award in self.awards:
            self.achievement_stats['受賞'] += 1
            self.achievement_stats['主著受賞'] += 1 if award['主著'] else 0

    def save_to_excel(self, filename):
        try:
            personal_dict = {'氏名': self.get_name_ja(), 
                            '氏名(英語)': self.get_name_en(), 
                            '氏名(カナ)': self.get_name_kana(), 
                            '所属': ';'.join([d['所属'] for d in self.affiliations]),
                            '部署': ';'.join([d['部署'] for d in self.affiliations]),
                            '職位': ';'.join([d['職位'] for d in self.affiliations]),
                            '研究分野': self.research_field,
                            'キーワード': self.research_keyword,
                            '国際雑誌': '=COUNTIFS(論文!$D$2:$D$10000,"雑誌論文",論文!$E$2:$E$10000,"英語")',
                            '主著国際雑誌': '=COUNTIFS(論文!$D$2:$D$10000,"雑誌論文",論文!$E$2:$E$10000,"英語",論文!$F$2:$F$10000,"TRUE")',
                            '和文雑誌': '=COUNTIFS(論文!$D$2:$D$10000,"雑誌論文",論文!$E$2:$E$10000,"日本語")',
                            '主著和文雑誌': '=COUNTIFS(論文!$D$2:$D$10000,"雑誌論文",論文!$E$2:$E$10000,"日本語",論文!$F$2:$F$10000,"TRUE")',
                            '国際会議': '=COUNTIF(論文!$D$2:$D$10000,"国際会議")',
                            '主著国際会議': '=COUNTIFS(論文!$D$2:$D$10000,"国際会議",論文!$F$2:$F$10000,"TRUE")',
                            '受賞': '=COUNTA(受賞!$B$2:$B$1000)',
                            '主著受賞': '=COUNTIF(受賞!$E$2:$E$1000,"TRUE")',
                            'URL': f"https://researchmap.jp/{self.get_permalink()}"
                            }

            personal_df = pd.DataFrame([personal_dict])
            degrees_df = pd.DataFrame(self.degrees)
            affiliations_df = pd.DataFrame(self.affiliations)
            awards_df = pd.DataFrame(self.awards)
            research_experiences_df = pd.DataFrame(self.research_experiences)
            education_history_df = pd.DataFrame(self.education_history)
            commitee_memberships_df = pd.DataFrame(self.commitee_memberships)
            published_papers_df = pd.DataFrame(self.published_papers)
            presentations_df = pd.DataFrame(self.presentations)
            misc_items_df = pd.DataFrame(self.misc_items)
            books_df = pd.DataFrame(self.books)
            patents_df = pd.DataFrame(self.patents)

            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                personal_df.to_excel(writer, sheet_name='個人情報', index=False)
                degrees_df.to_excel(writer, sheet_name='学位', index=False)
                affiliations_df.to_excel(writer, sheet_name='所属', index=False)
                awards_df.to_excel(writer, sheet_name='受賞', index=False)
                research_experiences_df.to_excel(writer, sheet_name='研究経験', index=False)
                education_history_df.to_excel(writer, sheet_name='学歴', index=False)
                commitee_memberships_df.to_excel(writer, sheet_name='委員歴', index=False)
                published_papers_df.to_excel(writer, sheet_name='論文', index=False)
                presentations_df.to_excel(writer, sheet_name='発表', index=False)
                misc_items_df.to_excel(writer, sheet_name='その他', index=False)
                books_df.to_excel(writer, sheet_name='書籍', index=False)
                patents_df.to_excel(writer, sheet_name='特許', index=False)

            time.sleep(0.5)

            wb = openpyxl.load_workbook(filename)
            for sheet in wb.sheetnames:
                ws = wb[sheet]
                ws.auto_filter.ref = ws.dimensions
                ws.freeze_panes = 'A2'
            wb.save(filename)
        except Exception as e:
            print(f"  Exception: {e}")
            return None

    def get_name_list(self, list_dict, key, lang_type):
        if list_dict is None:
            return None

        if lang_type == 'jpn' or lang_type == '日本語':
            return [d.get(key, None) for d in list_dict.get('ja', list_dict.get('en', []))]
        elif lang_type == 'eng' or lang_type == '英語':
            return [d.get(key, None) for d in list_dict.get('en', list_dict.get('ja', []))]

    def is_first_authored(self, author_list, lang_type):
        if author_list is None or len(author_list) == 0:
            return False
        if self.family_name_ja is None:
            return False
        if lang_type == 'jpn' or lang_type == '日本語':
            return author_list[0].startswith(self.family_name_ja)
        if self.family_name_ja is None or self.given_name_en is None:
            return False
        if lang_type == 'eng' or lang_type == '英語':
            return author_list[0].lower().startswith(self.family_name_en.lower()) or author_list[0].lower().startswith(self.given_name_en.lower())
        return False

    def get_ja_or_en(self, text_dict):
        if text_dict is None:
            return None
        return text_dict.get('ja', text_dict.get('en', ''))

    def date_formatter(self, date_str):
        if date_str is None:
            return None
        return date_str.replace('-', '/')
    
    def get_paper_language_type(self, language_str, publication_name):
        if publication_name is not None:
            if '予稿' in publication_name or '講演' in publication_name or 'シンポジウム' in publication_name or '論文集' in publication_name or '論文誌' in publication_name or '学会誌' in publication_name:
                return '日本語'
            elif 'Proceeding' in publication_name or 'Proc.' in publication_name or 'Conf.' in publication_name or 'International Conference' in publication_name:
                return '英語'
            elif 'Journal' in publication_name or 'J.' in publication_name or 'Transactions' in publication_name or 'Trans.' in publication_name:
                return '英語'

        if language_str == 'jpn':
            return '日本語'
        elif language_str == 'eng':
            return '英語'
        elif language_str is not None:
            return f"その他({language_str})"

        if publication_name is not None:
            if publication_name.isascii():
                return '英語'
            else:
                return '日本語'

        return None

    def get_language_type(self, language_str, reference_str=None):
        if language_str is None:
            if reference_str is None:
                return None
            if reference_str.isascii():
                return '英語'
            else:
                return '日本語'
        if language_str == 'jpn':
            return '日本語'
        elif language_str == 'eng':
            return '英語'
        else:
            return f"その他({language_str})"

    def get_paper_type(self, publication_str, publication_name):
        if publication_str is None:
            if publication_name is None:
                return None
            if 'Proceeding' in publication_name or 'Proc.' in publication_name or 'Conf.' in publication_name or 'International Conference' in publication_name:
                return '国際会議'
            elif 'Journal' in publication_name or 'J.' in publication_name or 'Transactions' in publication_name or 'Trans.' in publication_name or '論文誌' in publication_name or '学会誌' in publication_name:
                return '雑誌論文'
            elif '予稿' in publication_name or '講演' in publication_name or 'シンポジウム' in publication_name or '論文集' in publication_name:
                return 'シンポジウム'
            return None
        
        if publication_str == 'scientific_journal':
            return '雑誌論文'
        elif publication_str == 'international_conference_proceedings':
            return '国際会議'
        elif publication_str == 'symposium':
            return 'シンポジウム'
        else:
            return f"その他({publication_str})"

