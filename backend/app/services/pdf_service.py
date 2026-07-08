import io
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.models.abastecimento import Abastecimento
from app.models.manutencao import Manutencao
from app.models.usuario import Usuario
from app.models.veiculo import Veiculo
from app.schemas.veiculo import HistoricoVeiculoOut
from app.services.qrcode_service import gerar_qrcode_png, url_publica_veiculo
from app.services.veiculo_service import calcular_status_efetivo

LOGO_PATH = Path(__file__).resolve().parent.parent / "static" / "logo.png"

ESTILOS = getSampleStyleSheet()


def _cabecalho_rodape(titulo: str, usuario: Usuario) -> Callable:
    def desenhar(canvas, doc) -> None:
        canvas.saveState()
        largura, altura = A4
        if LOGO_PATH.exists():
            canvas.drawImage(
                str(LOGO_PATH),
                2 * cm,
                altura - 2.6 * cm,
                width=1.8 * cm,
                height=1.8 * cm,
                preserveAspectRatio=True,
                mask="auto",
            )
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(4.2 * cm, altura - 1.6 * cm, titulo)
        canvas.setFont("Helvetica", 8)
        emitido_em = datetime.now(UTC).strftime("%d/%m/%Y %H:%M")
        canvas.drawString(
            4.2 * cm, altura - 2.15 * cm, f"Emitido em {emitido_em} por {usuario.nome}"
        )
        canvas.setStrokeColor(colors.HexColor("#cbd5e1"))
        canvas.line(2 * cm, altura - 2.9 * cm, largura - 2 * cm, altura - 2.9 * cm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#64748b"))
        canvas.drawRightString(largura - 2 * cm, 1.3 * cm, f"Página {doc.page}")
        canvas.restoreState()

    return desenhar


def _gerar_pdf(titulo: str, usuario: Usuario, construir_conteudo: Callable[[], list]) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=3.4 * cm,
        bottomMargin=2 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        title=titulo,
    )
    desenhar = _cabecalho_rodape(titulo, usuario)
    doc.build(construir_conteudo(), onFirstPage=desenhar, onLaterPages=desenhar)
    return buffer.getvalue()


def _tabela(cabecalho: list[str], linhas: list[list[str]]) -> Table:
    tabela = Table([cabecalho, *linhas], repeatRows=1, hAlign="LEFT")
    tabela.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return tabela


def _fd(valor) -> str:
    """Formata data/datetime para dd/mm/aaaa; None vira travessão."""
    if valor is None:
        return "—"
    return valor.strftime("%d/%m/%Y")


def _fm(valor) -> str:
    """Formata valor monetário; None vira travessão."""
    if valor is None:
        return "—"
    return f"R$ {valor:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")


def gerar_ficha_veiculo(
    veiculo: Veiculo, abastecimentos: list[Abastecimento], usuario: Usuario
) -> bytes:
    def construir() -> list:
        story: list = []
        qrcode_png = gerar_qrcode_png(url_publica_veiculo(veiculo.codigo_publico))
        story.append(Image(io.BytesIO(qrcode_png), width=3 * cm, height=3 * cm))
        story.append(Spacer(1, 0.4 * cm))

        story.append(Paragraph("Dados principais", ESTILOS["Heading3"]))
        story.append(
            _tabela(
                ["Placa", "Modelo", "Marca", "Ano", "Status", "KM atual"],
                [
                    [
                        veiculo.placa,
                        veiculo.modelo,
                        veiculo.marca or "—",
                        str(veiculo.ano),
                        calcular_status_efetivo(veiculo),
                        str(veiculo.km_atual),
                    ]
                ],
            )
        )
        story.append(Spacer(1, 0.4 * cm))

        story.append(Paragraph("Documentação", ESTILOS["Heading3"]))
        story.append(
            _tabela(
                ["CRLV", "IPVA vence em", "Licenciamento vence em", "Chassi", "Renavam"],
                [
                    [
                        veiculo.crlv_numero or "—",
                        _fd(veiculo.ipva_vencimento),
                        _fd(veiculo.vencimento_licenciamento),
                        veiculo.chassi or "—",
                        veiculo.renavam or "—",
                    ]
                ],
            )
        )
        story.append(Spacer(1, 0.4 * cm))

        story.append(Paragraph("Seguro", ESTILOS["Heading3"]))
        story.append(
            _tabela(
                ["Seguradora", "Apólice", "Vigência até", "Franquia"],
                [
                    [
                        veiculo.seguradora or "—",
                        veiculo.apolice_numero or "—",
                        _fd(veiculo.vencimento_seguro),
                        _fm(veiculo.seguro_franquia),
                    ]
                ],
            )
        )
        story.append(Spacer(1, 0.4 * cm))

        story.append(Paragraph("Últimos abastecimentos", ESTILOS["Heading3"]))
        if abastecimentos:
            story.append(
                _tabela(
                    ["Data", "Posto", "Litros", "Valor", "KM"],
                    [
                        [
                            _fd(a.data),
                            a.posto or "—",
                            str(a.litros),
                            _fm(a.valor),
                            str(a.km),
                        ]
                        for a in abastecimentos
                    ],
                )
            )
        else:
            story.append(Paragraph("Nenhum abastecimento registrado.", ESTILOS["Normal"]))

        return story

    return _gerar_pdf(f"Ficha do veículo — {veiculo.placa}", usuario, construir)


def gerar_historico_veiculo(
    veiculo: Veiculo, historico: HistoricoVeiculoOut, usuario: Usuario
) -> bytes:
    def construir() -> list:
        story: list = []

        story.append(Paragraph("Locações", ESTILOS["Heading3"]))
        if historico.contratos:
            story.append(
                _tabela(
                    ["Cliente", "Saída", "Devolução", "Status", "Diária"],
                    [
                        [
                            c.cliente_nome,
                            _fd(c.data_inicio),
                            _fd(c.data_fim_real),
                            c.status,
                            _fm(c.valor_diaria),
                        ]
                        for c in historico.contratos
                    ],
                )
            )
        else:
            story.append(Paragraph("Nenhuma locação registrada.", ESTILOS["Normal"]))
        story.append(Spacer(1, 0.4 * cm))

        story.append(Paragraph("Manutenções", ESTILOS["Heading3"]))
        if historico.manutencoes:
            story.append(
                _tabela(
                    ["Data", "Tipo", "KM", "Custo", "Oficina"],
                    [
                        [_fd(m.data), m.tipo, str(m.km), _fm(m.custo), m.oficina or "—"]
                        for m in historico.manutencoes
                    ],
                )
            )
        else:
            story.append(Paragraph("Nenhuma manutenção registrada.", ESTILOS["Normal"]))
        story.append(Spacer(1, 0.4 * cm))

        story.append(Paragraph("Despesas", ESTILOS["Heading3"]))
        if historico.despesas:
            story.append(
                _tabela(
                    ["Data", "Categoria", "Valor", "Observação"],
                    [
                        [_fd(d.data), d.categoria, _fm(d.valor), d.descricao or "—"]
                        for d in historico.despesas
                    ],
                )
            )
        else:
            story.append(Paragraph("Nenhuma despesa registrada.", ESTILOS["Normal"]))

        return story

    return _gerar_pdf(f"Histórico do veículo — {veiculo.placa}", usuario, construir)


def gerar_abastecimentos_veiculo(
    veiculo: Veiculo, abastecimentos: list[Abastecimento], usuario: Usuario
) -> bytes:
    def construir() -> list:
        if not abastecimentos:
            return [Paragraph("Nenhum abastecimento registrado.", ESTILOS["Normal"])]
        return [
            _tabela(
                ["Data", "Posto", "Litros", "Valor", "KM", "Combustível"],
                [
                    [
                        _fd(a.data),
                        a.posto or "—",
                        str(a.litros),
                        _fm(a.valor),
                        str(a.km),
                        a.tipo_combustivel or "—",
                    ]
                    for a in abastecimentos
                ],
            )
        ]

    return _gerar_pdf(f"Abastecimentos — {veiculo.placa}", usuario, construir)


def gerar_manutencoes_veiculo(
    veiculo: Veiculo, manutencoes: list[Manutencao], usuario: Usuario
) -> bytes:
    def construir() -> list:
        if not manutencoes:
            return [Paragraph("Nenhuma manutenção registrada.", ESTILOS["Normal"])]
        return [
            _tabela(
                ["Data", "Tipo", "KM", "Custo", "Oficina", "Descrição"],
                [
                    [
                        _fd(m.data),
                        m.tipo,
                        str(m.km),
                        _fm(m.custo),
                        m.oficina or "—",
                        m.descricao or "—",
                    ]
                    for m in manutencoes
                ],
            )
        ]

    return _gerar_pdf(f"Manutenções — {veiculo.placa}", usuario, construir)
