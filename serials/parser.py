from urllib import request
from urllib.request import Request
import re
from serials.models import *
from django.db.models import Max


def pars_site(url, parser, encoding='utf-8'):
    response = request.urlopen(url)
    if isinstance(parser, str):
        result = re.findall(parser, response.read().decode(encoding))
        return result


def pars_trakt_serials():
    parser = '<div class="grid-item[^$]*?<meta content="([^$]*?)"'
    urls = pars_site('https://trakt.tv/shows/trending', parser)
    for url in urls:
        pars_trakt_serial(url)


def pars_trakt_serial(url):
    response = request.urlopen(url).read().decode('utf-8')
    name = re.search(r'<meta property="og:title" content="([^$]*?)"', response).group(1)
    description = re.search(r'<meta property="og:description" content="([^$]*?)"', response).group(1)
    serial = Serial.objects.filter(name=name)
    if not serial:
        serial = Serial()
        serial.name = name
        serial.description = description
        serial.save()
        pars_trakt_seasons(url, serial)
        return
    else:
        serial = serial[0]
    episodes = []
    curr_index = response.find('<a class="watch-now"')
    while curr_index != -1:
        begin = response.rfind('<span class=\'main-title-sxe\'>', 0, curr_index)
        substr = response[begin:curr_index]
        num = re.search(r'(\d+)x(\d+)', substr)
        if num:
            episode_name = re.search(r'\'\d+\'>([^$]*?)</span></h3>', substr).group(1)
            episodes.append((episode_name, num.group(1), num.group(2)))
        curr_index = response.find('<a class="watch-now"', curr_index + 1)
    curr_order = serial.episode_set.aggregate(Max('order'))['order__max'] + 1
    for i in range(len(episodes) - 1, -1, -1):
        episode = serial.episode_set.filter(name=episodes[i][0])
        if not episode:
            episode = Episode()
            episode.serial = serial
            episode.name = episodes[i][0]
            episode.season = episodes[i][1]
            episode.order = curr_order
            episode.save()
            link = Link()
            link.episode = episode
            link.link = url + 'seasons/' + episodes[i][1] + '/episodes/' + episodes[i][2]
            link.save()
            curr_order += 1


def pars_trakt_seasons(url, serial):
    response = request.urlopen(url + '/seasons/all').read().decode('utf-8')
    curr_order = 1
    curr_index = response.find('<a class="watch-now"')
    while curr_index != -1:
        end = response.find('</span></a></h3>', curr_index)
        num = re.search(r'(\d+)x(\d+)', response[curr_index:end])
        if num:
            episode_name = response[response.rfind('>', curr_index, end) + 1:end]
            episode = Episode()
            episode.serial = serial
            episode.name = episode_name
            episode.season = num.group(1)
            episode.order = curr_order
            episode.save()
            link = Link()
            link.episode = episode
            link.link = url + 'seasons/' + num.group(1) + '/episodes/' + num.group(2)
            link.save()
            curr_order += 1
        curr_index = response.find('<a class="watch-now"', end)


def pars_watchseries_serials():
    req = Request('http://watchseries.cr/popular', headers={'User-Agent': 'Mozilla/5.0'})
    response = request.urlopen(req)
    parser = '<a href="([^"]*?)" class="videoHname title">'
    urls = re.findall(parser, response.read().decode('utf-8'))
    for url in urls:
        pars_watchseries_serial(url)


def pars_watchseries_serial(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = request.urlopen(req).read().decode('utf-8')
    name = re.search(r'<p style="font-size: 30px;">([^<]*?)</p>', response).group(1)
    serial = Serial.objects.filter(name=name)
    if not serial:
        return
    else:
        serial = serial[0]
    season_count = re.search(
        r'<a href="http://watchseries.cr/series/[^/]*?/season/(\d+)/episode/\d+" class="videoHname">',
        response).group(1)
    parser = '<a href="([^"]*?)" class="videoHname"><b>Episode \d+:</b> ([^<]*?)</a>'
    for i in range(1, int(season_count) + 1):
        req = Request(url + '/season/' + str(i), headers={'User-Agent': 'Mozilla/5.0'})
        response = request.urlopen(req).read().decode('utf-8')
        episodes = re.findall(parser, response)
        for epis in episodes:
            episode = serial.episode_set.filter(name=epis[1])
            if episode:
                link = episode[0].link_set.filter(link=epis[0])
                if not link:
                    link = Link()
                    link.episode = episode[0]
                    link.link = epis[0]
                    link.save()