import os

from back_end.helpers.constants import EnvModeChoices, ENV_MODE


def get_postgres_password():
    # code for storing db password in aws secrets
    # session = boto3.Session()
    # client = session.client(service_name='secretsmanager', region_name='PUT_OUR_AWS_REGION_HERE')
    # try:
    #     secrets_response = client.get_secret_value(SecretId="SocialBase")
    #     secrets = json.loads(secrets_response["SecretString"])
    #
    #     return secrets["postgres_pw"]
    #
    # except Exception as e:
    #     print("An error occurred accessing Secrets Manager secrets for postgres pw.", e)
    #     raise e
    return os.getenv('POSTGRES_PW')


def get_postgres_url_prod():
    user = os.getenv('POSTGRES_USER_PROD')
    host = os.getenv('POSTGRES_HOST_PROD')
    db = os.getenv('POSTGRES_DB_PROD')
    port = os.getenv('POSTGRES_PORT_PROD')
    if None in (user, host, db, port):
        raise Exception('check mssql env vars')
    password = get_postgres_password()
    return 'postgresql://{u}:{p}@{h}:{port}/{db}'.format(u=user, p=password, h=host, port=port, db=db)


def get_postgres_url_dev():
    user = os.getenv('POSTGRES_USER_DEV')
    host = os.getenv('POSTGRES_HOST_DEV')
    db = os.getenv('POSTGRES_DB_DEV')
    port = os.getenv('POSTGRES_PORT_DEV')
    if None in (user, host, db, port):
        raise Exception('check mssql env vars')
    password = get_postgres_password()
    return 'postgresql://{u}:{p}@{h}:{port}/{db}'.format(u=user, p=password, h=host, port=port, db=db)


def get_postgres_url_local():
    user = os.getenv('POSTGRES_USER_LOCAL')
    host = os.getenv('POSTGRES_HOST_LOCAL')
    db = os.getenv('POSTGRES_DB_LOCAL')
    port = os.getenv('POSTGRES_PORT_LOCAL')
    if None in (user, host, db, port):
        raise Exception('check mssql env vars')
    password = get_postgres_password()
    return 'postgresql://{u}:{p}@{h}:{port}/{db}'.format(u=user, p=password, h=host, port=port, db=db)


def get_postgres_url():
    if ENV_MODE == EnvModeChoices.prod:
        print('Getting PROD postgres url.')
        return get_postgres_url_prod()
    elif ENV_MODE == EnvModeChoices.dev:
        print('Getting DEV postgres url.')
        return get_postgres_url_dev()
    elif ENV_MODE == EnvModeChoices.local:
        print('Getting LOCAL postgres url.')
        return get_postgres_url_local()
    else:
        raise NotImplementedError('bad env mode')
