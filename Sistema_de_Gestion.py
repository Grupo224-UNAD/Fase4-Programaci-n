#---------------CLASE CLIENTE--------------

# Se importan las clases necesarias desde el módulo core.
from core import ValidationError, LogSystem
from core import EntidadSistema
from abc import ABC, abstractmethod

class Cliente(EntidadSistema):
    
    "Clase que representa a un cliente en el sistema de gestión," 
    "con atributos privados para nombre, email y teléfono."
    
    def __init__(self, nombre, email, telefono):
        
        "Constructor de la clase Cliente, que inicializa los atributos y llama al método de validación."
        
        # Se asignan los valores a los atributos privados.
        self.__nombre = nombre
        self.__email = email
        self.__telefono = telefono
        
        # Se llama al método de validación para verificar los datos del cliente.
        self.validar()
    
    
    def validar(self):
        
        "Método que valida los datos del cliente."
        "Lanza una excepción de validación si los datos no son correctos"
        "y registra el error en el sistema de logs."
    
        # Se crea una instancia del sistema de logs.
        logger = LogSystem()
        
        try:
            # Se verifica que el nombre no esté vacío.
            if not self.__nombre:
                # Si el nombre está vacío, se lanza una excepción de validación.
                raise ValidationError("El nombre del cliente no puede estar vacío.")
            
            # Se verifica que el email contenga un "@" para ser considerado válido.
            if not self.__email or "@" not in self.__email:
                # Si el email no es válido, se lanza una excepción de validación.
                raise ValidationError("El email del cliente no es válido.")
            
            # Se verifica que el teléfono contenga solo dígitos.
            if not self.__telefono or not self.__telefono.isdigit():
                # Si el teléfono no es válido, se lanza una excepción de validación.
                raise ValidationError("El teléfono del cliente debe contener solo números.")
        
        # Se captura la excepción de validación.    
        except ValidationError as e:
            
            # Se registra el error de validación en el sistema de logs.
            logger.write(f"Error de validación: {e}")
            
            # Se vuelve a lanzar la excepción para que el sistema de gestión la maneje.
            raise
    
    def get_info(self):
        
        "Método que devuelve la información del cliente en formato de cadena."
        
        return f"Cliente: {self.__nombre}, Email: {self.__email}, Teléfono: {self.__telefono}"
    
    @property
    def nombre(self):
        
        "Propiedad que devuelve el nombre del cliente."
        
        return self.__nombre
        
    @property
   def email(self):

       "Propiedad que devuelve el email del cliente."

       return self.__email

    @property
    def telefono(self):

        "Propiedad que devuelve el telefono del cliente."

        return self.__telefono

class Servicio(ABC):
    def __init__(self, nombre)
