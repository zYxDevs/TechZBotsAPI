import aiohttp


async def ud(word):
    requests = aiohttp.ClientSession()
    r = await requests.get(f"http://api.urbandictionary.com/v0/define?term={word}")
    r = await r.json()
    await requests.close()
    z = []
    for x in r['list']:
        z.append([x["thumbs_up"] - x["thumbs_down"]])
    z.sort()
    z.reverse()
    fuck = []
    for x in r['list']:
        if (x["thumbs_up"] - x["thumbs_down"]) == z[0][0]:
            fuck.append(x)

    resp = []
    for result in fuck:
        re = {}
        re['definition'] = result['definition']
        re['example'] = result['example']
        resp.append(re)

    return resp

