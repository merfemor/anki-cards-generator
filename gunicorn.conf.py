bind = "127.0.0.1:5055"
workers = 2
timeout = 60
# Initialize app in main process, otherwise init checks like Ollama availability won't stop it
preload_app = True

accesslog = "-"
errorlog = "-"
loglevel = "info"
