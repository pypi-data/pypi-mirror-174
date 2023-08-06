# Salt Vector

[Salt](https://saltproject.io) engine to send events to [Vector](https://vector.dev)

## Quickstart

First, install Vector on the same (or separate) server as the Salt Master: https://vector.dev/docs/setup/installation/

The engine requires the following source to be configured in Vector:

```toml
[sources.salt_socket]
type = "socket"
address = "127.0.0.1:9000"  # change to 0.0.0.0:9000 if the server is separate from Salt
mode = "tcp"
max_length = 102400  # tweak to fit the largest event payload
decoding.codec = "json"
```

Second, install the engine on the Salt Master:

For onedir Salt package:

```shell
salt-pip install saltext.vector
```

For classic Salt package:

```shell
pip install saltext.vector
```

Third, place a snippet like this into `/etc/salt/master.d/engines.conf` and restart the master:

```yaml
engines:
  - vector:
      # host_id: myid  # master or minion id override, optional
      address: "127.0.0.1:9000"  # vector socket endpoing
      # include_tags:
      #   - "*"
      exclude_tags:
        - salt/auth
        - minion_start
        - minion/refresh/*
        - "[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]"
```

To learn how to send events to Grafana and visualize the result, please visit the project documentation at https://turtletraction-oss.gitlab.io/salt-grafana/
