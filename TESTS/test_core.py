import sys
import os
import pytest
import asyncio

# Sincronización de Rutas para los tests
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ALPHA_CORE'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ALPHA_CORE', 'managers'))

from core_orchestrator import CoreOrchestrator

def test_orchestrator_singleton():
    core1 = CoreOrchestrator()
    core2 = CoreOrchestrator()
    assert core1 is core2

def test_managers_loading():
    core = CoreOrchestrator()
    assert "ai" in core.managers
    assert "auditor" in core.managers
    assert "network" in core.managers

def test_system_auditor_report():
    from system_auditor import SystemAuditor
    auditor = SystemAuditor()
    report = auditor.run_full_audit()
    assert "cpu" in report
    assert "ram" in report
    assert report["system_integrity"] == "INTEGRITY_CERTIFIED"

@pytest.mark.asyncio
async def test_ai_manager_status():
    from ai_manager import AIManager
    ai = AIManager()
    ai.start()
    status = ai.get_status()
    assert status["name"] == "AI_Manager"
    assert "model" in status
