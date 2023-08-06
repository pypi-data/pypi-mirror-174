from abc import ABC, abstractmethod
from psycopg2 import connect
from pymongo import MongoClient
from boto3 import client

from spt_factory.credentials import Credentials
from spt_factory.utils.s3_manager import S3Manager


class Resource(ABC):

    def __init__(self, c: Credentials):
        self.c = c

    @abstractmethod
    def get_object(self):
        pass

    @staticmethod
    @abstractmethod
    def get_name():
        pass


class Postgres(Resource):

    def get_object(self):
        return connect(**self.c.get_credentials())

    @staticmethod
    def get_name():
        return 'postgres'


class Greenplum(Resource):

    def get_object(self):
        return connect(**self.c.get_credentials())

    @staticmethod
    def get_name():
        return 'greenplum'


class Mongo(Resource):

    def get_object(self):
        return MongoClient(**self.c.get_credentials())

    @staticmethod
    def get_name():
        return 'mongo'


class Any:
    __slots__ = "creds"
    def __init__(self, creds):
        self.creds = creds
    def get_creds(self):
        return self.creds


class AnyCreds(Resource):

    def get_object(self):
        return Any(self.c.get_credentials())

    @staticmethod
    def get_name():
        return 'any_creds'


class S3ManagerResource(Resource):

    def get_object(self):
        return S3Manager(client(**self.c.get_credentials()))

    @staticmethod
    def get_name():
        return 's3_manager'
