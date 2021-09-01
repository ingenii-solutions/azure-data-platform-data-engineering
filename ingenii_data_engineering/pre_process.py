import csv
import json
from os import makedirs, path
from shutil import move

from .dbt_schema import get_all_sources

all_sources = get_all_sources("/".join(["", "dbfs", "mnt", "dbt"]))

class PreProcess:
    def __init__(self, data_provider: str, table: str, file_name: str,
                 development: bool = False):
        self.data_provider = data_provider
        self.table = table
        self.file_name = file_name

        self.table_details = all_sources[data_provider]["tables"][table]

        self.development = development

        if development:
            # Will move to a folder in the same location the file is in now
            self.write_folder = "/".join(self.file_name.split("/")[:-1]) or "."
            self.archive_folder = self.write_folder + "/before_pre_process"

            self.file_name = self.file_name.split("/")[-1]
        else:
            # Move to the correct container location
            self.write_folder = "/" + "/".join([
                "dbfs", "mnt", "raw", self.data_provider, self.table])
            self.archive_folder = "/" + "/".join([
                "dbfs", "mnt", "archive", self.data_provider, self.table, "before_pre_process"])

        if not path.exists(self.archive_folder):
            makedirs(self.archive_folder)
        
        if not path.exists(self.get_write_path()) and not path.exists(self.get_raw_path()):
            raise Exception(
                f"Unable to find file at {self.get_write_path()} or {self.get_raw_path()} to process!"
            )

        if not path.exists(self.get_raw_path()):
            move(self.get_write_path(), self.get_raw_path())
        

    def get_raw_path(self):
        return self.archive_folder + "/" + self.file_name

    def get_write_path(self, new_file_name=None):
        if new_file_name:
            return self.write_folder + "/" + new_file_name
        else:
            return self.write_folder + "/" + self.file_name

    def get_filename_no_extension(self):
        return ".".join(self.file_name.split(".")[:-1])

    def get_raw_file(self):
        with open(self.get_raw_path(), "r") as raw_file:
            return raw_file.read()

    def get_raw_file_by_line(self):
        with open(self.get_raw_path(), "r") as raw_file:
            for line in raw_file.readlines():
                yield line

    def get_file_as_json(self):
        with open(self.get_raw_path(), "r") as jsonfile:
            return json.load(jsonfile)

    def get_table_fields(self, json_list):
        known_columns = set()
        for ind_json in json_list:
            known_columns.update(ind_json.keys())

        schema_column_names = \
            [c["name"].strip("`") for c in self.table_details["columns"]]
        missing_fields = [f for f in known_columns 
                          if f not in schema_column_names]
        if missing_fields:
            raise Exception(
                f"Columns in file not in schema! {missing_fields}. "
                f"Schema columns: {schema_column_names}, "
                f"file columns: {known_columns}")

        return schema_column_names

    def write_json_to_csv(self, json_to_write, new_file_name=None,
                          write_header=True, **kwargs):
        with open(self.get_write_path(new_file_name), "w") as result:

            writer = csv.DictWriter(
                result,
                fieldnames=self.get_table_fields(json_to_write),
                **kwargs)

            if write_header:
                writer.writeheader()

            for entry in json_to_write:
                writer.writerow(entry)
  
    def write_json(self, json_to_write, new_file_name=None, **kwargs):
        with open(self.get_write_path(new_file_name), "w") as result:
            for ind_json in json_to_write:
                json.dump(ind_json, result, **kwargs)
                result.write("\n")
