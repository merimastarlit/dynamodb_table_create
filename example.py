import boto3
import uuid
import boto3.dynamodb.conditions import Key

resource = boto3.resource("dynamodb", region_name="us-east-1")
table_name = "PetStoreAppointments"
table = resource.Table(table_name)


def create_appointment():
    print("New Grooming Appointment")
    pet_name = input("Enter pet name:")
    owner = input("Owner's name")
    service = input("Type of service")
    date = input("Enter date in (MM:DD:YYYY)")

    appoinment_id = str(uuid.uuid4())

    item - {
        "appointment_id": appoinment_id,
        "pet_name": pet_name,
        "owner": owner,
        "service": service,
        "date": date
    }

    table.put_item(Item=item)
    print('Appointment created')
