example: example-server example-client

example-server: env-run
	@echo "🏃‍➡️ $(BLUE)running example server...$(NC)"
	gunicorn -k eventlet -w 1 example.hello:server

define show_and_run
	@echo "$(GREEN)$(1)$(NC)"
	@$(1)
endef

define fetch
	$(eval $@_CMD = curl -s http://localhost:8000/$(1)/$(2) | python -m json.tool)
	$(call show_and_run,${$@_CMD})
endef

example-client: env-run
	@echo "🏃‍➡️ $(BLUE)waiting a second for example server to boot...$(NC)"
	@sleep 1
	@echo "🏃‍➡️ $(BLUE)executing a few queries...$(NC)"
	$(call fetch,MyData,1)
	$(call fetch,MyData,2)
	$(call fetch,MyData,3)
	@echo "🏃‍➡️ $(BLUE)all done, use ctrl+c to terminate this example session$(NC)"
