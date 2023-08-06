import hashlib
import json
from io import BytesIO

import redis


def job_id(identifier: str) -> str:
    return "job:" + identifier


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
            self.redis.hset(job_id(identifier), mapping=job)
            self.redis.expire(job_id(identifier), 300)
            self.redis.rpush(queue_id, identifier)
        elif self.job_status(job_id(identifier)) == "FINISHED":
            self.redis.expire(job_id(identifier), 3600)
        return identifier

    def job_status(self, job_identifier):
        output = self.redis.hget(job_id(job_identifier), key="status")
        if output is not None:
            return output.decode()

    def queue(self, queue_id: str):
        return self.JobIterator(self.redis, queue_id)

    def fetch_job_result(self, job_identifier: str):
        job = self.redis.hgetall(name=job_id(job_identifier))
        if job and job[b'status'].decode() == "FINISHED":
            self.redis.expire(job_id(job_identifier), 900, gt=True)
            return BytesIO(job[b"data"])

    def job_not_exist(self, job_identifier: str):
        return not self.redis.exists(job_id(job_identifier))

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
    def __init__(self, redis_object, job_identifier):
        self.id = job_identifier
        self.redis = redis_object
        self.redis.hset(name=job_id(self.id), key="status", value="RUNNING")
        self.redis.expire(job_id(self.id), 120)

    def data(self):
        return json.loads(self.redis.hget(name=job_id(self.id), key="data").decode())

    def update_data(self, data: str):
        self.redis.hset(name=job_id(self.id), key="data", value=data)

    def enqueue(self, queue_id: str):
        pass

    def finish(self, job_result: BytesIO = None):
        job_result.seek(0)
        job_result_value = job_result.read()
        self.redis.expire(job_id(self.id), 3600)
        self.redis.hset(name=job_id(self.id), key="data", value=job_result_value)
        self.redis.hset(name=job_id(self.id), key="status", value="FINISHED")

    def fail(self):
        self.redis.hset(name=job_id(self.id), key="status", value="FAILED")
        self.redis.delete(job_id(self.id))

