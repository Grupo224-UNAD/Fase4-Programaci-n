#---------------CLASE CLIENTE--------------

# Se importan las clases necesarias desde el módulo core y abc.
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
        
#---------------CLASE SERVICIO --------------
class Servicio(ABC):

# Clase servicio para calcular costos, describir servicios y validar parámetros, ademas de implementar tres servicios.
    
    def __init__(self, nombre_servicio, precio_base):
        self.nombre_servicio = nombre_servicio
        self.precio_base = precio_base

    # Se obliga a implementar el calculo de costos con sobrecarga.
    @abstractmethod
    def calcular_costos(self, **kwargs):
        pass
        
    # Obliga a las subclases a dar una explicacion propia.
    @abstractmethod
    def describir_servicios(self):
        pass

    # Metodo para validar que el valor o los datos no sean negativos.
    def validar_parametros(self, valor):
        if valor < 0:
            # Si el valor es negativo, lanza un mensaje de error.
            raise ValidationError("Error en {self.nombre_servicio} el valor no puede ser negativo.")
        return True

# Se crea la clase reserva de salas y se definen los servicios incluidos.
class reservas_de_salas(Servicio):
    def describir_servicios(self):
        return "Reserva de sala: {self.nombre_servicio} con todos los servicios incluidos."

    # Se definen las horas y la inclusion de la categoria.
    def calcular_costos(self, horas=1, incluye_categoria=False):
        self.validar_parametros(horas, "horas")
        # Logica: precio x hora + recargo opcional por categoria.
        total = self.precio_base * horas
        if incluye_categoria:
            # Valor fijo de la Categoria.
            total += 250000
        return total
        
# Se crea la clase alquiler de equipos y se incluye el servicio tecnico.
class alquiler_de_equipos(Servicio):
    def describir_servicios(self):
        return "Alquiler de equipo: {self.nombre_servicio}. Ademas incluye servicio tecnico basico"

    # Se definen los dias y el seguro opcional.
    def calcular_costos(self, dias=1, seguro_opcional=True):
        self.validar_parametros(dias, "dias")
        # Logica: precio por dia con el descuento por mas de (5 dias).
        total = self.precio_base * dias
        if dias > 5:
            # 20% de descuento.
            total *= 0.80
        if seguro_opcional:
            # 10% del seguro por dia.
            total += (self.precio_base 0.10) * dias
            return total

# Se crea la clase asesorias especializadas 
class asesorias_especializadas(Servicio):
    def describir_servicios(self):
        return "Asesoria Especializada: {self.nombre_servicio}. Consultoria tecnica con los mejores expertos"

    # Se definen las horas y la urgencia.
    def calcular_costos(self, horas=1, es_de_urgencia=False):
        self.validar_paramteros(horas, "horas")
        # Logica: precio por hora con el recargo por la urgencia.
        tarifa_final = self.precio_base
        if es_de_urgencia:
            # 50% de racargo por urgencia
            tarifa_final *= 1.50
            return tarifa_final * horas
            
#---------------MÉTODOS SOBRECARGADOS--------------
    def calcular_costo_final(self, precio_base, impuesto=0, descuento=0, cargo_extra=0):
        
        "Método que calcula el costo final de un servicio, aplicando un descuento si es necesario."
        
        # Se crea una instancia del sistema de logs.
        logger = LogSystem()
        
        try:
            # Se valida que el precio base sea un número positivo.
            if precio_base < 0:
                logger.write("Error: El precio base no puede ser negativo.")
                # Si el precio base es negativo, se lanza una excepción de validación.
                raise ValidationError("El precio base no puede ser negativo.")
            
            # Se valida que el impuesto no sea negativo.
            if impuesto < 0:
                logger.write("Error: El impuesto no puede ser negativo.")
                # Si el impuesto es negativo, se lanza una excepción de validación.
                raise ValidationError("El impuesto no puede ser negativo.")
            
            # Se valida que el descuento no sea negativo.
            if descuento < 0:
                logger.write("Error: El descuento no puede ser negativo.")
                # Si el descuento es negativo, se lanza una excepción de validación.
                raise ValidationError("El descuento no puede ser negativo.")
            
            # Se valida que el cargo extra no sea negativo.
            if cargo_extra < 0:
                logger.write("Error: El cargo extra no puede ser negativo.")
                # Si el cargo extra es negativo, se lanza una excepción de validación.
                raise ValidationError("El cargo extra no puede ser negativo.")
            
            # Se calcula el impuesto aplicado al precio base.
            impuesto_aplicado = precio_base * (impuesto / 100)
            
            # Se suma el precio base más el impuesto. 
            costo_con_impuesto = precio_base + impuesto_aplicado
            
            # Se agregan cargos adicionales al costo con impuesto.
            costo_con_cargos = costo_con_impuesto + cargo_extra
            
            # Se aplica el descuento final calculado.
            costo_final = costo_con_cargos - descuento
            
            # Se valida que el costo final no sea negativo.
            if costo_final < 0:
                logger.write("Error: El costo final no puede ser negativo.")
                # Si el costo final es negativo, se lanza una excepción de validación.
                raise ValidationError("El costo final no puede ser negativo.")
            
            # Se retorna el costo final calculado.
            return costo_final
        
        # Se captura la excepción de validación.
        except ValidationError as e:
            # Se registra el error de validación en el sistema de logs.
            logger.write(f"Error de validación: {e}")
            # Se vuelve a lanzar la excepción para que el sistema de gestión la maneje.
            raise
