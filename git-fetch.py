import urllib2
import json
import sys


def fetch_data(url, page_index="", page_items=""):
    """
    :param url:
    :param page_index:
    :param page_items: number of items per page
    :return: data from git, also checks for requests exceed and error
    """
    if page_index != "":
        page_index = '&page=' + str(page_index)

    if page_items != "":
        page_items = '&per_page=' + str(page_items)
    try:
        response = urllib2.urlopen(url + page_index + page_items)
    except urllib2.HTTPError as e:
        if e.code == 403:
            print "Requests Exceeded. Only 60 requests can be made in an hour."
            sys.exit()
        elif e.code == 422:
            print "Requested data not found"
            sys.exit()
    # if data returned is blank, return empty list so execution can continue
    try:
        data = json.load(response)
    except Exception as e:
        data = []
    return data


def fetch_driver(typeof, count, url, page_index, page_items):
    """
    :param typeof: can be repo or contribution
    :param count: count of data to be fetched
    :param url:
    :param page_index:
    :param page_items:
    :return: total data to be fetched
    """
    data_length = 0
    data = []
    while data_length != count:
        page_items = count-data_length
        if typeof == "repo":
            data_return = fetch_data(url, page_index, page_items)['items']
        else:
            data_return = fetch_data(url, page_index, page_items)
        if len(data_return) == 0:
            #no more data to fetch
            break
        data_length += len(data_return)
        data.extend(data_return)
        page_index += 1
    return data


organization = raw_input("Enter Organization Name:")
# organization = "google"
n = int(raw_input("Enter Repositories Count:"))
# n = 5
m = int(raw_input("Enter Commits Count:"))
# m = 3

url_owner = 'https://api.github.com/search/repositories?q=user:'+organization+'&sort=forks&order=desc'
page_index_owner = 1
page_item_owner = n
data_repo = fetch_driver("repo", n, url_owner, page_index_owner, page_item_owner)
repo_length = len(data_repo)
if repo_length < n:
    print "Only ", repo_length, " repositories found."
for i in data_repo:
    print 'Repository Name =', i['full_name']
    url_commits = 'https://api.github.com/repos/'+i['full_name']+'/contributors?'
    page_index_repo = 1
    page_item_repo = m
    data_contributors = fetch_driver('contributor', m, url_commits, page_index_repo, page_item_repo)
    contributors_length = len(data_contributors)
    if repo_length < n:
        print "Only ", contributors_length, " contributors found."
    for j in data_contributors[:m]:
        print "Top Contributor: ", j['login'], '/', "Total Contributions: ", j['contributions']