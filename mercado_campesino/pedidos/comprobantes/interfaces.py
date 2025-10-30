from abc import ABC, abstractmethod
from ..models import Pedido

class ComprobantePagoStrategy(ABC):
    """
    Interfaz que define el contrato para la generación de comprobantes de pago.
    Siguiendo el principio de inversión de dependencias, las implementaciones
    concretas dependerán de esta abstracción.
    """
    
    @abstractmethod
    def generar_comprobante(self, pedido: Pedido) -> bytes:
        """
        Genera un comprobante de pago en formato PDF.
        
        Args:
            pedido: Instancia del modelo Pedido con la información necesaria
            
        Returns:
            bytes: Contenido del PDF generado en formato bytes
        """
        pass