import pytest
from Backend.microservices.app.API.v1.shared_microservices.cryptoapi.main import EncryptText, encrypt, decrypt
from pydantic import ValidationError
from termcolor import cprint

# Pruebas para la validación de texto

#@pytest.mark.skip(reason="Esta prueba está deshabilitada temporalmente.")
def test_valid_ascii_text():
    assert EncryptText(text='Hello World') == EncryptText(text='Hello World')

#@pytest.mark.skip(reason="Esta prueba está deshabilitada temporalmente.")
def test_invalid_ascii_text():
    with pytest.raises(ValidationError):
        EncryptText(text='Hello\x00World')

#@pytest.mark.skip(reason="Esta prueba está deshabilitada temporalmente.")
def test_valid_text_with_permitted_characters():
    assert EncryptText(text='Hello, World!') == EncryptText(text='Hello, World!')

#@pytest.mark.skip(reason="Esta prueba está deshabilitada temporalmente.")
"""def test_invalid_text_with_special_characters():
    with pytest.raises(ValidationError):
        EncryptText(text='Hello @#%')
"""

#@pytest.mark.skip(reason="Esta prueba está deshabilitada temporalmente.")
def test_invalid_utf8_text():
    with pytest.raises(ValidationError):
        EncryptText(text='Café')

# Mock para la lógica de encriptación y desencriptación

#@pytest.mark.skip(reason="Esta prueba está deshabilitada temporalmente.")
def test_encrypt():
    # Simulación del comportamiento esperado para pruebas
    mock_text = 'Hello World'
    result = encrypt(mock_text)
    assert isinstance(result, str)  # Verificar que el resultado es de tipo bytes

#@pytest.mark.skip(reason="Esta prueba está deshabilitada temporalmente.")
def test_decrypt():
    # Simulación del comportamiento esperado para pruebas
    encrypted_text = encrypt('Hello World')
    assert isinstance(encrypted_text, str)
    print("\n")
    cprint(encrypted_text, "green", "on_black")
    result = decrypt(encrypted_text)
    cprint(result, "green", "on_black")
    print("\n")
    assert isinstance(result, str)  # Verificar que el resultado es de tipo bytes
    assert result == 'Hello World'

