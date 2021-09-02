class ExceptionBase(Exception):
    """ Exceção base """
    pass


class TooManyRedirectsException(ExceptionBase):
    """ TooManyRedirects ao acessar uma URL """
    pass


class ConnectionErrorException(ExceptionBase):
    """ Erro genérico de conexão ao acessar uma URL """
    pass


class ForbiddenUrlException(ExceptionBase):
    """ Erro 403 ao acessar uma URL """
    pass
