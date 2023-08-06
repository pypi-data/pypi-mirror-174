# psenv -- (Parameter Store Environment)
### a cli tool for managing environments stored in the AWS parameter store


## Getting Started
``pip install psenv``

or better yet, install as a standalone application using pipx

``pipx install psenv`` --> This is the best option


### Create a config file
at the terminal run
```shell
psenv init
```

This will create a directory at ``~/.psenv`` and a config file at `~/.psenv/psenv.yml`
this file is where you will define your environments.

### Example psenv.yml
```yaml
environments:
  some_meaningful_name:
    path: /the/path/used/in-the/aws/parameter-store
    env: /path/to/local/env/file/.env

```

You can now run

```shell
psenv show
```

You should see a list of all available environments


## Fetch an Environment from the AWS Parameter Store

This command will fetch all the parameters on the path configured in the ``path`` section of the `psenv.yml` file
```
psenv fetch --env some_meaningful_name
```

## Push and Environement to the AWS Parameter Store
Sometimes you need to set up new environments. This is easy with `psenv`
add an entry in `psenv.yml`

```yaml
environments:
  new_env:
    path: /some/parameter-store/path
    env: /path/to/.env
```

populate the .env file with the secrets and parameters you need for your environment and then run
``psenv push --env new_env``


## Credential Injection (Currently just AWS Supported)
Sometimes you might want to copy some environment variables from your local env to a .env file.
for example when you use temp AWS credentials and need to load them into more than one project / environment. To do this, get your creds however you normally would
and then

``psenv inject aws --env some_env``

all your aws credentials will be injected to your .env file! Like Magic!
