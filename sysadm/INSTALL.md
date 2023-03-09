

```
cd isard
cp isardvdi.cfg.example isardvdi.cfg
vi isardvdi.cfg
```

##### Services & Security

Install docker, docker-compose and set basic firewall and fail2ban ssh jail.

```
cd sysadm
bash debian_docker.sh
bash debian_firewall.sh
cd ..
```

##### OPTION A: Pull from docker hub

```
bash build.sh
docker-compose pull && docker-compose up -d
```


##### OPTION B: Build from source

```
bash build.sh
docker-compose build && docker-compose up -d
```


