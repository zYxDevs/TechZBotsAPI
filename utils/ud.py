import aiohttp


async def ud(word):
   requests = aiohttp.ClientSession()
   
   r = await requests.get(f"http://api.urbandictionary.com/v0/define?term={word}")
   r = await r.json()
   await requests.close()
   results = []
   for defin in r['list']:
     results.append([defin["thumbs_up"] - defin["thumbs_down"], defin])
   
   resp = []


   for result in results:
     for res in results:
       if result[0] >= res[0]:
         results.remove(res)
       else:
         pass
   
   for result in results:
     for res in results:
       if result[0] >= res[0]:
         results.remove(res)
       else:
         pass
   
   for result in results:
     result = result[1]
     res = {}
     res['definition'] = result['definition']
     res['example'] = result['example']
     resp.append(res)

   return resp
