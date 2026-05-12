### IMPORTACIONES ###
from abc import ABC, abstractmethod
from datetime import datetime

### EXCEPCIONES PERSONALIZADAS ###
class ValidationError(Exception):
    """Excepción personalizada para errores de validación."""
    pass

class ReservationError(Exception):
    """Excepción personalizada para errores relacionados con reservas."""
    pass

class ServiciosNoDisponiblesError(Exception):
    """Excepción personalizada para errores relacionados con servicios."""
    pass

### SISTEMA LOGS ###
class LogSystem:
    def write(self, message):
        with open("sistema_logs.txt", "a", encoding="utf-8") as archivo:
            fecha = datetime.now()
            archivo.write(f"[{fecha}] {message}\n")

### CLASE ABSTRACTA GENERAL ###
class EntidadSistema(ABC):
    @abstractmethod
    def get_info(self):
        pass


#---------------CLASE CLIENTE--------------
class Cliente(EntidadSistema):
    """Clase que representa a un cliente en el sistema de gestión,
    con atributos privados para nombre, email y teléfono."""
    
    def __init__(self, nombre, email, telefono):
        
        """Constructor de la clase Cliente, que inicializa los atributos 
        y llama al método de validación."""
        
        # Se asignan los valores a los atributos privados.
        self.__nombre = nombre
        self.__email = email
        self.__telefono = telefono
        
        # Se llama al método de validación para verificar los datos del cliente.
        self.validar()
    
    # Validar datos
    def validar(self):
        
        """Método que valida los datos del cliente.

        Lanza una excepción de validación si los datos no son correctos
        y registra el error en el sistema de logs.
        """
    
        # Se crea una instancia del sistema de logs.
        logger = LogSystem()
        
        try:
            # Se verifica que el nombre no esté vacío.
            if not self.__nombre:
                # Si el nombre está vacío, se lanza una excepción de validación.
                raise ValidationError(
                    "El nombre del cliente no puede estar vacío."
                    )
            
            # Se verifica que el email contenga un "@" para ser considerado válido.
            if not self.__email or "@" not in self.__email:
                # Si el email no es válido, se lanza una excepción de validación.
                raise ValidationError(
                    "El email del cliente no es válido."
                    )
            
            # Se verifica que el teléfono contenga solo dígitos.
            if not self.__telefono or not self.__telefono.isdigit():
                # Si el teléfono no es válido, se lanza una excepción de validación.
                raise ValidationError(
                    "El teléfono del cliente debe contener solo números."
                    )
        
        # Se captura la excepción de validación.    
        except ValidationError as e:
            
            # Se registra el error de validación en el sistema de logs.
            logger.write(
                f"Error de validación: {e}"
                )
            
            # Se vuelve a lanzar la excepción para que el sistema de gestión la maneje.
            raise
    
    # Información del cliente
    def get_info(self):
        
        """Método que devuelve la información del 
        cliente en formato de cadena."""
        
        return (
            f"Cliente: {self.__nombre}, "
            f"Email: {self.__email},"
            f"Teléfono: {self.__telefono}"
            )
    
    # Encapsulación
    @property
    def nombre(self): 
        """Propiedad que devuelve el nombre del cliente."""
        return self.__nombre
        
    @property
    def email(self):
       """Propiedad que devuelve el email del cliente."""
       return self.__email

    @property
    def telefono(self):
        """Propiedad que devuelve el telefono del cliente."""
        return self.__telefono
    

       
#---------------CLASE SERVICIO --------------
class Servicio(ABC):

    """Clase servicio para calcular costos, describir servicios 
    y validar parámetros, ademas de implementar tres servicios."""
    
    def __init__(self, nombre_servicio, precio_base):
        self.nombre_servicio = nombre_servicio
        self.precio_base = precio_base
        
        if precio_base < 0:
            raise ValidationError("El precio base no puede ser negativo.")

    # Se obliga a implementar el calculo de costos con sobrecarga.
    @abstractmethod
    def calcular_costos(self, **kwargs):
        pass
        
    # Obliga a las subclases a dar una explicacion propia.
    @abstractmethod
    def describir_servicios(self):
        pass
    
    # Metodo para validar que el valor o los datos no sean negativos.
    def validar_parametros(self, valor, nombre_parametro) -> bool:
        if valor <= 0:
            # Si el valor es negativo, lanza un mensaje de error.
            raise ValidationError(
                f"{self.nombre_servicio} el valor de {nombre_parametro} no puede ser negativo."
                )
        return True

# SE CREA LA CLASE RESERVA DE SALAS Y SE DEFINEN LOS SERVICIOS INCLUIDOS.
class ReservaSala(Servicio):
    def describir_servicios(self):
        return(
            f"Reserva de sala: {self.nombre_servicio}. con todos los servicios incluidos."
        )

    # Se definen las horas y la inclusion de la categoria.
    def calcular_costos(
        self, 
        horas=1,
        incluye_categoria=False
    ):
        
        self.validar_parametros(horas, "Horas")
        
        # Logica: precio x hora + recargo opcional por categoria.
        total = self.precio_base * horas
        if incluye_categoria:
            # Valor fijo de la Categoria.
            total += 250000
        return total
        
# SE CREA LA CLASE ALQUILER DE EQUIPOS Y SE INCLUYE EL SERVICIO TECNICO.
class AlquilerEquipo(Servicio):
    def describir_servicios(self):
        return (
            f"Alquiler de equipo:"
            f"{self.nombre_servicio}. Ademas incluye servicio tecnico basico"
        )

    # Se definen los dias y el seguro opcional.
    def calcular_costos(
        self, dias=1, seguro_opcional=True
        ):
        self.validar_parametros(dias, "Dias")
        # Logica: precio por dia con el descuento por mas de (5 dias).
        total = self.precio_base * dias
        if dias > 5:
            # 20% de descuento.
            total *= 0.80
        if seguro_opcional:
            # 10% del seguro por dia.
            total += (self.precio_base * 0.10) * dias
            return total

# SE CREA LA CLASE ASESORIAS ESPECIALIZADAS.
class AsesoriaEspecializada(Servicio):
    def describir_servicios(self):
        return(
            f"Asesoria Especializada:"
            f"{self.nombre_servicio}. Consultoria tecnica con los mejores expertos"
        )

    # Se definen las horas y la urgencia.
    def calcular_costos(
        self, horas=1, es_de_urgencia=False
        ):
        self.validar_parametros(horas, "Horas")
        # Logica: precio por hora con el recargo por la urgencia.
        tarifa_final = self.precio_base
        if es_de_urgencia:
            # 50% de racargo por urgencia
            tarifa_final *= 1.50
            return tarifa_final * horas


 
#---------------CLASE RESERVA--------------
class Reserva:

    """
    Clase que representa una reserva realizada por un cliente
    para un servicio específico.
    """

    def __init__(self, cliente, servicio, duracion):

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

        logger = LogSystem()

        try:

            # VALIDAR CLIENTE
            if cliente is None:
                raise ValidationError(
                    "La reserva debe tener un cliente."
                )

            # VALIDAR SERVICIO
            if servicio is None:
                raise ValidationError(
                    "La reserva debe tener un servicio."
                )

            # VALIDAR DURACIÓN
            if duracion <= 0:
                raise ValidationError(
                    "La duración debe ser mayor a cero."
                )

        except ValidationError as e:

            logger.write(
                f"Error al crear reserva: {e}"
            )

            raise ReservationError(
                "No se puede crear la reserva"
            ) from e

    # MÉTODO PARA CONFIRMAR RESERVA
    def confirmar(self):

        logger = LogSystem()

        try:

            if self.estado == "Cancelada":
                raise ValidationError(
                    "No se puede confirmar una reserva cancelada."
                )

            self.estado = "Confirmada"

            logger.write(
                "Reserva confirmada correctamente."
            )

        except ValidationError as e:

            logger.write(
                f"Error al confirmar reserva: {e}"
            )

            raise ReservationError(
                "No se pudo crear la reserva"
            ) from e

    # MÉTODO PARA CANCELAR RESERVA
    def cancelar(self):

        logger = LogSystem()

        try:

            if self.estado == "Cancelada":
                raise ValidationError(
                    "La reserva ya está cancelada."
                )

            self.estado = "Cancelada"

            logger.write(
                "Reserva cancelada correctamente."
            )

        except ValidationError as e:

            logger.write(
                f"Error al cancelar reserva: {e}"
            )

            raise

    # MÉTODO PARA PROCESAR RESERVA
    def procesar_reserva(self):

        logger = LogSystem()

        try:

            if self.estado != "Confirmada":
                raise ValidationError(
                    "La reserva debe estar confirmada para procesarse."
                )

            total = self.servicio.precio_base * self.duracion

            logger.write(
                f"Reserva procesada. Total: {total}"
            )

            return total

        except Exception as e:

            logger.write(
                f"Error al procesar reserva: {e}"
            )

            raise

        finally:

            logger.write(
                "Finalizó el procesamiento de la reserva."
            )

    # MOSTRAR INFORMACIÓN
    def mostrar(self):

        return (
            f"Cliente: {self.cliente.nombre}\n"
            f"Servicio: {self.servicio.nombre_servicio}\n"
            f"Duración: {self.duracion}\n"
            f"Estado: {self.estado}"
        )     
    print("\n===== PRUEBAS RESERVA =====")

try:

    cliente1 = Cliente(
        "Carlos",
        "carlos@gmail.com",
        "3001234567"
    )
    
    servicio1 = ReservaSala(
        "Sala VIP",
        100000
    )
    
    reserva1 = Reserva(
        cliente1,
        servicio1,
        3
    )

    print("\nReserva creada:")
    print(reserva1.mostrar())

    reserva1.confirmar()

    total = reserva1.procesar_reserva()

    print(f"\nCosto total: {total}")

    reserva1.cancelar()

    print("\nEstado final:")
    print(reserva1.mostrar())

except Exception as e:

    print("Error:", e) 


       
#---------------MÉTODOS SOBRECARGADOS--------------
class CalculadoraCostos:
    
    """Clase que implementa métodos para calcular costos de servicios,
    aplicando descuentos e impuestos según sea necesario."""
    def calcular_costo_final(
        self, 
        precio_base,
        impuesto=0,
        descuento=0,
        cargo_extra=0
        ):
        
        """Método que calcula el costo final de un servicio,
        aplicando un descuento si es necesario."""
        
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
        
        
        
#-------------10 OPERACIONES DEL SISTEMA-------------
print("\n===== 10 OPERACIONES DEL SISTEMA =====")


# OPERACIÓN 1
try:
    cliente1 = Cliente("Ana", "ana@gmail.com", "3009876543")
    print("1. Cliente registrado correctamente")

except Exception as e:
    print("1. Error:", e)


# OPERACIÓN 2
try:
    cliente2 = Cliente("", "correo", "abc")
    print("2. Cliente registrado")

except ValidationError as e:
    print("2. Error controlado:", e)


# OPERACIÓN 3
try:
    servicio1 = ReservaSala("Sala VIP", 100000)
    print("3. Servicio creado correctamente")
    
except Exception as e:
    print("3. Error:", e)


# OPERACIÓN 4
try:
    servicio2 = AsesoriaEspecializada("Marketing", -500)
    print("4. Servicio creado")

except Exception as e:
    print("4. Error controlado:", e)


# OPERACIÓN 5
try:
    reserva1 = Reserva(cliente1, servicio1, 2)
    print("5. Reserva creada correctamente")

except Exception as e:
    print("5. Error:", e)


# OPERACIÓN 6
try:
    reserva2 = Reserva(cliente1, servicio1, 0)
    print("6. Reserva creada")

except Exception as e:
    print("6. Error controlado:", e)


# OPERACIÓN 7
try:
    reserva1.confirmar()
    print("7. Reserva confirmada")

except Exception as e:
    print("7. Error:", e)


# OPERACIÓN 8
try:
    reserva1.cancelar()
    print("8. Reserva cancelada")

except Exception as e:
    print("8. Error:", e)


# OPERACIÓN 9
try:
    servicio3 = AlquilerEquipo("VideoBeam", 80000)
    
    total = servicio3.calcular_costos()

    print("9. Costo calculado:", total)

except Exception as e:
    print("9. Error:", e)


# OPERACIÓN 10
try:
    print("10. Información final:")
    print(reserva1.mostrar())

except Exception as e:
    print("10. Error:", e)
