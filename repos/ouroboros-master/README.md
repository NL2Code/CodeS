ouroboros is no longer in development. It does its job (more or less) and the devs have succumb to real life! Please feel free to fork and maintain as you wish. We appreciate all of the support in the last year :). After support from the community, automated version bumps will continue to try to keep ouroboros in check with dependencies. ⚠️⚠️⚠️
<img width="800" src="https://raw.githubusercontent.com/pyouroboros/ouroboros/master/assets/ouroboros_logo_primary_long_cropped.jpg" alt="Ouroboros Logo">

Automatically update your running Docker containers to the latest available image.

The de-facto standard for docker update automation

## Overview

Ouroboros will monitor (all or specified) running docker containers and update them to the (latest or tagged) available image in the remote registry. The updated container uses the same tag and parameters that were used when the container was first created such as volume/bind mounts, docker network connections, environment variables, restart policies, entrypoints, commands, etc.

- Push your image to your registry and simply wait your defined interval for ouroboros to find the new image and redeploy your container autonomously.
- Notify you via many platforms courtesy of [Apprise](https://github.com/caronc/apprise) 
- Serve metrics for trend monitoring (Currently: Prometheus/Influxdb)
- Limit your server ssh access
- `ssh -i key server.domainname "docker pull ... && docker run ..."` is for scrubs
- `docker-compose pull && docker-compose up -d` is for fancier scrubs
