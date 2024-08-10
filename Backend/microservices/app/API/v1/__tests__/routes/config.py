from Backend.microservices.conversor.config.config import Config

config: dict = Config()
app: str = config['app']

host: str = app['API']['testing']['host']
port: str = app['API']['net']['port']
ssl: str = app['API']['ssl']
protcol: str = 'https' if ssl else 'http'


BASE_URL: str = f"{protcol}://{host}:{port}"