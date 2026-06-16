from main import MESSAGE_TEMPLATE, build_message


def test_build_message():
    assert build_message("Maria") == "Olá, Maria tudo bem com você?"


def test_message_template_uses_comma_after_ola():
    assert MESSAGE_TEMPLATE == "Olá, {nome} tudo bem com você?"
