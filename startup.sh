#!/usr/bin/bash
export PYTHONPATH=`pwd`
uvicorn --ssl-certfile ./cert.pem --ssl-keyfile ./key.pem infrastructure.entrypoint.web.fast_api.server:app --reload  