from io import BytesIO

import redis


class RedisRepository:
    def __init__(self, host, port):
        self.redis = redis.Redis(host=host,
                                 port=port)

    def fetch_job_result(self, job_id):
        item = self.redis.get(job_id)
        if not item:
            raise KeyError()
        return BytesIO(item)

    def store_job_result(self, job_result, job_id):
        job_result.seek(0)
        job_result_value = job_result.read()
        self.redis.set(job_id, job_result_value)

    def __setitem__(self, key, value):
        self.redis.set(key, value)

    def __delitem__(self, key):
        self.redis.delete(key)


class MapRepository:
    def __init__(self):
        self.content = {}

    def fetch_job_result(self, job_id):
        mem = self.content[job_id]
        mem.seek(0)
        return mem

    def store_job_result(self, job_result, job_id):
        self.content[job_id] = job_result

    def __setitem__(self, key, value):
        self.content[key] = value

    def __delitem__(self, key):
        self.content.__delitem__(key)
