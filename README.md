# Food Store --- Sistema de Gestión de Pedidos

**Trabajo Práctico Integrador (TPI) --- Programación II**\
**Tecnicatura Universitaria en Programación**

Food Store es una aplicación de consola desarrollada en Python para
gestionar categorías, productos, usuarios y pedidos de un negocio de
comidas. El sistema aplica Programación Orientada a Objetos (POO),
organiza las responsabilidades en capas y ofrece distintos menús según
el rol del usuario autenticado.

------------------------------------------------------------------------
dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
## Integrantes

-   **Integrante 1:** Joaquin Moreno
-   **Integrante 2:** Kevin Giraldo

## Enlaces del proyecto

-   **Repositorio de GitHub:** https://github.com/joaquinmoreno1781/Trabajo-Practico-Integrador-Programaci-n-2.git
-   **Video** https://youtu.be/ypLILuvWAz8

------------------------------------------------------------------------

## 1. Objetivo y alcance

El objetivo de Food Store es administrar la información básica de un
negocio de comidas desde una interfaz de consola. Según el rol
autenticado, el sistema habilita las operaciones correspondientes:

-   **Administrador (`ADMIN`):** administra categorías, productos,
    usuarios y pedidos.
-   **Cliente (`USUARIO`):** consulta categorías y productos
    disponibles, sus propios pedidos y sus datos personales.

La aplicación incorpora validaciones de entrada, reglas de negocio y
excepciones propias para informar errores sin interrumpir
inesperadamente la ejecución.

## 2. Funcionalidades principales

### Inicio de sesión

-   Acceso mediante mail y contraseña.
-   Identificación del rol del usuario.
-   Hasta tres intentos de autenticación.
-   Menú diferente para administrador y cliente.

### Administración

-   Gestión de categorías.
-   Gestión de productos y stock.
-   Gestión de usuarios.
-   Gestión de pedidos y sus estados.
-   Consultas y listados desde los menús de consola.

### Cliente

-   Consulta de categorías.
-   Consulta de productos disponibles.
-   Consulta de sus propios pedidos.
-   Consulta de sus datos personales.

### Pedidos y stock

-   Selección del usuario y forma de pago.
-   Incorporación de productos y cantidades.
-   Cálculo del total a partir de los detalles del pedido.
-   Validación de stock disponible.
-   Descuento de stock al crear el pedido.
-   Devolución de stock al cancelar un pedido, según las reglas
    implementadas.

### Interfaz

La interfaz utiliza paneles y estilos de consola para organizar la
información. Los menús interactivos permiten navegar con las flechas y
confirmar con Enter.

------------------------------------------------------------------------

## 3. Tecnologías y dependencias

-   **Python 3.12 o superior.**
-   **Rich:** presentación de paneles, tablas, mensajes y estilos en
    consola.
-   **Questionary:** componentes de selección interactiva.
-   **prompt-toolkit:** soporte para la interacción y presentación de
    controles de consola.

Las dependencias externas se encuentran declaradas en
`requirements.txt`.

## 4. Requisitos previos

Antes de ejecutar el proyecto se necesita:

1.  Tener instalado Python 3.12 o una versión superior.
2.  Tener disponible una terminal (PowerShell, CMD o terminal integrada
    de VS Code).
3.  Descargar o clonar este repositorio.

Comprobar la instalación de Python:

``` bash
python --version
```

En Windows también se puede utilizar:

``` powershell
py --version
```

## 5. Instalación

Clonar el repositorio:

``` bash
git clone https://github.com/joaquinmoreno1781/Trabajo-Practico-Integrador-Programacion-2.git
```

Ingresar a la carpeta del proyecto:

``` bash
cd Trabajo-Practico-Integrador-Programacion-2
```

Instalar las dependencias:

``` bash
py -m pip install -r requirements.txt
```

Si el comando `py` no está disponible, utilizar:

``` bash
python -m pip install -r requirements.txt
```

## 6. Ejecución

Desde la carpeta raíz del proyecto, ejecutar:

``` bash
py main.py
```

O bien:

``` bash
python main.py
```

El programa carga usuarios y datos de ejemplo en memoria al iniciarse y
presenta el formulario de acceso.

### Credenciales de demostración

  Rol             Mail                    Contraseña
  --------------- ----------------------- ------------
  Administrador   `admin@foodstore.com`   `admin123`
  Cliente         `juan@foodstore.com`    `juan123`

------------------------------------------------------------------------

## 7. Organización del código

El proyecto está separado en paquetes según la responsabilidad de cada
parte:

``` text
FoodStore/
├── main.py
├── pruebas.py
├── requirements.txt
├── README.md
├── entidades/
│   ├── base.py
│   ├── calculable.py
│   ├── categoria.py
│   ├── producto.py
│   ├── usuario.py
│   ├── pedido.py
│   └── detalle_pedido.py
├── enums/
│   ├── rol.py
│   ├── estado.py
│   └── forma_pago.py
├── excepciones/
│   └── food_store_error.py
├── servicios/
│   ├── base_servicio.py
│   ├── categoria_servicio.py
│   ├── producto_servicio.py
│   ├── usuario_servicio.py
│   └── pedido_servicio.py
└── consola/
    ├── ui.py
    ├── lectura.py
    ├── menu.py
    ├── menu_administrador.py
    └── menu_cliente.py
```

### Responsabilidad de cada paquete

  -----------------------------------------------------------------------
  Paquete / archivo                   Responsabilidad
  ----------------------------------- -----------------------------------
  `entidades/`                        Modela las clases del dominio y sus
                                      atributos, propiedades y
                                      comportamientos.

  `enums/`                            Define los valores posibles para
                                      roles, estados y formas de pago.

  `excepciones/`                      Contiene excepciones propias del
                                      sistema.

  `servicios/`                        Administra colecciones y aplica
                                      reglas de negocio.

  `consola/`                          Gestiona la interacción, los menús,
                                      la lectura de datos y la
                                      presentación.

  `main.py`                           Inicializa los servicios, carga
                                      datos de demostración y administra
                                      las sesiones.

  `pruebas.py`                        Ejecuta pruebas automatizadas del
                                      modelo y los servicios.

  `requirements.txt`                  Declara las dependencias necesarias
                                      para la interfaz.
  -----------------------------------------------------------------------

## 8. Conceptos de Programación Orientada a Objetos aplicados

El desarrollo utiliza los siguientes conceptos:

-   **Abstracción:** `Base` y `Menu` definen comportamientos y
    estructuras comunes.
-   **Herencia:** las entidades concretas heredan de `Base`; los menús
    específicos heredan de `Menu`.
-   **Encapsulamiento:** los atributos se protegen y se accede a ellos
    mediante propiedades y métodos.
-   **Polimorfismo:** `MenuAdministrador` y `MenuCliente` implementan su
    propio comportamiento mediante `mostrar()`.
-   **Sobrescritura:** las entidades proporcionan su representación
    mediante `__str__`; la comparación por identificador se define en la
    clase base.
-   **Interfaz:** `Calculable` establece el método `calcular_total()`
    implementado por `Pedido`.
-   **Composición:** un pedido contiene sus detalles, que representan
    los productos y cantidades incluidos.
-   **Enumeraciones:** `Rol`, `Estado` y `FormaPago` restringen los
    valores disponibles.
-   **Excepciones propias:** se utilizan para comunicar errores del
    dominio, como datos inválidos, duplicados y stock insuficiente.
-   **Type hints:** se incorporan anotaciones de tipos en atributos,
    parámetros y retornos.

## 9. Almacenamiento de datos

La información se administra en colecciones en memoria durante la
ejecución del programa. No se utiliza una base de datos ni archivos CSV
o JSON para persistir los registros.

Al cerrar el programa, los datos creados o modificados durante esa
ejecución se pierden. Al iniciar nuevamente, se cargan los datos de
demostración definidos en `main.py`. Este comportamiento responde al
requisito de almacenamiento en memoria de la consigna.

## 10. Ejecución de las pruebas

Para ejecutar las pruebas automatizadas:

``` bash
py pruebas.py
```

También se puede utilizar:

``` bash
python pruebas.py
```

Las pruebas incluidas verifican, entre otros casos:

1.  Rechazo de categorías duplicadas.
2.  Creación de pedidos, cálculo del total y descuento de stock.
3.  Rechazo de pedidos cuando el stock es insuficiente.
4.  Devolución del stock al cancelar un pedido.
5.  Rechazo de transiciones de estado no permitidas.
6.  Autenticación de usuarios.

Las pruebas deben ejecutarse desde la carpeta raíz del proyecto. 

------------------------------------------------------------------------
