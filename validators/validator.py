from ..service.blacklist_service import BlacklistService

campos_requeridos = ['email', 'blocked_reason', 'app_uuid']

service = BlacklistService()

class Validador():

    def validar_request_blacklist(self, data):
        resultado = None

        resultado = self.validar_datos_requeridos(data)

        if resultado is None:
            resultado = self.validar_email_existente(data)

        return resultado

    def validar_datos_requeridos(self, data):
        campos_faltantes = ''

        for campo in campos_requeridos:
            if campo not in data:
                campos_faltantes += f"{campo} "

        if campos_faltantes != '':
            return f" faltan los campos {campos_faltantes}"
        else:
            return None        

    def validar_email_existente(self, data):
        email = data.get('email')
        blacklist_item = service.consultar_by_email(email)

        if blacklist_item:
            return  f"el email {email} ya se encuentra registrado"
        else:
            return None