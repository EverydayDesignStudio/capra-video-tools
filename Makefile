define INIT_MESSAGE
Installing dependencies
endef

export INIT_MESSAGE

init:
	@echo "$$INIT_MESSAGE"
	sudo pip3 install -r requirements.txt
