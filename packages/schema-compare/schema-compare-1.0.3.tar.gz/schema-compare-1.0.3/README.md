# Schema Compare
Schema compare is a simple utility tool with the sole goal of comparing schemas between two databases. Currently it only supports postgresql.


### Installation
You can install Schema Compare from PyPi:

    pip install schema-compare

### How to use

1. Define config.toml file
2. python schema-compare {{config.toml path}}


### Configuration file

    [source]
    username = ....
    password = ....
    hostname = ....
    database = ....

    [target]
    username = ....
    password = ....
    hostname = ....
    database = ....