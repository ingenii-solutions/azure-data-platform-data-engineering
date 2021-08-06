import json

from functions import *

with open("scratch/sftp_config.json", "r") as pipeline_file:
    full_config = json.load(pipeline_file)

sub_config = full_config["config"]

for table in full_config["tables"]:
    data_lake_path = full_config["name"] + "/" + table["name"]
    pipeline = DataFactoryPipeline(data_lake_path.replace("/", "-"))

    get_sftp_files = list_sftp_files(sub_config["url"], sub_config["username"],
                                    sub_config["key_vault_secret_name"], table["path"])
    find_all_raw_files = get_data_lake_files("raw", data_lake_path)
    find_all_archive_files = get_data_lake_files("archive", data_lake_path)

    pipeline.add_activity(get_sftp_files)
    pipeline.add_activity(find_all_raw_files)
    pipeline.add_activity(find_all_archive_files)

    find_raw_files = filter_for_files(find_all_raw_files)
    find_archive_files = filter_for_files(find_all_archive_files)

    pipeline.add_activity(find_raw_files, depends_on=[find_all_raw_files])
    pipeline.add_activity(find_archive_files, depends_on=[find_all_archive_files])

    move_files = move_new_files(get_sftp_files, find_raw_files, find_archive_files,
                                sub_config["url"], sub_config["username"],
                                sub_config["key_vault_secret_name"], table["path"],
                                data_lake_path)
    
    pipeline.add_activity(move_files, depends_on=[get_sftp_files, find_raw_files, find_archive_files])

    with open(f"scratch/{pipeline.pipeline_json['name']}.json", "w") as pipeline_file:
        json.dump(pipeline.pipeline_json, pipeline_file, indent=4)
