import redis
import json

stream_key = 'ST:TRACKER::::'

if __name__ == '__main__':
    # r = redis.Redis(host='localhost', port=6379, db=0)
    redis_dev = redis.Redis(host='10.61.228.218', port=6379, db=0, password='PiPaPo-2021.12')
    redis_local = redis.Redis(host='localhost', port=6379, db=0)
    while True:
        l = redis_dev.xread(count=1, block=5000, streams={stream_key: '$'})[-1][-1][-1][-1]
        # l = { key.decode(): val.decode() for key, val in l.items() }
        print(f"stream length: {redis_dev.xlen(stream_key)}")
        print(f"{redis_dev.xlen(stream_key)} - {type(l)} {l}")

        redis_local.xadd(stream_key, l)

# d = [b'ST:TRACKER::::', [(b'1664453926273-0',
#                           {b'url': b'https://www.rtl.lu/news/panorama/a/1972529.html?didomiConfig.notice.enable=false',
#                            b'uui': b'ipdigl5f9zzzs0q10k39ixfa',
#                            b'ua': b'Mozilla/5.0 (Linux; Android 12; SM-G996B Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/105.0.5195.136 Mobile Safari/537.36',
#                            b'lang': b'de-DE,de;q=0.9,fr-LU;q=0.8,fr;q=0.7,en-DE;q=0.6,en-US;q=0.5,en;q=0.4',
#                            b'dt': b'1664453925996'})]]
# print(type(d[-1][-1][-1]), d[-1][-1][-1])