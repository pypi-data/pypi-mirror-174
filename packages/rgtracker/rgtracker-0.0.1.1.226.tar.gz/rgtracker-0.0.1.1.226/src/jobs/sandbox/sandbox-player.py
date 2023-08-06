from rgtracker.record import *
from rgtracker.tracker import *
from rgtracker.common import *
from rgtracker.website import *
from rgtracker.section import *
from rgtracker.page import *
from rgtracker.device import *
from rgtracker.pageviews import *

# from redis import Redis
#
# redis_dev = Redis(host="10.61.228.218", port=6379, password='PiPaPo-2021.12')
# redis_local = Redis(host="localhost", port=6379)
#
# player_data = redis_dev.xrange('ST:PLAYER::::', 1663767601740, 1663767808901)
#
# for pd in player_data:
#     redis_local.xadd('ST:PLAYER::::', pd[1])
#     print(f'XADD ST:PLAYER:::: {pd[1]}')

# foreach(lambda record: log(f'{record}')). \
# foreach(lambda record: execute('TOPK.ADD', 'topk', {record.value.url})). \
GB("StreamReader"). \
    foreach(lambda record: execute('TOPK.ADD', 'topk', {record.get('value').get('url')})). \
    run('ST:PLAYER::::', trimStream=False)
# run('ST:PLAYER::::', trimStream=False, fromId="1663766604999")

# gears-cli run --host localhost --port 6379 src/jobs/sandbox/sandbox-player.py
