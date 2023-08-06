import sys
import tomli
import argparse
from schema_compare.drivers.postgresql.connection import Connection

def main():
    if len(sys.argv) < 2:
        raise Exception("Please provide the file path of your configuration.toml file")

    FILE_PATH = sys.argv[1]

    with open(FILE_PATH, mode="rb") as fp:
        config = tomli.load(fp)

    source = config["source"]
    source = Connection(source["username"], source["password"], source["hostname"], source["database"])
    source = source.get_schema()
    target = config["target"]
    target = Connection(target["username"], target["password"], target["hostname"], target["database"])
    target = target.get_schema()
   
    def not_exists(row):
        table_name = row["table_name"]
        column_name = row["column_name"]
        return ((table_name  == target["table_name"]).sum() + (column_name  == target["column_name"]).sum()) == 0

    print(f'Source schema has {len(source)} (table_name,column_name)')
    print(f'Target schema has {len(source)} (table_name,column_name)')

    result = source[source.apply(not_exists, axis = 1)]
    print("The following are not present in target schema:")
    print(result)
    print(f"Target schema has less {len(result)} (table_name,column_name) than source schema")
    result = result.to_html()

    if len(sys.argv) == 3:
        #TODO - use argparse...
        print("Generating report")
        import os
        absolute_path = os.path.dirname(__file__)
        relative_path = "report.html"
        full_path = os.path.join(absolute_path, relative_path)
        f = open(full_path,"r")
        content = f.read()
        output = open("/output.html","w")
        output.write(content.replace("{{body}}",result))
        output.close()
        f.close()

if __name__ == "__main__":
    main()
   