# Gym Membership Management System

## Descripción General

Sistema completo de gestión de membresías de gimnasio que permite a los usuarios:
- Seleccionar planes de membresía (Basic, Premium, Family)
- Agregar características adicionales (entrenamiento personal, clases grupales, consultoría nutricional)
- Calcular costos con descuentos de grupo y ofertas especiales
- Aplicar recargos por características premium
- Revisar y confirmar su selección

## Características Principales

✅ **Múltiples Planes de Membresía**
- Basic: $29.99
- Premium: $59.99
- Family: $99.99

✅ **Características Adicionales**
- Personal Training: $50.00
- Group Classes: $30.00
- Nutritional Consulting: $40.00

✅ **Sistema de Descuentos**
- Descuento de grupo del 10% para 2+ miembros
- Descuento especial: $20 si costo > $200, $50 si > $400

✅ **Recargos Premium**
- 15% de recargo para características premium exclusivas

✅ **Validación Completa**
- Validación de planes disponibles
- Validación de características
- Validación de número de miembros

✅ **Confirmación del Usuario**
- Resumen detallado de selección
- Desglose completo de costos
- Confirmación antes de finalizar

## Archivos del Proyecto

- `gym_membership.py` - Sistema principal (clases y aplicación)
- `test_gym_membership.py` - Suite completa de pruebas unitarias (100+ casos)
- `SYSTEM_DOCUMENTATION.md` - Documentación detallada del sistema
- `README.md` - Este archivo

## Instalación y Uso

### Requisitos
- Python 3.7 o superior
- Sin dependencias externas

### Ejecutar la Aplicación

```bash
python gym_membership.py
```

Esto inicia la interfaz interactiva de línea de comandos.

### Ejecutar las Pruebas

```bash
# Usando unittest
python test_gym_membership.py

# O usando pytest (si está instalado)
pytest test_gym_membership.py -v
```

## Ejemplo de Flujo de Usuario

```
1. Bienvenida
   ↓
2. Seleccionar plan de membresía
   ↓
3. Ingresar número de miembros
   ↓
4. Seleccionar características adicionales (opcional)
   ↓
5. Seleccionar nivel premium (opcional)
   ↓
6. Ver resumen de costos
   ↓
7. Confirmar o cancelar
   ↓
8. Retorna costo total (entero) o -1 si se cancela
```

## Cálculo de Costos

El cálculo de costos sigue este orden:

1. **Costo Base**: Costo del plan seleccionado
2. **Características**: Suma de costos de características adicionales
3. **Subtotal**: Base + Características
4. **Descuento de Grupo**: 10% si 2+ miembros
5. **Descuento Especial**: $20 (si > $200) o $50 (si > $400)
6. **Recargo Premium**: 15% si hay características premium
7. **Costo Total**: Resultado final

## Ejemplos de Cálculo

### Ejemplo 1: Basic + 1 miembro
```
Base: $29.99
Total: $29 (como entero)
```

### Ejemplo 2: Premium + Personal Training + 2 miembros
```
Base: $59.99
Características: $50.00
Subtotal: $109.99
Descuento grupo (10%): -$11.00
Total: $98 (como entero)
```

### Ejemplo 3: Family + Todas características + 2 miembros + Premium
```
Base: $99.99
Características: $120.00
Subtotal: $219.99
Descuento grupo (10%): -$22.00
Después descuento: $197.99
Recargo premium (15%): +$29.70
Total: $227 (como entero)
```

## Suite de Pruebas

La suite incluye más de 100 casos de prueba que cubren:

- ✅ Validación de planes de membresía
- ✅ Validación de características
- ✅ Validación de número de miembros
- ✅ Cálculo de costos base
- ✅ Cálculo de costos de características
- ✅ Cálculo de descuentos de grupo
- ✅ Cálculo de descuentos especiales
- ✅ Cálculo de recargos premium
- ✅ Cálculo total con combinaciones complejas
- ✅ Generación de resúmenes
- ✅ Casos límite y errores

Ejecutar pruebas:
```bash
python test_gym_membership.py
```

## Supuestos Realizados

1. Los costos están en USD
2. El número de miembros debe estar entre 1 y 10
3. Los descuentos se aplican en orden: grupo → especial → premium (recargo)
4. El recargo premium se aplica al costo DESPUÉS de todos los descuentos
5. El costo final se retorna como entero positivo (o -1 si se cancela)
6. Si se envían características duplicadas, se cuentan múltiples veces
7. Toda entrada se valida antes de procesarse

## Validaciones Implementadas

- ✅ Existencia de plan seleccionado
- ✅ Disponibilidad de plan
- ✅ Existencia de características
- ✅ Disponibilidad de características
- ✅ Rango válido de miembros
- ✅ Tipo de dato correcto
- ✅ Mensajes de error descriptivos

## Valor Retornado

- **Entero positivo**: Costo total de membresía confirmada
- **-1**: Membresía cancelada o datos inválidos

## Estructura del Código

### Clases Principales

- `MembershipType`: Tipos de membresía
- `PremiumFeatureLevel`: Niveles de características premium
- `MembershipPlan`: Estructura de plan de membresía
- `AdditionalFeature`: Estructura de característica adicional
- `MembershipSelection`: Selección del usuario
- `GymMembershipManager`: Lógica de negocio (cálculos, validaciones)
- `GymMembershipApp`: Interfaz de usuario (línea de comandos)

### Funciones Principales

#### GymMembershipManager
- `validate_membership_plan()`: Valida plan
- `validate_features()`: Valida características
- `validate_num_members()`: Valida número de miembros
- `calculate_base_cost()`: Calcula costo base
- `calculate_features_cost()`: Calcula costo de características
- `calculate_group_discount()`: Calcula descuento de grupo
- `calculate_special_offer_discount()`: Calcula descuento especial
- `calculate_premium_surcharge()`: Calcula recargo premium
- `calculate_total_cost()`: Calcula costo total con desglose
- `get_summary()`: Genera resumen formateado

#### GymMembershipApp
- `run()`: Inicia el flujo de la aplicación
- `select_membership_plan()`: Obtiene selección de plan
- `select_additional_features()`: Obtiene selección de características
- `select_num_members()`: Obtiene número de miembros
- `select_premium_level()`: Obtiene nivel premium
- `confirm_membership()`: Solicita confirmación

## Documentación Adicional

Consulte `SYSTEM_DOCUMENTATION.md` para:
- Descripción detallada de características
- Ejemplos completos de cálculo
- Guía de uso de clases
- Extensibilidad del sistema
- Detalles técnicos

## Versión

1.0 - Versión inicial del sistema

## Autor

Sistema de Gestión de Membresías de Gimnasio

---

**Nota**: Esta es una aplicación de demostración educativa. Para uso en producción, se recomienda agregar persistencia de datos, integración con bases de datos y características adicionales de seguridad.
