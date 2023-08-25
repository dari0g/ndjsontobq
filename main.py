from NdjsonToBq import NdjsonToBq
# Sample NDJSON dictionary
ndjson_data = {
    "name": "Dario",
    "birth_date": "1993-08-25T00:00:00Z",
    "registration_date": "2022-03-15T08:00:00Z",
    "contact": {
        "email": "dario@example.com",
        "phone": "123-456-7890",
        "address": {
            "street": "123 Main St",
            "city": "Miami",
            "state": "FL"
        }
    }
}


# Create an instance of NdjsonToBq
converter = NdjsonToBq(ndjson_data)

# Access the generated BigQuery schema
print(converter.bq_schema)