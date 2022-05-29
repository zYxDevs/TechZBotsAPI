import aiohttp
from bs4 import BeautifulSoup as bs
  
  
YTS_URI = "https://yts.ng/search?search={}"


async def yts(query):
  requests = aiohttp.ClientSession()
  
  query = query.replace(" ", "+")
  
  try:
    
    x = await requests.get(YTS_URI.format(query))
  
    res = await x.text()
  
    soup = bs(res, "html.parser")
  
    pri =  soup.find_all("div", attrs={"class":"product_info"})
  
  #Here pri is list of search results
  
    links = []
  
    for x in pri:
      nam = x.img.get("alt") 
    
    #name of result
    
      link = x.get("onclick")
    
    #link to post
    
      link = str(link).split("'")[1]
    
    #getting true link 
    
      r = await requests.get(link)
    
      resp = await r.text()
    
      soup = bs(resp, "html.parser")
    
      po =  soup.find_all("a", attrs={"class":"magnet-download download-torrent magnet"}) 
    
      #Here po is magnet
      
      ma = soup.find_all("a",attrs={"class":"downloadbtn"})
    
      #Here ma is quality
      
      magnets = []
      
      for a in po:
        
        m = ma[po.index(a)]
    
        #creating results of each magnet link
  
        json = {"quality":(str(m).replace("\t", "").split("\n")[1]).replace(" ", ""), "magnet":a.get("href")}
        
        magnets.append(json)
    
      # adding magnets to thier respective dicts
    
        l = {"name": nam, "magnets": magnets}
        links.append(l)
        
    #closing aiohttp connection

    await requests.close()
 
    return links
    
  except:
    
    return None
