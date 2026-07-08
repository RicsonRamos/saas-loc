import io

import qrcode

from app.core.config import settings


def url_publica_veiculo(codigo_publico: str) -> str:
    return f"{settings.frontend_base_url}/veiculo/public/{codigo_publico}"


def gerar_qrcode_png(dados: str) -> bytes:
    """Gera o QR code sob demanda — não é persistido, sempre reflete o código atual."""
    imagem = qrcode.make(dados)
    buffer = io.BytesIO()
    imagem.save(buffer, format="PNG")
    return buffer.getvalue()
