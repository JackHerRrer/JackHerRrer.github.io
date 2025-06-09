# Overview
This repo is dedicated to retrieve data from an I-spindle and to store the received data online

## Architecture

```
                                                                                                                               
┌─────────────┐              ┌────────────┐┌───────────────────────────────────────┐┌──────────┐                  ┌───────────┐
│ I-spindle   │              │   Wifi     ││               Raspberry pi            ││   Wifi   │                  │spre       │
│             │              │ dongle 1   ││                                       ││ dongle 2 │                  │           │
│  Configured │              │            ││      ┌─────────────────────────┐      ││          │                  │           │
│  to         │              │         hotspot    │         Server          │      ││          │                  │           │
│  connect    │              │           wifi     │                         │     wifi         │                  │           │
│  to         │              │         "LaCave"   │                         │  connection      │                  │           │
│  "LaCave"   │              │            ││      │                         │  to internet     │                  │           │
│             │              │            ││      │                         │      ││          │                  │           │
│             │              │            ││      └─────────────────────────┘      ││          │                  │           │
└─────────────┘              └────────────┘└───────────────────────────────────────┘└──────────┘                  └───────────┘
```
## Raspberry pi config
Refer to [server_config.md](server/server_config.md)

## I-spindle configuration

[I-Spindle](https://www.ispindel.fr/demarrage-rapide/)
