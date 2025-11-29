# an example of client interface to put item into the table
from boto3.dynamodb.conditions import Attr
from boto3.dynamodb.conditions import Key
import boto3

dynamodb = boto3.client("dynamodb")

dynamodb.put_item(
    TableName="AdoptionApplications",
    Item={
        "pet_id": {"S": "764388af-8c95-411c-81d3-7b2d07ba5c78"},
        "submission_time": {"S": "2025-04-02T21:08:04.533Z"},
        "applicant_name": {"S": "Ana Carolina Silva"},
        "has_children": {"BOOL": "true"},
        "number_of_pets": {"N": "1"},
        # ... more attributes ...
    },
)


# creating table:


resource = boto3.resource("dynamodb", region_name="us-east-1")


def create_adoption_table(table_name):
    table = resource.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "pet_id", "KeyType": "HASH"},
            {"AttributeName": "submission_time", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "pet_id", "AttributeType": "S"},
            {"AttributeName": "submission_time", "AttributeType": "S"},
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )

    print("Creating table...")
    table.wait_until_exists()
    print(f"Table {table_name} is ready!")


# Call the function
create_adoption_table("AdoptionEvent")


# Describing table:


client = boto3.client("dynamodb", region_name="us-east-1")
response = client.describe_table(TableName="PetStoreAppointments")
print(response)


# getting a list of tables:


client = boto3.client("dynamodb", region_name="us-east-1")
response = client.list_tables()
print(response)


"""""CRUD Operations:"""

# PutItem (Create)

# Create a single appointment.

resource = boto3.resource("dynamodb", region_name="us-east-1")
table_name = "PetStoreAppointments"
table = resource.Table(table_name)

table.put_item(
    Item={
        "appointment_id": "11",
        "pet_name": "Gordon",
        "owner": "Jane Doe",
        "service": "Deluxe grooming",
        "date": "2025-03-26",
    }
)
print("Appointment created successfully.")

# BatchWriteItem (Create Multiple)

# Create multiple appointments.

appointments = [
    {
        "appointment_id": "1",
        "pet_name": "Buddy",
        "owner": "Alice",
        "service": "Haircut",
        "date": "2025-04-01",
    },
    {
        "appointment_id": "2",
        "pet_name": "Whiskers",
        "owner": "Bob",
        "service": "Nail Trim",
        "date": "2025-04-01",
    },
    {
        "appointment_id": "3",
        "pet_name": "Rex",
        "owner": "Charlie",
        "service": "Bath",
        "date": "2025-04-02",
    },
]

resource = boto3.resource("dynamodb", region_name="us-east-1")
table_name = "PetStoreAppointments"

table = resource.Table(table_name)
with table.batch_writer() as batch:
    for appointment in appointments:
        batch.put_item(Item=appointment)
print("Multiple appointments created successfully.")

# GetItem (Read)

# Read a single appointment.

resource = boto3.resource("dynamodb", region_name="us-east-1")
table_name = "PetStoreAppointments"
table = resource.Table(table_name)
response = table.get_item(Key={"appointment_id": "1"})
print(response)
print("Appointment retrieved successfully.")

# BatchGetItem (Read Multiple)


resource = boto3.resource("dynamodb", region_name="us-east-1")
table_name = "PetStoreAppointments"

response = resource.batch_get_item(
    RequestItems={
        table_name: {
            "Keys": [
                {"appointment_id": "1"},
                {"appointment_id": "2"},
                {"appointment_id": "3"},
            ]
        }
    }
)

print(response["Responses"])
print("Multiple appointments retrieved successfully.")

# Query (Read with Condition) and Scan


resource = boto3.resource("dynamodb", region_name="us-east-1")
table_name = "PetStoreAppointments"
table = resource.Table(table_name)

response = table.query(KeyConditionExpression=Key("appointment_id").eq("1"))
print(response)


resource = boto3.resource("dynamodb", region_name="us-east-1")
table_name = "PetStoreAppointments"
table = resource.Table(table_name)

response = table.scan(FilterExpression=Attr("service").eq("Deluxe grooming"))
print(response["Items"])


# UpdateItem (Update)


resource = boto3.resource("dynamodb", region_name="us-east-1")
table_name = "PetStoreAppointments"
table = resource.Table(table_name)

response = table.update_item(
    Key={"appointment_id": "1"},
    UpdateExpression="SET service = :s",
    ExpressionAttributeValues={":s": "Deluxe grooming"},
    ReturnValues="UPDATED_NEW",
)

print(response)


# DeleteItem (Delete)


resource = boto3.resource("dynamodb", region_name="us-east-1")
table_name = "PetStoreAppointments"
table = resource.Table(table_name)

response = table.delete_item(Key={"appointment_id": "1"})
print("Appointment deleted: ", response)
