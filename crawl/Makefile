


run:
	nohup /root/anaconda3/bin/python -u alertHS.py >> alert.out 2>&1 &

stop:
	kill $$(ps aux | grep '[a]lertHS.py' | awk '{print $$2}')
