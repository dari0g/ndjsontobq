from datetime import datetime, date

class NdjsonToBq:
    def __init__(self, ndjson_blob):
        self.ndjson_blob = ndjson_blob
        self.bq_schema = self.create_bq_schema(self.ndjson_blob)

    def create_bq_schema(self, data, parent_name="root"):
        schema = []

        for key, value in data.items():
            field_name = f"{parent_name}_{key}" if parent_name != "root" else key
            
            if isinstance(value, list):
                if len(value) > 0:
                    array_element_type = self.determine_field_type(value[0])
                    schema.append({"name": field_name, "type": "ARRAY", "fields": [{"name": "element", "type": array_element_type}]})
                else:
                    schema.append({"name": field_name, "type": "ARRAY", "fields": [{"name": "element", "type": "STRING"}]})
            elif isinstance(value, dict):
                nested_schema = self.create_bq_schema(value, field_name)  # Pass the nested dictionary and new parent name
                schema.append({"name": field_name, "type": "RECORD", "fields": nested_schema})
            else:
                field_type = self.determine_field_type(value)
                schema.append({"name": field_name, "type": field_type})

        return schema

    def determine_field_type(self, value):
        if value is None:
            return "STRING"
        elif isinstance(value, bool):
            return "BOOLEAN"
        elif isinstance(value, int):
            return "INTEGER"
        elif isinstance(value, float):
            return "FLOAT"
        elif isinstance(value, datetime):
            return "TIMESTAMP"
        elif isinstance(value, date):
            return "DATE"
        else:
            try:
                datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z") 
                return "TIMESTAMP"
            except ValueError:
                try:
                    datetime.strptime(value, "%Y-%m-%d")
                    return "DATE"
                except ValueError:
                    return "STRING"