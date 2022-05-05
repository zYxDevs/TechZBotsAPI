import aiohttp


async def ud(word):
   requests = aiohttp.ClientSession()
   
   r = await requests.get(f"http://api.urbandictionary.com/v0/define?term={word}")
   r = await r.json()
   z = []
   for x in r['list']:
     z.append([x["thumbs_up"] - x["thumbs_down"], [x]])
   
   hm = []
   for x in z:
     for a in z:
       if x[0] >= a[0]:
         z.remove(a)
       else:
         pass
   
   for a in z:
     a = a[1][0]
     at = {}
     at['definition'] = a['definition']
     at['example'] = a['example']
     hm.append(at)

   return hm
