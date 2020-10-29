define INIT_MESSAGE
Installing dependencies from both pip and apt-get
endef

export INIT_MESSAGE

init:
	@echo "$$INIT_MESSAGE"
	sudo pip3 install -r requirements.txt
	sudo ./install_apps.sh

