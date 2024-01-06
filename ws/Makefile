envName = web_learning_py311	

freeze:
ifneq ($(shell command -v conda),)
	conda env export > environment.yml
else ifneq ($(shell command -v mamba),)
	mamba env export > environment.yml
else
	@echo off
	echo "please install conda/mamba"
endif
