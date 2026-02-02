import pytest
import os
from unittest.mock import MagicMock, patch

# 1. DEFINE AS VARIÁVEIS DE AMBIENTE PRIMEIRO
os.environ["GOOGLE_CLOUD_PROJECT"] = "test-project"
os.environ["JWT_SECRET_KEY"] = "star-wars-test-secret-key-long-enough-for-sha256"

# 2. MOCK FIRESTORE ANTES DE QUALQUER IMPORTAÇÃO DO APP
mock_firestore_client_instance = MagicMock()

# Deixa o mock do firestore disponível
firestore_patcher = patch('google.cloud.firestore.Client', return_value=mock_firestore_client_instance)
firestore_patcher.start()

# 3. FORÇA O PATCH DA INSTÂNCIA DO DB NOS MÓDULOS CORE
def force_patch_db():
    try:
        import app.database.core
        import app.database
        app.database.core.db = mock_firestore_client_instance
        app.database.db = mock_firestore_client_instance
    except ImportError:
        pass

@pytest.fixture(scope="session", autouse=True)
def global_mocks():
    force_patch_db()
    yield
    firestore_patcher.stop()

@pytest.fixture
def app():
    from app.main import app as flask_app
    flask_app.config.update({"TESTING": True})
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_db():
    return mock_firestore_client_instance

@pytest.fixture(autouse=True)
def patch_controllers(mock_db):
    # Isto é necessário porque os serviços são instanciados no nível do módulo nos controladores
    from app.user.service import UserService
    from app.favorites.service import FavoriteService
    
    with patch('app.swapi_client.SWAPICacheRepository') as mock_cache_repo:
        # Garante que o cache falhe por padrão em todos os testes E2E
        mock_cache_repo.return_value.get_cached_response.return_value = None
        
        # Create fresh services with the mock_db and the patched SWAPICacheRepository
        test_user_service = UserService(database=mock_db)
        test_favorite_service = FavoriteService(database=mock_db)
        
        with patch('app.auth.controller.user_service', test_user_service), \
             patch('app.favorites.controller.favorite_service', test_favorite_service):
            yield

@pytest.fixture(autouse=True)
def reset_mocks(mock_db):
    mock_db.reset_mock()
    yield
