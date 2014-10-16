#!python
# Video Links Extractor from Coursera
# (c) Sergey Vinogradov, 2014
#
# similar projects:
# https://github.com/coursera-dl/coursera/tree/master/coursera - does the job, but seems too overcomplicated
# https://gist.github.com/macias/2880753 - doesn't have a pass->credentials convertion; written in php

import requests, re, os.path, sys

usage = """
  Usage: {0} user password 'coursera_class_url' [curl|text]
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
    for m in re.findall('.*?(Video \(MP4\) for[^<]+)<.*?data-modal-iframe="([^"]+)"', text):
        video_player_url = m[1].strip()
        r = session.get(video_player_url, headers = headers)
        assert r.ok, "Couldn't get video player page"

        repr(m[0].strip(), get_video_url(r.text))

def show_link_as_text(name, url):
    print "%s: %s" % (name, url)

def show_link_as_curl_commands(name, url):
    out_file = re.sub("[^a-zA-Z0-9_.,\[\]\(\)]", "_", name)
    extension = os.path.splitext(url)[1]
    if not out_file.endswith(extension):
        out_file += extension
    print "curl -C - -o '%s' '%s'" % (out_file, url)

def normalize_class_name(url):
    m = re.match(r"(?:https://)?(?:www\.)?(?:coursera\.org/course|class\.coursera\.org)/([^/]+)", url)
    assert m, "Please, pass a valid coursera URL"
    name = m.group(1)
    return name
    #r = requests.get('https://api.coursera.org/api/catalog.v1/courses')
    #assert r.ok, "Couldn't list all coursera courses via API"
    #print r.json()
    #quit();

if len(sys.argv) not in (4, 5):
    sys.stderr.write(usage)
    sys.exit(1)

user = sys.argv[1]
pwd = sys.argv[2]
class_name = normalize_class_name(sys.argv[3])
curl_or_text = 'curl' if len(sys.argv) == 4 else sys.argv[4]

(session, headers) = login(class_name, user, pwd)
get_link_pairs(class_name, session, headers, show_link_as_curl_commands if curl_or_text == 'curl' else show_link_as_text)
