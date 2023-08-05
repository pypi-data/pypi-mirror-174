DataLakeUtils
    This class instanciates an object to handle read/write operations on an 
    specific bucket on Amazon S3 working as a Data Lake, with folders splitted
    into the following hierarchy, compatible to Apache Hadoop filesystem:
    - schema/
        - table/
            - partition[0]/
                - partition[1]/
                    ...
                        - partition[n]/
                            - object