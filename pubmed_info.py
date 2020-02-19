# Author: L.A.B.
# Last modified August 2019
# Fetching NCBI PubMed information using a pubmed_id
import pandas as pd
from shutil import copyfile
import time
from bs4 import BeautifulSoup
import certifi
import requests
import math
from crossref.restful import Works
import urllib3

# opening file
filename = "temp.csv"
# creating new file
newfile = "output.csv"
# copy imported file
copyfile(filename, newfile)
# extract data from file
filereader = pd.read_csv(newfile)
# size of data frame
counter = len(filereader)
my_columns = ['title', 'authors', 'journal', 'volume', 'issue', 'first_page', 'last_page', 'abstract', 'language']
my_rows = list(range(counter - 1))
df = pd.DataFrame(data=None, index=my_rows, columns=my_columns)
df2 = pd.concat([filereader, df], axis=1, join_axes=[filereader.index])
filereader = df2


def get_pubmed_id(doi, your_email):
    pmid = 0
    try:
        url = 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=my_tool&email='
        email = your_email
        doi_url = '%s%s&ids=%s' % (url, email, doi)
        # print(str(doi_url))
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        response = requests.get(str(doi_url))
        soup = BeautifulSoup(response.content, 'lxml')
        maintag = soup.select_one('record')
        if maintag:
            if maintag.get('pmid'):
                pmid = int(maintag.get('pmid'))

    except (urllib3.exceptions.HTTPError, AttributeError) as e:
        print("ERROR!", e)
    else:
        pass
    return pmid


def get_pubmed_info(temp_id):
    new_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    efetch_url = '%sefetch.fcgi?db=pubmed&id=%s&retmode=xml' % (new_url, temp_id)
    esummary_url = "".join('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=' + str(temp_id))
    # print(efetch_url, esummary_url)
    pub_issue = pub_year = pub_volume = pub_title = pub_language = pub_abstract = pub_journal = ""
    first_page = last_page = pub_issue = pub_doi = authors = ""

    # fetch doi and abstract
    try:
        url = str(efetch_url)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        maintag = soup.select_one('Abstract')
        pub_abstract = ''
        pub_doi = ''
        for childtag in maintag.select('AbstractText'):
            pub_abstract = childtag.text.strip()
        pub_doi = soup.select_one('ArticleId[IdType="doi"]').text
    except (urllib3.exceptions.HTTPError, AttributeError, ValueError) as e:
        print("ERROR!", e)
    else:
        pub_abstract = ''

        # fetching the remainder of the publication information
    try:
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        url = esummary_url
        results = http.request('GET', url)
        soup = BeautifulSoup(results.data, features='lxml')
        pub_title = soup.find('item', attrs={'name': 'Title'}).text
        author_list = soup.find_all('item', attrs={'name': 'Author'})
        pub_journal = soup.find('item', attrs={'name': 'Source'}).text
        pub_year = soup.find('item', attrs={'name': 'PubDate'}).text
        pub_year = pub_year[0:4]
        pub_volume = soup.find('item', attrs={'name': 'Volume'}).text
        pub_issue = soup.find('item', attrs={'name': 'Issue'}).text
        pub_pages = soup.find('item', attrs={'name': 'Pages'}).text
        page_position = pub_pages.find('-')
        last_page = pub_pages
        if page_position > 0:
            first_page = pub_pages[0:page_position]
            try:
                last_page = int(first_page) + int(pub_pages[(int(page_position) + 1):len(pub_pages)])
                last_page = str(last_page)
            except ValueError as e:
                print(e)
            else:
                pass

        else:
            first_page = last_page = 0
        pub_language = soup.find('item', attrs={'name': 'Lang'}).text
        authors = []
        for author in author_list:
            authors.append(author.text)
        authors = ", ".join(authors)
        print(authors)
    except (urllib3.exceptions.HTTPError, AttributeError) as e:
        print("ERROR!", e)
    else:
        pass
    filereader.loc[i, "title"] = pub_title
    filereader.loc[i, 'volume'] = pub_volume
    filereader.loc[i, 'abstract'] = pub_abstract
    filereader.loc[i, 'language'] = pub_language
    filereader.loc[i, 'year'] = pub_year
    filereader.loc[i, 'journal'] = pub_journal
    filereader.loc[i, 'first_page'] = first_page
    filereader.loc[i, 'last_page'] = last_page
    filereader.loc[i, 'issue'] = pub_issue
    filereader.loc[i, 'doi'] = pub_doi
    filereader.loc[i, 'authors'] = authors


def get_doi_info(i, doi, filereader):
    works = Works()
    try:
        result = works.doi(doi)

    except (AttributeError, ValueError) as err:
        print(err)
    else:
        pass
    # print(result)
    author_list = result.get("author")
    authors = []

    print("i am here")
    if result:
        try:
            pub_year = result.get('published-print')
            pub_year = pub_year.get('date-parts')
            pub_year = pub_year[0]
            pub_year = pub_year[0]
            pub_volume = result.get('volume')
            pub_journal = result.get('container-title')
            pub_page = result.get('page')
            pub_title = result.get('title')
            pub_language = result.get('language')
            pub_issue = result.get('issue')
            result = result.get('created')
            pub_authors = ''
            if result.get('author'):
                for i in author_list:
                    author_string = [i.get("family"), i.get("given")]
                    author_string = " ".join(author_string)
                    authors.append(author_string)
                pub_authors = authors
            print(pub_authors, pub_page, pub_journal, pub_title, pub_volume, pub_year, pub_language, pub_issue)
            filereader.at[i, "title"] = pub_title
            filereader.at[i, 'volume'] = pub_volume
            filereader.at[i, 'language'] = pub_language
            filereader.loc[i, 'year'] = pub_year
            filereader.loc[i, 'journal'] = pub_journal
            filereader.loc[i, 'last_page'] = pub_page
            filereader.loc[i, 'issue'] = pub_issue
            filereader.loc[i, 'authors'] = pub_authors
        except (AttributeError, ValueError, KeyError) as e:
            print(e)
        else:
            pass


for i in range(0, counter):
    print(i)
    if i > 0:
        if i % 50 == 0:
            time.sleep(10)
        if i % 15 == 0:
            filereader.to_csv('output.csv')
        if i % 100 == 0:
            time.sleep(20)
        if i % 1000 == 0:
            time.sleep(270)
    temp_id = filereader.at[i, 'pubmed_id']
    if temp_id > 0:
        # PubMed search may proceed
        temp_id = int(filereader.at[i, 'pubmed_id'])
        get_pubmed_info(int(temp_id))
    elif temp_id == 0 or math.isnan(temp_id) is True:
        if filereader.at[i, 'doi']:
            # get PubMed from doi'
            temp_id = int(get_pubmed_id(filereader.at[i, 'doi'], 'example@email.com'))
            # print(temp_id)
            doi = filereader.at[i, 'doi']
            if math.isnan(temp_id) is False:
                if temp_id > 0:
                    # doi generated a pubmed_id)
                    filereader.loc[i, 'pubmed_id'] = int(temp_id)
                    get_pubmed_info(int(temp_id))
                elif temp_id <= 0:
                    # proceed with doi search
                    get_doi_info(i, doi, filereader)
                else:
                    pass
