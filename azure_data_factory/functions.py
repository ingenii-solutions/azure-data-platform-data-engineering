default_policy = {
    "timeout": "0.00:01:00",
    "retry": 3,
    "retryIntervalInSeconds": 30,
    "secureOutput": False,
    "secureInput": False
}


def list_sftp_files(host_url, username, key_vault_secret_name, folder_path):
    return {
        "name": f"List files at {host_url}/{folder_path}".replace("https://", "").replace("http://", "").replace("/", "-"),
        "type": "GetMetadata",
        "dependsOn": [],
        "policy": default_policy,
        "userProperties": [],
        "typeProperties": {
            "dataset": {
                "referenceName": "SFTPFolder",
                "type": "DatasetReference",
                "parameters": {
                    "Host": host_url,
                    "UserName": username,
                    "KeyVaultSecretName": key_vault_secret_name,
                    "FolderPath": folder_path
                }
            },
            "fieldList": [
                "childItems"
            ],
            "storeSettings": {
                "type": "SftpReadSettings",
                "recursive": True,
                "enablePartitionDiscovery": False
            },
            "formatSettings": {
                "type": "BinaryReadSettings"
            }
        }
    }


def get_data_lake_files(container, path):
    return {
        "name": f"List current {container}/{path} files".replace("/", "-"),
        "type": "GetMetadata",
        "dependsOn": [],
        "policy": default_policy,
        "userProperties": [],
        "typeProperties": {
            "dataset": {
                "referenceName": "DataLakeFolder",
                "type": "DatasetReference",
                "parameters": {
                    "Container": container,
                    "FolderPath": path,
                }
            }
        },
        "fieldList": [
            "childItems"
        ],
        "storeSettings": {
            "type": "AzureBlobFSReadSettings",
            "recursive": True,
            "enablePartitionDiscovery": False
        },
        "formatSettings": {
            "type": "BinaryReadSettings"
        }
    }


def filter_for_files(output_activity):
    return {
        "name": f"Only files from {output_activity['name']}",
        "type": "Filter",
        "dependsOn": [
            {
                "activity": output_activity["name"],
                "dependencyConditions": [
                    "Succeeded"
                ]
            }
        ],
        "userProperties": [],
        "typeProperties": {
            "items": {
                "value": f"@activity('{output_activity['name']}').output.childItems",
                "type": "Expression"
            },
            "condition": {
                "value": "@equals(item().type, 'File')",
                "type": "Expression"
            }
        }
    }


def move_new_files(source_activity: dict, raw_list_activity: dict, archive_list_activity: dict,
                   host_url, username, key_vault_secret_name, folder_path, data_lake_folder_path):
    return {
        "name": "For each found file",
        "type": "ForEach",
        "dependsOn": [
            {
                "activity": activity["name"],
                "dependencyConditions": [
                    "Succeeded"
                ]
            }
            for activity in [source_activity, raw_list_activity, archive_list_activity]
        ],
        "userProperties": [],
        "typeProperties": {
            "items": {
                "value": f"@activity('{source_activity['name']}').output.childItems",
                "type": "Expression"
            },
            "activities": [
                {
                    "name": "If new file",
                    "type": "IfCondition",
                    "dependsOn": [],
                    "userProperties": [],
                    "typeProperties": {
                        "expression": {
                            "value": f"@not(or(contains(activity('{raw_list_activity['name']}').output.childItems, item()), contains(activity('{archive_list_activity['name']}').output.childItems, item())))",
                            "type": "Expression"
                        },
                        "ifTrueActivities": [
                            {
                                "name": "Move file to raw",
                                "type": "Copy",
                                "dependsOn": [],
                                "policy": default_policy,
                                "userProperties": [],
                                "typeProperties": {
                                    "source": {
                                        "type": "BinarySource",
                                        "storeSettings": {
                                            "type": "SftpReadSettings",
                                            "recursive": False,
                                            "deleteFilesAfterCompletion": False
                                        },
                                        "formatSettings": {
                                            "type": "BinaryReadSettings"
                                        }
                                    },
                                    "sink": {
                                        "type": "BinarySink",
                                        "storeSettings": {
                                            "type": "AzureBlobFSWriteSettings"
                                        }
                                    },
                                    "enableStaging": False
                                },
                                "inputs": [
                                    {
                                        "referenceName": "SFTPFile",
                                        "type": "DatasetReference",
                                        "parameters": {
                                            "Host": host_url,
                                            "UserName": username,
                                            "KeyVaultSecretName": key_vault_secret_name,
                                            "FolderPath": folder_path,
                                            "FileName": {
                                                "value": "@item().name",
                                                "type": "Expression"
                                            },
                                        }
                                    }
                                ],
                                "outputs": [
                                    {
                                        "referenceName": "DataLakeFolder",
                                        "type": "DatasetReference",
                                        "parameters": {
                                            "Container": "raw",
                                            "FolderPath": data_lake_folder_path
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        }
    }


class DataFactoryPipeline:
    def __init__(self, name):
        self.pipeline_json = {
            "name": name,
            "properties": {
                "activities": [],
                "parameters": {},
                "variables": {},
                "annotations": []
            }
        }

    def add_activity(self, activity_json, depends_on=[]):
        activity_json["dependsOn"] = [
            {
                "activity": activity["name"],
                "dependencyConditions": [
                    "Succeeded"
                ]
            }
            for activity in depends_on
        ]
        self.pipeline_json["properties"]["activities"].append(activity_json)
