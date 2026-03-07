# GUÍA DE SINCRONIZACIÓN ORANGE [VIRGILIO]

Para que el puente de comunicación funcione con estabilidad extrema entre tu **Livebox 6** y el **Repetidor Mesh**, y para liberar los puertos de **JDownloader**, sigue estos pasos:

## 1. Acceso al Panel Central
- **URL**: [http://192.168.1.1](http://192.168.1.1)
- **Usuario**: admin
- **Contraseña**: Los **primeros 8 caracteres** de tu clave WiFi (pegada detrás del router).

## 2. Sincronización del Repetidor
Si notas que el repetidor no está "en sintonía":
1. Pulsa el botón **WPS** en el frontal de tu Livebox 6.
2. Pulsa el botón **+** en tu repetidor oficial de Orange.
3. Espera a que las luces se estabilicen en verde/lila.

## 3. Ajuste de Windows (Roaming)
Para evitar que tu PC se quede "pegado" al Router cuando estás cerca del Repetidor:
- Administrador de Dispositivos > Adaptadores de Red > Tu WiFi > Propiedades.
- Pestaña **Opciones Avanzadas**.
- Busca **Agresividad de Itinerancia** (Roaming Aggressiveness).
- Cambia el valor a **"Media-Alta"** o **"Alta"**.

## 4. Canales de Radio (Interferencias)
Si notas micro-cortes:
1. En el panel Livebox, ve a **Wi-fi** > **Configuración avanzada**.
2. **2.4 GHz**: Desactiva el modo "Automático" y selecciona el canal **1, 6 o 11**. (Prueba los tres, uno suele estar más libre).
3. **5 GHz**: Selecciona el canal **36, 40, 44 o 48** para máxima compatibilidad y estabilidad.

## 5. Apertura de Puertos (NAT/PAT)
Desde el panel de Livebox, selecciona tu PC y activa **Asignación de IP estática** para que las reglas de puertos no se rompan al reiniciar.
