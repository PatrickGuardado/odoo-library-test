# Odoo Library Management - Prueba Técnica

Este módulo de Odoo 19 ha sido desarrollado como solución a la prueba técnica para el puesto de Desarrollador Odoo. A su vez,implementa un sistema para gestión de biblioteca, incluyendo control de inventario, préstamos, portal web para socios, integración con Punto de Venta (POS) y un endpoint API REST para la consulta de libros mediante un parámetro ISBN de los registros que se añadan a la base de datos.

## 1. Instalación y Configuración del Entorno

Para levantar este módulo en un entorno de desarrollo utilizando `virtualenv. Es necesario contar con un entorno de desarrollo de **Odoo 19** y **PostgreSQL**. Siga estos pasos para su configuración:

1. **Clonar el repositorio y preparar el entorno:**
   
    ### 1.1. Descarga de Odoo 19
    Si no cuenta con el código fuente del framework, puede clonarlo directamente desde el repositorio oficial de Odoo:
```bash
git clone [https://github.com/odoo/odoo.git](https://github.com/odoo/odoo.git) -b 19.0 --depth 1 odoo19
```
    ### 1.2. Configuración de PostgreSQL
    Asegúrese de tener PostgreSQL instalado y en funcionamiento. Crear una base de datos para Odoo y configure un usuario con los permisos adecuados. Actualice el archivo `odoo.conf` con las credenciales de la base de datos.

    CREATE USER odoo WITH PASSWORD 'odoo';
    ALTER USER odoo CREATEDB;

    ### 1.3. Configuración de `odoo.conf`
    Cree o modifique su archivo odoo.conf en la raíz de su entorno. Asegúrese de incluir las credenciales de su base de datos y la ruta donde haya guardado este módulo (custom_addons):

    [options]
    admin_passwd = admin_password
    db_host = localhost
    db_port = 5432
    db_user = odoo
    db_password = odoo
    # Añada la ruta de este módulo a su addons_path
    addons_path = odoo19/addons,custom_addons

    ### 1.4. Entorno virtual y dependencias
    ```bash
   # Crear entorno virtual en la raíz del proyecto
   python -m venv venv
   
   # Activar el entorno virtual
   # En Windows:
   venv\Scripts\activate
   
   # Instalar las dependencias de Odoo
   pip install -r odoo19/requirements.txt


2. **Iniciar el servidor de Odoo incluyendo la ruta de addons:**
   ```bash
   # Levantar el servidor de Odoo con el módulo de library_management
   python odoo19/odoo-bin -c odoo.conf -d nombre_base_datos -i library_management

3. **instalación de módulo**
    - Acceder a la interfaz de Odoo en el navegador (http://localhost:8069).
    - Iniciar sesión con las credenciales de administrador Usuario: admin, Contraseña: admin.
    - Navegar a la sección de "Aplicaciones" y buscar "Library Management".
    - Instalar el módulo y seguir las instrucciones para configurar la biblioteca, incluyendo la creación de categorías de libros, autores y socios.
    - Nota para el POS: Es necesario instalar un paquete de localización contable genérico para habilitar las transacciones del Punto de Venta.
  
    - Instalar el módulo de "Punto de Venta" para habilitar la integración con el sistema de préstamos:
    1. Instalar el Plan Contable
        En el apartado de aplicaciones, seleccionar Point of Sale, luego "install a chart of accounts".
    2. Aparecerá la configuración de contabilidad. seleccionar un paquete contable Fiscal Localization. Buscar y seleccionar "Configuración contable genérica".
    3. Hacer clic en Instalar/Guardar. Se tardará unos segundos configurando los diarios contables.

## 2. Preparación del Entorno y Casos de Prueba

Para evaluar correctamente todas las funcionalidades de este módulo, siga los pasos de preparación y ejecute los 5 casos de prueba detallados a continuación.

### Fase 0: Preparación de Datos y Usuarios
Antes de ejecutar las pruebas, es necesario configurar el entorno con datos de prueba:

1. **Creación de Usuarios y Roles:**
   * Navegar a *Ajustes > Usuarios y Compañías > Usuarios*.
   * Crear un usuario llamado **"Lector"**. En la pestaña de permisos, sección *Biblioteca*, asigne el Nivel de Acceso: **Usuario Público**.
   * Cree un usuario llamado **"Bibliotecario"**. En la sección *Biblioteca*, asigne el Nivel de Acceso: **Bibliotecario**.
   * Asigne una contraseña a ambos usuarios desde el botón de acción (*Engranaje > Cambiar Contraseña*).
2. **Creación de Catálogo Base:**
   * Inicie sesión como Administrador o Bibliotecario.
   * Navegue a *Biblioteca > Libros*.
   
   * Crear seis libros:
   
   * Libro 1: Título "El Quijote", Autor "Cervantes", ISBN "978-3-16-148410-0", Fecha de publicación 01/16/1605.
   * Libro 2: Título "Cien Años de Soledad", Autor "García Márquez", ISBN "978-0-14-118280-3", Fecha de publicación 05/30/1967.
   * Libro 3: ítulo "Viaje al Centro de la Tierra", Autor "Jules Verne", ISBN "978-6-07969-358-9", Fecha de publicación 01/01/2017.
   * Libro 4: Título "1984", Autor "George Orwell", ISBN "978-0-452-28423-4", Fecha de publicación 06/08/1949.
   * Libro 5: Titulo "Moby Dick", Autor "Herman Melville", ISBN "978-1-56619-909-4", Fecha de publicación 10/18/1851.
   * Libro 6: Título "El Principito", Autor "Antoine de Saint-Exupéry", ISBN "978-0-15-601219-5", Fecha de publicación 04/06/1943.
      
3. **Configuración Contable (Para POS):**
   * Navegue a la aplicación *Punto de Venta*.
   * Si el sistema lo solicita, instalar un "Paquete de Localización Contable" genérico para permitir la apertura de cajas.

---

### Caso 1: Lógica de Préstamos y Límites de Préstamo
**Objetivo:** Comprobar que el sistema respeta el límite de 5 préstamos por socio y la disponibilidad del libro.
1. **Paso a paso:**
   * Navegue a *Biblioteca > Préstamos*.
   * Seleccione un mismo cliente (ej. "Lector de Prueba") y registre 5 préstamos de libros diferentes.
   * Intente registrar un **6to préstamo** para el mismo cliente.
2. **Resultado Esperado:** El sistema bloquea la acción y muestra una alerta (`ValidationError`) indicando que el socio ya tiene 5 préstamos activos.
3. **Prueba secundaria:** Intente prestar un libro que ya tiene el estado "Prestado". El sistema también debe bloquear la acción con un mensaje de error.

### Caso 2: Automatización de Vencimientos
**Objetivo:** Verificar que la acción programada detecta préstamos con más de 30 días y cambia su estado.
1. **Paso a paso:**
   * Vaya a *Biblioteca > Préstamos* y abra un préstamo activo.
   * Edite manualmente el campo "Fecha de Préstamo" a una fecha de hace **más de 30 días** (ej. 1 de enero) y guarde.
   * Active el Modo Desarrollador en Odoo (*Ajustes > Activar modo desarrollador*).
   * Navegue a *Ajustes > Técnico > Acciones Programadas*.
   * Busque y abra la acción **"Biblioteca: Verificar préstamos vencidos"**.
   * Haga clic en el botón **"Ejecutar Manualmente"** (*Run Manually*).
2. **Resultado Esperado:** Al regresar a *Biblioteca > Préstamos*, el registro modificado ahora aparecerá con una etiqueta roja de estado **"Vencido"** (`overdue`).

### Caso 3: Portal del Socio y Renovaciones
**Objetivo:** Validar la autonomía del usuario público desde el frontend (Website/Portal).
1. **Paso a paso:**
   * Asegúrese de que el usuario "Lector de Prueba" tenga al menos un préstamo activo asignado a su contacto.
   * Abra una ventana de navegación privada (Incógnito).
   * Vaya a `http://localhost:8069/web/login` e inicie sesión como "Lector de Prueba".
   * Vaya a la URL del portal: `http://localhost:8069/my/home`.
   * Haga clic en la tarjeta **"Mis Préstamos"** (Ícono de libro 📚).
   * En la tabla de préstamos, haga clic en el botón azul **"Renovar"**.
2. **Resultado Esperado:** La página se recargará y la "Fecha de Préstamo" del libro se actualizará automáticamente a la fecha actual del sistema.

### Caso 4: Reglas de Seguridad
**Objetivo:** Confirmar que la arquitectura de seguridad de Odoo 19 oculta registros según el nivel de acceso.
1. **Paso a paso:**
   * Asegúrese de tener al menos un libro en estado "Disponible" y otro en estado "Prestado".
   * Manteniendo la sesión iniciada como "Lector de Prueba" (en la ventana de Incógnito), navegue al backend: `http://localhost:8069/web`.
   * Abra la aplicación **Biblioteca** y entre a la vista de "Libros".
2. **Resultado Esperado:** El usuario únicamente podrá ver en la lista los libros con etiqueta verde ("Disponible"). Los libros prestados están restringidos por la base de datos y no son visibles para este rol.

### Caso 5: Integración POS y API REST
**Objetivo:** Demostrar la interoperabilidad del módulo con herramientas externas y aplicaciones nativas.
1. **Paso a paso (API REST):**
   * Abra una nueva pestaña del navegador o una herramienta como Postman.
   * Realice una petición GET a la URL: `http://localhost:8069/api/library/book/<ISBN_DEL_LIBRO>` (Sustituya `<ISBN_DEL_LIBRO>` por un ISBN real de su catálogo).
   * **Resultado Esperado:** Retorno de un objeto JSON estructurado con el ID, Título, ISBN y Estado de disponibilidad.
2. **Paso a paso (Punto de Venta):**
   * Regrese a su sesión de Administrador/Bibliotecario.
   * Abra la aplicación **Punto de Venta** e inicie una **Nueva Sesión** (Caja).
   * Seleccione uno de los libros disponibles (Aparecerá con precio $0.00).
   * Asigne un **Cliente** a la orden.
   * Haga clic en *Pagar*, seleccione el método de pago y *Valide* la orden.
   * Cierre la sesión del POS y vaya a *Biblioteca > Libros*.
   * **Resultado Esperado:** El libro vendido en el POS pasó automáticamente a estado "Prestado" y se generó un nuevo registro en el modelo `library.loan`.