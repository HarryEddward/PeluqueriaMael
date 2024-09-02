from Backend.microservices.conversor.config.config import Config

config: dict = Config()
app: str = config['app']

host: str = app['API']['testing']['host']
port: str = app['API']['net']['port']
ssl: str = app['API']['ssl']
protcol: str = 'https' if ssl else 'http'


BASE_URL: str = f"{protcol}://{host}:{port}"

login_credentials: dict = {
  "email": "adrianbestloginuser@gmail.com",
  "password": "Dark_Draw_Everything"
}

delete_credentials: dict = {
    "email": "user_adrian_delete@gmail.com",
    "password": "PopThatShit"
}

register_credentials: dict = {
    "email": "new_user_register_deleteab@gmail.com",
    "password": "NewPasswordForThat"
}