#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color


pip install requests
pip uninstall pip-system-certs &> /dev/null

python3 test/simple-https-server.py &

curl -s https://localhost:4443 || (echo -e "\n${RED}curl failed as expected${NC}"; true)
python3 test/request.py 2> /dev/null || (echo -e "${RED}python failed as expected${NC}\n"; true)

cp test/pki/ca.crt  /usr/local/share/ca-certificates/
update-ca-certificates

curl -s https://localhost:4443 > /dev/null && echo -e "\n${GREEN}curl passed as expected${NC}"
python3 test/request.py 2> /dev/null || (echo -e "${RED}python failed as expected${NC}\n"; true)

pip install .

curl -s https://localhost:4443 > /dev/null && echo -e "\n${GREEN}curl passed as expected${NC}"
python3 test/request.py > /dev/null && echo -e "${GREEN}python passed as expected${NC}\n"
