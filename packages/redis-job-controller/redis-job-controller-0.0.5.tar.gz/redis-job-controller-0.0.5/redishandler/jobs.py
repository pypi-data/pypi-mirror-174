import hashlib
import json
from io import BytesIO

import redis


class JobManager:
    def __init__(self, host, port):
        self.redis = redis.Redis(host=host,
                                 port=port)

    def enqueue_job(self, job_data: dict, queue_id: str, identifier: str = None):
        data_json = json.dumps(job_data)
        if identifier is None:
            identifier = self.generate_job_id(data_json, queue_id)
        if self.job_not_exist(identifier):
            job = {"id": identifier, "data": data_json, "status": "PENDING", "queue": queue_id}
            self.redis.hset("job:" + identifier, mapping=job)
            self.redis.rpush(queue_id, identifier)
        return identifier

    def job_status(self, job_id):
        return self.redis.hget(name="job:" + job_id, key="status").decode()

    def queue(self, queue_id: str):
        return self.JobIterator(self.redis, queue_id)

    def fetch_job_result(self, job_id: str):
        job = self.redis.hgetall(name="job:" + job_id)
        if job and job[b'status'].decode() == "FINISHED":
            return BytesIO(job[b"data"])

    def job_not_exist(self, job_id: str):
        return not self.redis.hgetall("job:" + job_id)

    @classmethod
    def generate_job_id(cls, job_data: str, queue_id: str = ""):
        return hashlib.md5((job_data + queue_id).encode('utf-8')).hexdigest()

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
            return Job(self.redis, job[1].decode())


class Job:
    def __init__(self, redis_object, job_id):
        self.id = job_id
        self.redis = redis_object
        self.redis.hset(name="job:" + job_id, key="status", value="RUNNING")

    def data(self):
        return json.loads(self.redis.hget(name="job:" + self.id, key="data").decode())

    def update_data(self, data: str):
        self.redis.hset(name="job:" + self.id, key="data", value=data)

    def enqueue(self, queue_id: str):
        pass

    def finish(self, job_result: BytesIO = None):
        job_result.seek(0)
        job_result_value = job_result.read()
        self.redis.hset(name="job:" + self.id, key="data", value=job_result_value)
        self.redis.hset(name="job:" + self.id, key="status", value="FINISHED")

    def fail(self):
        self.redis.hset(name="job:" + self.id, key="status", value="FAILED")
