example: example-server example-client

example-server: env-run
	@echo "🏃‍➡️ $(BLUE)running example server...$(NC)"
	gunicorn -k eventlet -w 1 example.hello:server

define show_and_run
	$(eval $@_CMD = "$(1)")
	@echo "$(GREEN)${$@_CMD}$(NC)"
	@$(shell echo $(1))
endef

example-client: env-run
	@echo "🏃‍➡️ $(BLUE)waiting a second for example server to boot...$(NC)"
	@sleep 1
	@echo "🏃‍➡️ $(BLUE)executing a few queries...$(NC)"
	$(call show_and_run,"curl -s http://localhost:8000/MyData/1 | python -m json.tool")
	$(call show_and_run,"curl -s http://localhost:8000/MyData/2 | python -m json.tool")
	$(call show_and_run,"curl -s http://localhost:8000/MyData/3 | python -m json.tool")
	@echo "🏃‍➡️ $(BLUE)all done, use ctrl+c to terminate this example session$(NC)"
