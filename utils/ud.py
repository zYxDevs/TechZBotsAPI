import aiohttp


async def ud(word):
   requests = aiohttp.ClientSession()
   
   r = await requests.get(f"http://api.urbandictionary.com/v0/define?term={word}")
   r = await r.json()
   await requests.close()
   results = []
   for defin in r['list']:
     results.append([defin["thumbs_up"] - defin["thumbs_down"]])
   
   resp = []


   results.sort()
   results.reverse()

   res = []
   for result in r:
     if (result['thumbs_up'] - result['thumbs_down']) == results[0][0]:
       res.append(result)
     else:
       pass
   
   for result in res:
     res = {}
     res['definition'] = result['definition']
     res['example'] = result['example']
     resp.append(res)

   return resp
