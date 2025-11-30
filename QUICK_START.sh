#!/bin/bash
# Gym Membership Management System - Comandos Útiles
# Este archivo documenta los comandos más útiles para trabajar con el sistema

# ============================================================================
# EJECUCIÓN DEL SISTEMA
# ============================================================================

# Ejecutar aplicación interactiva
echo "Ejecutar aplicación interactiva:"
echo "  python gym_membership.py"
echo ""

# Ejecutar pruebas unitarias
echo "Ejecutar pruebas unitarias:"
echo "  python test_gym_membership.py"
echo ""

# Ejecutar demostración
echo "Ejecutar demostración:"
echo "  python demo.py"
echo ""

# ============================================================================
# PRUEBAS ESPECÍFICAS
# ============================================================================

echo "Pruebas específicas:"
echo "  python -m pytest test_gym_membership.py -v                    # Verbose"
echo "  python -m pytest test_gym_membership.py::TestGroupDiscount -v  # Solo grupo"
echo "  python -m pytest test_gym_membership.py -q                    # Quiet"
echo ""

# ============================================================================
# ANÁLISIS DEL CÓDIGO
# ============================================================================

echo "Análisis del código:"
echo "  pylint gym_membership.py                                       # Análisis"
echo "  python -m py_compile gym_membership.py                        # Compilar"
echo "  python -m ast gym_membership.py                               # AST"
echo ""

# ============================================================================
# EJEMPLOS DE USO PROGRAMÁTICO
# ============================================================================

echo "Ejemplos de uso programático:"
echo ""
echo "1. Calcular costo simple:"
python3 << 'EOF'
from gym_membership import GymMembershipManager, PremiumFeatureLevel

manager = GymMembershipManager()
total, breakdown = manager.calculate_total_cost(
    "Premium", 
    ["Personal Training"], 
    2, 
    PremiumFeatureLevel.NONE
)
print(f"   Total: ${total:.2f}")
EOF

echo ""
echo "2. Validar entrada:"
python3 << 'EOF'
from gym_membership import GymMembershipManager

manager = GymMembershipManager()
is_valid, msg = manager.validate_membership_plan("Basic")
print(f"   Valid: {is_valid}")
EOF

echo ""
echo "3. Generar resumen:"
python3 << 'EOF'
from gym_membership import GymMembershipManager, PremiumFeatureLevel

manager = GymMembershipManager()
summary = manager.get_summary(
    "Family",
    ["Personal Training"],
    2,
    PremiumFeatureLevel.EXCLUSIVE_FACILITIES
)
print(summary)
EOF

# ============================================================================
# ESTADÍSTICAS
# ============================================================================

echo ""
echo "Estadísticas del proyecto:"
wc -l gym_membership.py test_gym_membership.py demo.py
echo ""

# ============================================================================
# DOCUMENTACIÓN
# ============================================================================

echo "Archivos de documentación:"
echo "  README.md                    - Guía de usuario"
echo "  SYSTEM_DOCUMENTATION.md      - Documentación técnica"
echo "  IMPLEMENTATION_SUMMARY.md    - Resumen de implementación"
echo "  INDEX.md                     - Índice del proyecto"
echo ""

# ============================================================================
# VERIFICACIÓN FINAL
# ============================================================================

echo "Verificación final:"
python3 << 'EOF'
import sys
from gym_membership import GymMembershipManager

# Verificar que el sistema funciona
manager = GymMembershipManager()
total, _ = manager.calculate_total_cost("Basic", [], 1, None)
print(f"✅ Sistema funcionando correctamente")
print(f"✅ Cálculo de ejemplo: Basic plan = ${total:.2f}")

# Contar tests
import unittest
loader = unittest.TestLoader()
suite = loader.discover('.', pattern='test_*.py')
test_count = suite.countTestCases()
print(f"✅ {test_count} tests disponibles")
EOF

echo ""
echo "======================================================================"
echo "Para más información, ver README.md"
echo "======================================================================"
