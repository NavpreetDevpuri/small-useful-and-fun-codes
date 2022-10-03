import os
import psycopg2
import json

with psycopg2.connect(
    host="localhost", database="design_studio", user="navpreetdevpuri"
) as conn:
    with conn.cursor() as cur:
        base_dir = os.path.dirname(__file__)
        json_files_dir = os.path.join(base_dir, "json_files")
        config_files_dir = os.path.join(base_dir, "config_files")
        json_file_names = os.listdir(json_files_dir)

        for json_file_name in json_file_names:
            curr_file_path = os.path.join(json_files_dir, json_file_name)
            with open(curr_file_path) as curr_file:
                json_data = json.load(curr_file)

            formated_data = []
            curr_json_file_config_path = os.path.join(
                config_files_dir, json_file_name)
            with open(curr_json_file_config_path) as curr_config_file:
                curr_config_file_data = json.load(curr_config_file)

            for entity in json_data:
                formated_entity = {}
                for key in curr_config_file_data["field_to_column_map"].keys():
                    if key in entity:
                        formated_entity[curr_config_file_data["field_to_column_map"]
                                        [key]] = entity[key]
                    else:
                        formated_entity[curr_config_file_data["field_to_column_map"][key]] = None
                formated_data.append(formated_entity)

            table_name = os.path.splitext(json_file_name)[0].lower()

            if curr_config_file_data["should_delete_old_table"]:
                cur.execute(f"DROP TABLE IF EXISTS {table_name}")

            cur.execute(curr_config_file_data["create_table_sql_query"])
            column_names = list(
                curr_config_file_data["field_to_column_map"].values())
            entity = formated_data[0]

            insert_query = f"""insert into {table_name} 
                                    ({",".join(column_names)}) 
                                values 
                                    (%s{",%s"*(len(column_names)-1)})"""
            values = []
            for entity in formated_data:
                value = []
                for key in curr_config_file_data["field_to_column_map"].values():
                    value.append(entity[key])
                values.append(value)

            cur.executemany(insert_query, values)
