import json
import sys
import boto3
import logging

# from pathlib import Path
# import shutil
# import sys
import uuid

logging.basicConfig(level=logging.INFO)

class DataLake():
    """
    Data Lake Utils
    This class instanciates an object to handle read/write operations on an 
    specific bucket on Amazon S3 working as a Data Lake, with folders splitted
    into the following hierarchy:
    - schema/
        - table/
            - partition[0]/
                - partition[1]/
                    ...
                        - partition[n]/
                            - object
    .
    """

    def __init__(self, bucket_name: str, schema: str, table: str, partitions: list, profile_name : str = None):
        """
        Constructor method

        :bucket_name: name of Amazon S3 bucket
        :schema: name of schema
        :table: name of table
        :partitions: list of key/value pairs of partitions to be used
        :return: void
        """
        if profile_name is None:
            self.session = boto3.Session()
        else:
            self.session = boto3.Session(profile_name=profile_name)
            
        self.bucket_name = bucket_name
        self.schema = schema
        self.table = table
        self.partitions = partitions
        self.object_name_prefix = self.__concat_object_name_prefix()

    def __concat_object_name_prefix(self):
        object_partitions = "/".join("{0}={1}".format(
            partition["key"], partition["value"]) for partition in self.partitions)
        object_name_prefix = "{0}/{1}/{2}/".format(
            self.schema,
            self.table,
            object_partitions
        )
        # Object name returned already has a slash '/' at the end of string
        return object_name_prefix

    def append_to_s3(self, data):
        insert_count = len(data)
        
        if insert_count == 0:
            logging.info("NO DATA TO BE INSERTED")
            return
        
        object_name = self.object_name_prefix + str(uuid.uuid1()) + ".json"
        
        data = "\n".join(json.dumps(item) for item in data)
        
        logging.info("INSERTING DATA INTO S3...")
        try:
            s3 = self.session.client('s3')
            s3.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=bytes(data, "utf-8")
                )
        except:
            raise
        else:
            logging.info("{0} RECORDS INSERTED INTO S3".format(insert_count))
            logging.info("(+) {0}".format(object_name))
            
    def delete_from_s3(self):
        logging.info("DELETING DATA FROM S3 IF EXISTS...")
        objects_to_delete = {'Objects': []}
        try:
            s3 = self.session.client('s3')
            objects = s3.list_objects(
                Bucket=self.bucket_name,
                Prefix=self.object_name_prefix)
        except:
            raise
        else:
            if objects.get('Contents') is not None:
                objects_to_delete['Objects'] = [{'Key': k} for k in [
                    obj['Key'] for obj in objects.get('Contents', [])]]
                s3.delete_objects(
                    Bucket=self.bucket_name,
                    Delete=objects_to_delete)
            
                delete_count = len(objects_to_delete["Objects"])
                logging.info("{0} FILES DELETED FROM S3".format(delete_count))
                
                for item in objects_to_delete["Objects"]:
                    logging.info("(-) {0}".format(item["Key"]))
            else:
                logging.info("NO FILES TO BE DELETED FROM S3")

    def read_from_s3(self):
        logging.info("READING DATA FROM S3...")
        try:
            s3 = self.session.client('s3')
            objects = s3.list_objects(
                Bucket=self.bucket_name,
                Prefix=self.object_name_prefix)
        except:
            raise
        else:
            if objects.get('Contents') is not None:
                data = []
                for object in objects.get('Contents'):
                    logging.info(object.get('Key'))

                    content = s3.get_object(
                        Bucket=self.bucket_name,
                        Key=object.get('Key'))
                    content = content['Body'].read().splitlines()
                    
                    for line in content:
                        data += (json.loads(line.decode("utf-8")),)
                
                read_count = len(data)
                logging.info("{0} RECORDS READ FROM S3".format(read_count))
                return data
            else:
                logging.info("NO DATA WAS FOUND ON S3. ABORTING...")
                sys.exit(0)
