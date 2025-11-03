run:
	nohup /root/anaconda3/bin/python -u hk_internet.py >> hk.out 2>&1 &

runHK:
	/root/anaconda3/envs/crawl/bin/python -u hk_internet.py

stop:
	kill $$(ps aux | grep '[h]k_internet.py' | awk '{print $$2}')
