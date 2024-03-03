# pre setup

docker:
	docker compose up -d

env:
	python3 -m venv .venv

env-active:
	source ./.venv/bin/activate	&&	\
	$$SHELL

pip:
	pip3 install -r requirements.txt

# debug Proxy Re-Emcryption
# datasets:
#	-	 ./data/linear-regression/employee_data.csv		(15KB)
#	-	./data/mnist/train.csv							(76.8MB)
dpre:
	clear &&	\
	echo "\n\n\n\n YOU ARE IN DEBUG MODE \n\n\n\n" &&	\
	python3 ./fl-proxy_reEncryption-example/main.py ./data/linear-regression/employee_data.csv --debug_mode

