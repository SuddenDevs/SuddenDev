import os
from redis import StrictRedis

if __name__ == '__main__':
    r = StrictRedis.from_url(os.getenv('REDIS_URL'))
    r.flushall()
