from Backend.microservices.conversor.config.config import Config

config: dict = Config()
host: str = config['host']
app: str = config['app']

port: str = app['API']['net']['port']
ssl: str = app['API']['ssl']
protcol: str = 'https' if ssl else 'http'


BASE_URL: str = f"{protcol}://{host}:{port}"