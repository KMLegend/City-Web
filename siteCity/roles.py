from rolepermissions.roles import AbstractUserRole


class Gerente(AbstractUserRole):
    available_permissons = {'criar_linhas':True,'ver_linhas':True}

class Corretor(AbstractUserRole):
    available_permissons = {'ver_linhas': True, 'acessar_site': True}