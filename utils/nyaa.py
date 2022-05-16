import aiohttp, feedparser
from bs4 import BeautifulSoup as bs


async def get_nyaa_info(code): 
  try:
    r = aiohttp.ClientSession()
    x = await r.get(f"https://nyaa.si/view/{code}")
    x = await x.text()
    s = bs(x, "html.parser")
    title = s.find_all("h3", attrs={"class":"panel-title"})[0]
    link = s.find_all("a", attrs={"class": "card-footer-item"})[0].get("href")
    d1 = s.find_all("div", attrs={"class":"col-md-1"})
    d2 = s.find_all("div", attrs={"class":"col-md-5"})
    title = str(title.string)
    title = title[4:]
    inf = []
    for t in d1:
      num = d1.index(t)
      t = t.string
      t = t[:-1]
      y = d2[num]
      if y.span:
        y = y.span.string
      elif y.a:
        y = y.a.string
      else:
        y = y.string
      sq = [t, y]
      inf.append(sq)
      try:
        if "Information" in t:
          inf.remove([t, y])
        else:
          pass
      except:
        pass
    graph = {}
    graph['success'] = "True"
    graph['title'] = title
    for a in inf:
      graph[f'{a[0]}'] = a[1]
    graph['magnet'] = link 
    return graph
  except Exception:
    return {
             "success": "False",
             "message": str(Exception)
      }

  

async def get_nyaa_latest():
  api_url = 'https://techzbotsapi.herokuapp.com'
  x = feedparser.parse("https://nyaa.si/?page=rss")
  x = x.entries[0]
  dic = {}
  
  
  code = str(x['link'])
  code = code.split('/')[-1]
  code = code.split('.')[0]
  requests = aiohttps.ClientSession()
  resp = await requests.get(f'{api_url}/nyaa?code={code}')
  magnet = await resp.json()
  magnet = magnet['magnet']
  await requests.close()
  
  dic['success'] = true
  dic['title'] = x['title']
  dic['magnet'] = magnet
  dic['seeders'] = x['nyaa_seeders']
  dic['leechers'] = x['nyaa_leechers']
  dic['downloads'] = x['nyaa_downloads']
  dic['infohash'] = x['nyaa_infohash']
  dic['category'] = x['nyaa_category']
  dic['size'] = x['nyaa_size']
  return dic
