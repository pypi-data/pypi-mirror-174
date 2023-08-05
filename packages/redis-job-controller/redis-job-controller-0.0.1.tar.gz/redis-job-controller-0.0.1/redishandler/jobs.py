import hashlib
import json

import redis


class JobManager:
    def __init__(self, host, port):
        self.redis = redis.Redis(host=host,
                                 port=port)

    def enqueue_job(self, job_data: dict, queue_id: str):
        identifier = hashlib.md5((json.dumps(job_data) + queue_id).encode('utf-8')).hexdigest()
        job = {"id": identifier, "data": job_data}
        job = json.dumps(job)
        self.redis.rpush(queue_id, job)
        return identifier

    def job_status(self, job_id):
        pass

    def queue(self, queue_id: str):
        return self.JobIterator(self.redis, queue_id)

    class JobIterator:
        def __init__(self, redis_object, queue_id):
            self.redis = redis_object
            self.queue_id = queue_id

        def __iter__(self):
            return self

        def __next__(self):
            job = None
            while job is None:
                job = self.redis.blpop(self.queue_id, 30)
            return json.loads(job[1])
