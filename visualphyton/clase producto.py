"""#Clase Producto
class Producto:
    def __init__(self, nombre,precio,stock):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def mostrar_informacion(self):
        print("\n======Información del PRODUCTO======")
        print("Nombre:" , self.nombre)
        print("Precio:" , self.precio)
        print("Stock:" , self.stock)

#Crear objetos de la clase PRODUCTO
producto1 = Producto("Arroz",3.50,100)
producto2 = Producto("Azucar",4.50,50)
producto3 = Producto("Aceite",8.00,80)
producto4 = Producto("Leche",4.50,60)

#Mostrar la información de los PRODUCTOS
producto1.mostrar_informacion()
producto2.mostrar_informacion()
producto3.mostrar_informacion()
producto4.mostrar_informacion()





#Clase Producto
class Producto:
    def __init__(self, nombre,precio,stock):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def mostrar_informacion(self):
        print("\n======Información del PRODUCTO======")
        print("Nombre:" , self.nombre)
        print("Precio:" , self.precio)
        print("Stock:" , self.stock)
    
    def actualizar_precio(self,nuevo_precio):
        self.precio = nuevo_precio
        print("\npresio actualizado corectamente")
    def actualizar_stock(self,nuevo_stock):
        self.stock = nuevo_stock
        print("\nstock actualizado corectamente")

#Crear objetos de la clase PRODUCTO
producto1 = Producto("Arroz",3.50,100)
producto2 = Producto("Azucar",4.50,50)
producto3 = Producto("Aceite",8.00,80)
producto4 = Producto("Leche",4.50,60)

#Mostrar la información de los PRODUCTOS-
producto1.mostrar_informacion()
producto2.mostrar_informacion()
producto3.mostrar_informacion()
producto4.mostrar_informacion()


#actualizar precio y stock del producto
producto1.actualizar_precio(4)
producto1.actualizar_stock(110)

#mostar nuevamente l informcaion actualizadda
producto1.mostrar_informacion()  """












#Clase Producto
class Producto:
    def __init__(self, nombre,precio,stock):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def mostrar_informacion(self):
        print("\n======Información del PRODUCTO======")
        print("Nombre:" , self.nombre)
        print("Precio:" , self.precio)
        print("Stock:" , self.stock)

    def actualizar_precio(self,nuevo_precio):
        self.precio = nuevo_precio
        print("\nPrecio actualizado correctamente: ")

    def actualizar_stock(self,nuevo_stock):
        self.stock = nuevo_stock
        print("\nStock actualizado correctamente: ")

    def aplicar_descuento(self,porcentaje_descuento):
        descuento = self.precio*(porcentaje_descuento/100)
        self.precio -= descuento
        print(f"Descuento del {porcentaje_descuento}% aplicado. Nuevo precio. S/.{self.precio} ")

    def realizar_venta(self,cantidad):
        if cantidad <= self.stock:
            self.stock -= cantidad
            print(f"Venta realizada: {cantidad}: unidades vendidas")
            print(f"Stock restantes{self.stock}")
        else:
            print("No hay suficiente stock para realizar la venta")


#Crear objetos de la clase PRODUCTO
producto1 = Producto("Arroz",3.50,100)
producto2 = Producto("Azucar",4.50,50)
producto3 = Producto("Aceite",8.00,80)
producto4 = Producto("Leche",4.50,60)

#Mostrar la información de los PRODUCTOS
producto1.mostrar_informacion()
producto2.mostrar_informacion()
producto3.mostrar_informacion()
producto4.mostrar_informacion()

#PRODUCTO 1 MOSTRAR INFORMACION actualizada
producto1.mostrar_informacion()

#Aplicar descuento y mostrar la nueva informacion
producto1.aplicar_descuento(10) #Aplicar 10% de descuento
producto2.aplicar_descuento(10) #Aplicar 10% de descuento
producto3.aplicar_descuento(10) #Aplicar 10% de descuento
producto4.aplicar_descuento(10) #Aplicar 10% de descuento

#Realizar la venta 
producto1.realizar_venta(20)  #Vender 20 unidades
producto1.mostrar_informacion()

#Intentar vender mas unidades de las que hay en stock
producto1.realizar_venta(90) #Intentar vender 90 unidades (No hay suficiente stock)