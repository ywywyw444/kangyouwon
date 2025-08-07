class ServiceDiscovery:
    def __init__(self):
        self.services = {}
    
    def register_service(self, service_type, url):
        self.services[service_type] = url
    
    def get_service_url(self, service_type):
        return self.services.get(service_type)
