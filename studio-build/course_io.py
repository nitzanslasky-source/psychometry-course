import json
def load(path):
    s = open(path, encoding='utf-8').read()
    i = s.find('window.COURSE=') + len('window.COURSE='); j = s.find('</script>', i)
    return s, i, j, json.loads(s[i:j].rstrip().rstrip(';'))
