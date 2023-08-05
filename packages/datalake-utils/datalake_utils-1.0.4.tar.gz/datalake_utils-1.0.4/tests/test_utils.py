from datalake_utils.utils import DataLake
import json

data = [
    {
        "brand": "Ford",
        "model": "Mustang",
        "year": 1965
    },
    {
        "brand": "Pontiac",
        "model": "GTO",
        "year": 1964
    },
    {
        "brand": "Lamborghini",
        "model": "Miura",
        "year": 1966
    }
]

s3 = DataLake(
    bucket_name="yuca-data-development-landing-zone",
    schema="motor_vehicles",
    table="cars",
    partitions=[
        {
            "key": "logical_date",
            "value": "2022-01-01"
        },
        {
            "key": "decade",
            "value": "1960s"
        }
    ],
)

s3.append_to_s3(data)

retrieved_data = s3.read_from_s3()
print(json.dumps(retrieved_data, indent=4))

s3.delete_from_s3()
