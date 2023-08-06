# `jinja-docker-compose`
[`jinja-docker-compose`](https://github.com/MorganLindqvist/jinja-compose) is a simple python script that wraps [`docker-compose`](https://docs.docker.com/compose/) to provide Jinja2 based templating ability to `docker-compose`. It is based on ['jinja-compose'](https://github.com/sinzlab/jinja-compose).

## Dependencies
`jinja-docker-compose` requires following dependencies to be installed on the system:
* python3
* python3-pip
* Docker engine

## Installing
To install the script, simply run:

```bash
$ pip install jinja-docker-compose
```
The script is installed in ~/.local/bin. If not in the PATH add the following to your initiation script, like .bashrc
```
PATH=~/.local/bin:$PATH
```

## Using `jinja-docker-compose`
The `jinja-docker-compose` preprocess the `docker-compose` file to act upon for instance *for loops* and *conditional statements*. The variables used in the preprocessing resides in a dictionnay file in JSON format.

`jinja-docker-compose` can either just do the pre-processing or as well run `docker-compose` on the processed file.

Example of dictionary file:
```json
{
  "LOGGING": "false",
  "N_GPU": 2
}
```

`docker-compose` file to preprocess:
```
version: "3"
services:
  {% for i in range(N_GPU) %}
  ubuntu{{i}}:
    image: ubuntu:latest
  {% endfor %}
  ubuntulog:
    image: ubuntu:latest
    {% if LOGGING == 'true' %}
    logging:
      driver: syslog
      options:
        syslog-address: "tcp://graylog.example.com:516"
    {% endif %}
```
After processing the file looks like this:
```
version: "3"
services:
  ubuntu1:
    image: ubuntu:latest
  ubuntu2:
    image: ubuntu:latest
  ubuntulog:
    image: ubuntu:latest
```
The default names of the files are:
File|Default name
:--|--
Input file to preprocess|docker-compose.yml.j2
Dictionary file| docker-compose.dic
Output file | docker-compose.yml

The options are:
Option|Description
:--|--
-f|Input file name
-D|Dictionary file name
-o|Output file name
--loader|Uses the FullLoader when loading the YAML, this enables the possible exploit that the FullLoader opens up for.
-r|Apart from genereates the output file, also run `docker-compose`

All options that are valid options to `docker-compose` can also be given to `jinja-docker-compose`and then passed on to `docker-compose`

Depending on how your system is configured, you may need to run the script with `sudo` (i.e. if you usually need `sudo` to run `docker`, you will need `sudo`).
