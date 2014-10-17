#!python
# Video Links Extractor from Coursera
# (c) Sergey Vinogradov, 2014
#
# similar projects:
# https://github.com/coursera-dl/coursera - does the job, but seems too overcomplicated
# https://gist.github.com/macias/2880753 - doesn't have a pass->credentials convertion; written in php

import requests, re, os.path, sys

usage = """
  Usage: {0} user password 'coursera_class_url' [curl(default)|text|csv|urls]
  Example:  {0} user@mail.com 'SuperPass!#$%' 'https://www.coursera.org/course/hwswinterface' curl
  Example2: {0} user@mail.com 'SuperPass!#$%' 'https://class.coursera.org/digitalmedia-002/lecture/79' text
""".format("python " + sys.argv[0])

def login(class_name, user, pwd):
    session = requests.Session()

    # get token
    r = requests.get("https://class.coursera.org/" + class_name, allow_redirects=False)
    assert r.ok, "Couldn't find coursera's class URL"
    csrftoken = r.cookies.get('csrf_token', None)
    assert csrftoken, "Wrong cookie received from coursera - no csrf_token inside"

    headers = {
        'Cookie': 'csrftoken=' + csrftoken,
        'Referer': 'https://accounts.coursera.org/signin',
        'X-CSRFToken': csrftoken,
    }

    # pass auth for token
    r = session.post("https://accounts.coursera.org/api/v1/login", 
                     data={'email': user, 'password': pwd, 'webrequest':'true'},
                     headers=headers, allow_redirects=False)
    assert r.ok, "Couldn't login to Coursera"
    
    return (session, headers)

def get_link_pairs(class_name, session, headers, repr):
    def get_video_url(text):
        text = text.replace("\n", " ").replace("\r", "")
        m = re.search('<source type="video/mp4" src="([^"]+)">', text)
        assert m.group(1), "Couldn't extract mp4 link from video player page"
        return m.group(1)

    r = session.get('https://class.coursera.org/%s/lecture' % class_name, headers=headers)
    text = r.text.replace("\n", " ").replace("\r", "")
    
    found_links = 0
    for m in re.findall('.*?(Video \(MP4\) for[^<]+)<.*?data-modal-iframe="([^"]+)"', text):
        video_player_url = m[1].strip()
        r = session.get(video_player_url, headers = headers)
        assert r.ok, "Couldn't get video player page"
        
        found_links += 1
        repr(m[0].strip(), get_video_url(r.text))
    return found_links

def show_link_as_text(name, url):
    print "%s: %s" % (name, url)

def show_link_as_urls(name, url):
    print url

csv_first_line = True
def show_link_as_csv(name, url):
    global csv_first_line
    if csv_first_line:
        print "name,url"
        csv_first_line = False;
    print "%s,%s" % (name.replace(",", ";"), url)

def show_link_as_curl(name, url):
    out_file = re.sub("[^a-zA-Z0-9_.,\[\]\(\)]", "_", name)
    extension = os.path.splitext(url)[1]
    if not out_file.endswith(extension):
        out_file += extension
    print "curl -C - -o '%s' '%s'" % (out_file, url)

def normalize_class_name(url):
    def name_from_url(url):
        m = re.match(r"(?:https://)?(?:www\.)?(?:coursera\.org/course|class\.coursera\.org)/([^/]+)", url)
        assert m, "Please, pass a valid coursera URL"
        return m.group(1)

    name = name_from_url(url)
    if '-' in name:
        return [name]

    # search sessions for given class
    name = "/" + name + "-"
    r = requests.get('https://api.coursera.org/api/catalog.v1/sessions')
    assert r.ok and r.json().get('elements', None), "Couldn't list all coursera classes via API"
    all_classes = r.json()['elements']
    ids = []
    for session in all_classes:
        if name in session['homeLink']:
            ids.append([session['id'], session['homeLink']])
    assert len(ids) > 0, "Couldn't find session of a selected class"
        
    # build a list of sessions in latest-oldest order
    ids.sort(key = lambda e: e[0], reverse = True)
    names = map(lambda e: name_from_url(e[1]), ids)
    return names

if len(sys.argv) not in (4, 5):
    sys.stderr.write(usage)
    sys.exit(1)

user = sys.argv[1]
pwd = sys.argv[2]
class_names = normalize_class_name(sys.argv[3])
curl_or_text = 'curl' if len(sys.argv) == 4 else sys.argv[4]
visualizer = {'curl': show_link_as_curl, 
              'text': show_link_as_text,
              'csv': show_link_as_csv,
              'urls': show_link_as_urls}.get(curl_or_text, show_link_as_curl)

for class_name in class_names:
    (session, headers) = login(class_name, user, pwd)
    if get_link_pairs(class_name, session, headers, visualizer) > 0:
        break
