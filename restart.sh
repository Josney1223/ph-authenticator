#!/bin/bash

podman stop AuthenticatorProjetoHorizonte

podman rm AuthenticatorProjetoHorizonte

podman image rm authenticator-projeto-horizonte

podman build -t=authenticator-projeto-horizonte .

podman run -dt -p 40000:2000 --cpus=0.25 -m=256m --name=AuthenticatorProjetoHorizonte authenticator-projeto-horizonte