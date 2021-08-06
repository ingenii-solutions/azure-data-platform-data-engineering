## dbt

Part of this package validates dbt schemas to ensure they are compatible with Databricks and the larger Ingenii Data Platform.

In your Azure DevOps data engineering repository, a dbt project should be in the `dbt` folder. This is where we draw information about the data sources and the data quality tests to apply, and as part of the CI/CD process will be made available to the Databricks environment.
All data we want the platform to know about should be recorded as [dbt sources](https://docs.getdbt.com/docs/building-a-dbt-project/using-sources), where we specify each of the tables and their schemas in one or more `schema.yml` file. An example file would be

```
version: 2

sources:
  - name: random_example
    schema: random_example
    tables:
      - name: alpha
        external:
          using: "delta"
        join:
          type: merge
          column: "date"
        file_details:
          sep: ","
          header: false
          dateFormat: dd/MM/yyyy
        columns:
          - name: date
            data_type: "date"
            tests: 
              - unique
              - not_null
          - name: price1
            data_type: "decimal(18,9)"
            tests: 
              - not_null
          - name: price2
            data_type: "decimal(18,9)"
            tests: 
              - not_null
          - name: price3
            data_type: "decimal(18,9)"
            tests: 
              - not_null
          - name: price4
            data_type: "decimal(18,9)"
            tests: 
              - not_null
```
### dbt Schema: Sources
Each source must have the following keys:
  1. name: The name of the source internal to dbt
  1. schema: The schema to load the tables to in the database. Keep this the same as the name
  1. tables: A list of each of the tables that we will ingest

### dbt Schema: Tables
Each table within a source must have the following keys:
  1. name: The name of the table
  1. external: This sets that this is a delta table, and is stored in a mounted container. Always include this object as it is here.
  1. join: object to define how we should add new data to the main source table. The main way will be as above, where we merge into the table to avoid duplicate rows, and specify the 'date' column to merge on. The 'column' entry will accept a comma-separated list of column names, if more than one forms the primary key
  1. file_details: Gives general information about the source file to help read it. These entries are passed to, and so must follow the conventions of, the [pyspark.sql.DataFrameReader.csv](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.sql.DataFrameReader.csv.html#pyspark.sql.DataFrameReader.csv) function. 'path' and 'schema' are set separately, so do not set these or the 'inferSchema' and 'enforceSchema' parameters. Some example parameters are below:
      1. sep: When reading the source files, this is the field separator. For example, in comma-separated values (.csv), this is a comma ','
      1. header: boolean, whether the source files have a header row
      1. dateFormat: The format to convert from strings to date types. 
      1. timestampFormat: The format to convert from strings to datetimes types. 
  1. columns: A list of all the columns of the file. Schema is detailed in the section below

### dbt Schema: Columns
For each table all columns need to be specified, and each must have the following keys: 
  1. name: The name of the column
  1. data_type: The data type we expect the column to be, using [Databricks SQL data types](https://docs.microsoft.com/en-us/azure/databricks/spark/latest/spark-sql/language-manual/sql-ref-datatypes#sql)
  1. tests: A list of any [dbt tests](https://docs.getdbt.com/docs/building-a-dbt-project/tests) that we want to apply to the column on ingestion
