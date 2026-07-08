import boto3
from botocore.client import BaseClient
from botocore.config import Config
from botocore.exceptions import ClientError

from app.core.config import settings

BUCKETS = ("veiculos", "documentos", "checklists", "anexos")

_client: BaseClient | None = None

# Timeout curto: se o storage estiver indisponível, falhar rápido em vez de
# travar startup/requests.
_CLIENT_CONFIG = Config(
    connect_timeout=2,
    read_timeout=5,
    retries={"max_attempts": 1},
    signature_version="s3v4",
    s3={"addressing_style": "path"},
)


def get_s3_client() -> BaseClient:
    global _client
    if _client is None:
        _client = boto3.client(
            "s3",
            endpoint_url=settings.storage_endpoint,
            aws_access_key_id=settings.storage_access_key,
            aws_secret_access_key=settings.storage_secret_key,
            region_name=settings.storage_region,
            config=_CLIENT_CONFIG,
        )
    return _client


def garantir_buckets() -> None:
    """Cria os buckets padrão se ainda não existirem. Idempotente."""
    client = get_s3_client()
    for bucket in BUCKETS:
        try:
            client.head_bucket(Bucket=bucket)
        except ClientError:
            client.create_bucket(Bucket=bucket)


def upload_arquivo(bucket: str, chave: str, conteudo: bytes, content_type: str) -> None:
    get_s3_client().put_object(Bucket=bucket, Key=chave, Body=conteudo, ContentType=content_type)


def gerar_url_assinada(bucket: str, chave: str, expira_em_segundos: int = 300) -> str:
    return get_s3_client().generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": chave},
        ExpiresIn=expira_em_segundos,
    )


def remover_arquivo(bucket: str, chave: str) -> None:
    get_s3_client().delete_object(Bucket=bucket, Key=chave)
