import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Painel RPA • CLT & FN027 (120h)",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

TZ_BR = timezone(timedelta(hours=-3))

def now_br_str():
    return datetime.now(TZ_BR).strftime("%d/%m/%Y %H:%M")

DATA_FILE = Path(__file__).parent / "dados_projetos_rpa.json"

DEFAULT_DATA = {
    "schema_version": 4,
    "last_updated": "03/11/2026 18:06",
    "taxa_horaria_fn027": 50.0,
    "fn027_tasks": [
        {"id": 1, "etapa": "1. Levantamento Legado & PDD v1.1", "periodo": "Sem 1 (27-30/10)", "orcado_h": 6.0, "atuado_h": 6.0, "status": "Concluído (Aguard. Pontos)", "depende_acesso": False},
        {"id": 2, "etapa": "2. Arquitetura RPA (REFramework, Config e Filas)", "periodo": "Sem 2 (02-03/11)", "orcado_h": 8.0, "atuado_h": 0.0, "status": "A Iniciar (02/11)", "depende_acesso": False},
        {"id": 3, "etapa": "3. Componentes Transversais (API, Alertas, Erros)", "periodo": "Sem 2 (02-03/11)", "orcado_h": 5.0, "atuado_h": 0.0, "status": "A Iniciar (02/11)", "depende_acesso": False},
        {"id": 4, "etapa": "4. Geração NDs - Leitura e Apuração", "periodo": "Sem 2 (03-04/11)", "orcado_h": 10.0, "atuado_h": 0.0, "status": "Planejado Sem. 2", "depende_acesso": False},
        {"id": 5, "etapa": "5. Geração NDs - Montagem Aviso Débito", "periodo": "Sem 2 (04-05/11)", "orcado_h": 10.0, "atuado_h": 0.0, "status": "Planejado Sem. 2", "depende_acesso": False},
        {"id": 6, "etapa": "6. Leitura NDs Aprovadas e DE-PARA", "periodo": "Sem 2-3 (05-09/11)", "orcado_h": 6.0, "atuado_h": 0.0, "status": "Planejado Sem. 2", "depende_acesso": False},
        {"id": 7, "etapa": "7. Controle Idempotência e Retry", "periodo": "Sem 2-3 (05-09/11)", "orcado_h": 4.0, "atuado_h": 0.0, "status": "Planejado Sem. 2", "depende_acesso": False},
        {"id": 8, "etapa": "8. ERP R12 - Login, Resp. e JNLP", "periodo": "Sem 3 (09-11/11)", "orcado_h": 8.0, "atuado_h": 0.0, "status": "Bloqueado (Sem Acesso)", "depende_acesso": True},
        {"id": 9, "etapa": "9. ERP R12 - Módulo AR (Transações)", "periodo": "Sem 3 (09-11/11)", "orcado_h": 12.0, "atuado_h": 0.0, "status": "Bloqueado (Sem Acesso)", "depende_acesso": True},
        {"id": 10, "etapa": "10. ERP R12 - Módulo AP (NFF)", "periodo": "Sem 3 (11-13/11)", "orcado_h": 12.0, "atuado_h": 0.0, "status": "Bloqueado (Sem Acesso)", "depende_acesso": True},
        {"id": 11, "etapa": "11. Planilha Controle e Relatório.xlsx", "periodo": "Sem 3-4 (13-16/11)", "orcado_h": 5.0, "atuado_h": 0.0, "status": "A Iniciar", "depende_acesso": False},
        {"id": 12, "etapa": "12. Pós-processamento ND (Mover + PDF)", "periodo": "Sem 3-4 (13-16/11)", "orcado_h": 4.0, "atuado_h": 0.0, "status": "A Iniciar", "depende_acesso": False},
        {"id": 13, "etapa": "13. Tratamento de Exceções (BE/SE)", "periodo": "Sem 4 (16-17/11)", "orcado_h": 6.0, "atuado_h": 0.0, "status": "A Iniciar", "depende_acesso": False},
        {"id": 14, "etapa": "14. Testes Integrados", "periodo": "Sem 4 (16-17/11)", "orcado_h": 6.0, "atuado_h": 0.0, "status": "A Iniciar", "depende_acesso": True},
        {"id": 15, "etapa": "15. Deploy e Agendamentos Orchestrator", "periodo": "Sem 4-5 (18-23/11)", "orcado_h": 2.0, "atuado_h": 0.0, "status": "A Iniciar", "depende_acesso": True},
        {"id": 16, "etapa": "16. Homologação Assistida (UAT)", "periodo": "Sem 4-5 (18-23/11)", "orcado_h": 4.0, "atuado_h": 0.0, "status": "Marco UAT 24/11", "depende_acesso": True},
        {"id": 17, "etapa": "17. Hipercare (Produção Assistida - Aumentado)", "periodo": "Sem 5 (23-27/11)", "orcado_h": 12.0, "atuado_h": 0.0, "status": "Planejado Sem. 5", "depende_acesso": True},
    ],
    "clt_tasks": [
        {"id": 1, "etapa": "Fase 1: Discovery, PDD, TDD & Modeler 4 Etapas (BPMN)", "janela_4m": "Mês 1 (Até 02/11)", "meta_fast": "Concluído", "orcado_h": 16.0, "atuado_h": 10.0, "status": "Em Desenvolvimento (Com Acesso)"},
        {"id": 2, "etapa": "Fase 2: Esboço Etapa 01 (Disp_CFM) + REFramework + Config + Testes", "janela_4m": "Mês 1 (Nov/2026)", "meta_fast": "02/11 a 13/11", "orcado_h": 14.0, "atuado_h": 0.0, "status": "Em Andamento (Sem Acesso)"},
        {"id": 3, "etapa": "Fase 3: Esboço Etapas 02, 03 (ERP) e 04 (Portal) + Testes", "janela_4m": "Mês 1 (Nov/2026)", "meta_fast": "16/11 a 27/11", "orcado_h": 14.0, "atuado_h": 0.0, "status": "Planejado (Sem Acesso)"},
        {"id": 4, "etapa": "Fase 4: Seletores Reais ERP Desktop (Etapas 02 e 03)", "janela_4m": "Mês 2 (Dez/2026)", "meta_fast": "Dez/2026 (Pós-Acesso)", "orcado_h": 14.0, "atuado_h": 0.0, "status": "Em Desenvolvimento (Com Acesso)"},
        {"id": 5, "etapa": "Fase 5: Seletores Portal Web (Etapa 04) + Planilha A-K", "janela_4m": "Mês 3 (Jan/2027)", "meta_fast": "Dez/2026 - Jan/2027", "orcado_h": 8.0, "atuado_h": 0.0, "status": "Aguard. Acesso Portal"},
        {"id": 6, "etapa": "Fase 6: Testes E2E (CT-01 a CT-12), UAT & Go-Live", "janela_4m": "Mês 3-4 (Jan-Fev/2027)", "meta_fast": "Jan/2027", "orcado_h": 10.0, "atuado_h": 0.0, "status": "A Iniciar"},
    ],
    "pendencias": [
        {"projeto": "FN027 (Horista)", "item": "Retorno dos pontos levantados no PDD v1.1 junto à área de negócio", "status": "Em Andamento", "Impacto": "Regras finas de exceção"},
        {"projeto": "FN027 (Horista)", "item": "Liberação de acesso ao ambiente de Homologação e ERP R12 (AR/AP)", "status": "Em Andamento", "Impacto": "Gate 1 em 09/11"},
        {"projeto": "CLT (Corpo Clínico)", "item": "Liberação de credenciais e acesso ao sistema Desktop (Win32)", "status": "Resolvido ✅", "Impacto": "Seletores Mês 2 (Esboço segue normal)"},
        {"projeto": "CLT (Corpo Clínico)", "item": "Liberação de acesso ao Portal Web de Divulgação (HML)", "status": "Em Andamento", "Impacto": "Seletores Etapa 04"},
    ],
    "diario": [
        {"data": "03/11/2026 18:04", "projeto": "FN027 (Horista)", "nota": "Revisões em relação ao PDD. Faltando pontos com João Buso e código do Fortra para avançarmos."},
        {"data": "02/11/2026 17:30", "projeto": "Ambos", "nota": "Baseline ajustada: FN027 em 120h totais (Hipercare 12h) com 6h PDD contabilizadas. CLT com esboço de desenvolvimento e testes apartados nas 4 Etapas do Modeler (10h/76h)."}
    ]
}


def load_data():
    if DATA_FILE.exists():
        try:
            saved = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            if saved.get("schema_version", 1) < 4:
                new_data = json.loads(json.dumps(DEFAULT_DATA))
                save_data(new_data)
                return new_data
            return saved
        except Exception:
            return json.loads(json.dumps(DEFAULT_DATA))
    return json.loads(json.dumps(DEFAULT_DATA))


def save_data(data):
    data["schema_version"] = 4
    data["last_updated"] = now_br_str()
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


data = load_data()

# CSS com a mesma fonte perfeita, porém corrigindo o padding superior para o topo não cortar o título!
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-size: 12.5px !important;
    }
    /* Padding-top ajustado para ficar abaixo da barra superior do Streamlit sem cortar o título */
    .block-container {
        padding-top: 2.8rem !important;
        padding-bottom: 1.5rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 98% !important;
    }
    h1 {
        font-size: 1.45rem !important;
        line-height: 1.45 !important;
        margin-top: 0 !important;
        margin-bottom: 0.15rem !important;
        padding-top: 0.2rem !important;
    }
    h2, h3 {
        font-size: 1.05rem !important;
        line-height: 1.4rem !important;
        margin-top: 0.4rem !important;
        margin-bottom: 0.25rem !important;
    }
    h4 {
        font-size: 0.92rem !important;
        margin-top: 0.3rem !important;
        margin-bottom: 0.2rem !important;
    }
    p, li, .stCaption, [data-testid="stCaptionContainer"] {
        font-size: 0.78rem !important;
    }
    div[data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.07);
        border: 1px solid rgba(128, 128, 128, 0.18);
        padding: 8px 12px !important;
        border-radius: 8px !important;
    }
    div[data-testid="stMetricLabel"] p {
        font-size: 0.74rem !important;
    }
    div[data-testid="stMetricValue"] > div {
        font-size: 1.35rem !important;
        line-height: 1.6rem !important;
    }
    div[data-testid="stMetricDelta"] > div {
        font-size: 0.68rem !important;
    }
    button[data-baseweb="tab"] p {
        font-size: 0.78rem !important;
    }
    div[data-testid="stAlert"] p {
        font-size: 0.76rem !important;
    }
    .gantt-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 11px;
        margin-top: 4px;
        margin-bottom: 10px;
    }
    .gantt-table th {
        background-color: #164e63;
        color: #ffffff;
        padding: 4px 6px;
        border: 1px solid rgba(128,128,128,0.3);
        text-align: center;
        font-weight: 600;
    }
    .gantt-table td {
        padding: 3px 6px;
        border: 1px solid rgba(128,128,128,0.22);
        text-align: center;
    }
    .gantt-table td.act-name {
        text-align: left;
        font-weight: 500;
        min-width: 220px;
    }
    .bar-done { background-color: #10b981; border-radius: 3px; height: 14px; }
    .bar-now  { background-color: #3b82f6; border-radius: 3px; height: 14px; }
    .bar-wait { background-color: #f59e0b; border-radius: 3px; height: 14px; }
    .bar-uat  { background-color: #8b5cf6; border-radius: 3px; height: 14px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🤖 Central Mobile RPA — CLT (Corpo Clínico) & FN027 (120h)")
st.caption(f"📅 Início: **02 de Novembro de 2026** • Última atualização salva: `{data['last_updated']}`")

df_fn = pd.DataFrame(data["fn027_tasks"])
df_clt = pd.DataFrame(data["clt_tasks"])

fn_atuado = float(df_fn["atuado_h"].sum())
fn_orcado = float(df_fn["orcado_h"].sum())
fn_restante = max(0.0, fn_orcado - fn_atuado)
taxa = float(data.get("taxa_horaria_fn027", 50.0))
fn_valor_atuado = fn_atuado * taxa
fn_valor_total = fn_orcado * taxa

clt_atuado = float(df_clt["atuado_h"].sum())
clt_orcado = float(df_clt["orcado_h"].sum())
clt_restante = max(0.0, clt_orcado - clt_atuado)

# Formatação sem dois símbolos '$' na mesma string para evitar que o Streamlit interprete como LaTeX
fn_val_atuado_str = f"R$ {fn_valor_atuado:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
fn_val_total_str = f"R$ {fn_valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

col1, col2, col3, col4 = st.columns(4)
col1.metric("🟣 FN027 (Horista)", f"{fn_atuado:g}h / {fn_orcado:g}h", f"Restam {fn_restante:g}h (Hipercare 12h)")
col2.metric("💰 FN027 Acumulado", fn_val_atuado_str, f"Total: {fn_val_total_str} ({taxa:.0f}/h)")
col3.metric("🔵 CLT (Corpo Clínico)", f"{clt_atuado:g}h / {clt_orcado:g}h", f"Restam {clt_restante:g}h (Controle Interno)")
col4.metric("🗓️ Prazo Oficial CLT", "4 Meses (Nov–Fev)", "Meta Fast-Track: Jan/2027")

tab_visao, tab_modeler, tab_horas, tab_pend = st.tabs([
    "📊 Cronogramas (FN027 120h & CLT 4 Meses)",
    "🧩 Esboço Modeler 4 Etapas & Testes",
    "⏱️ Apontar / Editar / Zerar Horas",
    "🚧 Pendências PDD, Acessos & Diário",
])

with tab_visao:
    st.subheader("1. Cronograma CLT — Corpo Clínico (`PRC_0100` • Prazo 4 Meses vs. Fast-Track 76h)")
    st.info(
        "**Status Atual:** Modeler fechado no UiPath (`BPMN` em 4 Etapas). Acesso ao sistema Desktop (Win32) liberado ✅. "
        "Iniciando os **esboços de desenvolvimento e testes no Modeler/Studio**. "
        "Prazo oficial de **4 meses (Nov/2026 a Fev/2027)**, com controle interno em **76h**."
    )
    st.dataframe(
        df_clt[["etapa", "janela_4m", "meta_fast", "atuado_h", "orcado_h", "status"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "etapa": "Fase / Etapa (Pipeline 4 Etapas Modeler)",
            "janela_4m": "Cronograma Oficial (4 Meses)",
            "meta_fast": "Meta Interna (Fast-Track)",
            "atuado_h": st.column_config.NumberColumn("Atuado (h)", format="%.1f h"),
            "orcado_h": st.column_config.NumberColumn("Meta Interna (h)", format="%.1f h"),
            "status": "Status Atual",
        },
    )

    st.markdown("#### 🗓️ Cronograma Visual (Estilo FN027) — RPA Corpo Clínico (4 Meses / Semanas S1 a S16)")
    clt_weeks = [f"S{i}" for i in range(1, 17)]
    clt_visual_rows = [
        ("Assessment, PDD, TDD & Modeler (4 Etapas)", ["S1"], "bar-done"),
        ("Esboço Modeler (INIT/PROCESS/END) + Testes", ["S1", "S2"], "bar-now"),
        ("Etapa 01 (Disp_CFM): Esboço Studio + Testes CT-03/04/05/08", ["S1", "S2", "S3"], "bar-now"),
        ("Etapa 02 (Perf_ERP_Validacoes): Esboço + Testes CT-06/07/09", ["S2", "S3"], "bar-now"),
        ("Etapa 03 (Perf_ERP_Cad_Vinculo): Esboço + Testes CT-01/02", ["S3", "S4"], "bar-now"),
        ("Etapa 04 (Perf_Portal): Esboço + Planilha A-K + Testes CT-10/12", ["S4"], "bar-now"),
        ("Seletores Reais ERP Desktop (Etapa 02 - Consulta PJ)", ["S5", "S6"], "bar-wait"),
        ("Seletores Reais ERP Desktop (Etapa 03 - PF, Vínculo e Modais)", ["S6", "S7", "S8"], "bar-wait"),
        ("Seletores Reais Portal Web (Etapa 04 - Divulgação)", ["S9", "S10"], "bar-wait"),
        ("Testes Integrados E2E (CT-01 a CT-12) com Massa HML", ["S10", "S11"], "bar-uat"),
        ("Homologação Assistida (UAT) & Deploy (Meta Fast-Track)", ["S11", "S12", "S13"], "bar-uat"),
        ("Operação Assistida (Hypercare) & Janela Contratual Final", ["S13", "S14", "S15", "S16"], "bar-uat"),
    ]
    html_clt = '<table class="gantt-table"><thead><tr><th rowspan="2">Atividade / Etapa (CLT)</th>'
    html_clt += '<th colspan="4">Mês 1: Novembro/26</th><th colspan="4">Mês 2: Dezembro/26</th><th colspan="4">Mês 3: Janeiro/27</th><th colspan="4">Mês 4: Fevereiro/27</th></tr><tr>'
    for w in clt_weeks:
        style_th = ' style="background:#2563eb;"' if w == "S1" else ""
        html_clt += f"<th{style_th}>{w}</th>"
    html_clt += "</tr></thead><tbody>"
    for label, active_w, cls in clt_visual_rows:
        html_clt += f'<tr><td class="act-name">{label}</td>'
        for w in clt_weeks:
            cell = f'<div class="{cls}"></div>' if w in active_w else ""
            html_clt += f"<td>{cell}</td>"
        html_clt += "</tr>"
    html_clt += "</tbody></table>"
    st.markdown(html_clt, unsafe_allow_html=True)

    st.divider()
    st.subheader("2. Cronograma FN027 — Intercompany (`Horista PJ` • 120h Totais c/ Hipercare 12h)")
    st.warning(
        "**Status Atual:** Contabilizadas **6h de PDD** até o momento (`R$ 300,00`). Aguardando pontos com João Buso e código do Fortra para avançarmos. "
        "Próximo passo imediato: **Arquitetura RPA, REFramework e Filas (8h)** seguido dos **Componentes Transversais (5h)**."
    )
    st.dataframe(
        df_fn[["etapa", "periodo", "atuado_h", "orcado_h", "status"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "etapa": "Macroatividade FN027 (17 itens)",
            "periodo": "Janela no Cronograma",
            "atuado_h": st.column_config.NumberColumn("Já Atuado (h)", format="%.1f h"),
            "orcado_h": st.column_config.NumberColumn("Orçado (h)", format="%.1f h"),
            "status": "Status",
        },
    )

with tab_modeler:
    st.subheader("🧩 Esboço de Desenvolvimento & Testes nas 4 Etapas do Modeler (`PRC_0100`)")
    st.caption("Atividades estruturadas nas raias `INIT`, `PROCESS` e `END PROCESS` com casos de teste (`CT-01` a `CT-12`) apartados por etapa.")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown("#### 1️⃣ Etapa 01: `Disp_CFM`")
        st.markdown(
            "- **Fila:** `Queue_0100.01` ➔ `02`\n"
            "- **INIT:** `InitAllSettings` + Ler Planilha Entrada e Validar Schema (11 colunas).\n"
            "- **PROCESS:** Triagem CRM vs. Não-Médico (Bypass) ➔ Consultar Portal CFM (Regular + Especialidade) ➔ `Add Queue Item`.\n"
            "- **END:** Fechar navegador e gravar log.\n"
            "- 🧪 **Testes:** `CT-03` (`BRE-001` Schema), `CT-04` (`BRE-002` CRM Cancelado), `CT-05` (`BRE-002` Esp. Divergente), `CT-08` (Bypass Não-Médico), `CT-11` (`SYS-003`)."
        )
    with m2:
        st.markdown("#### 2️⃣ Etapa 02: `Perf_Validacoes`")
        st.markdown(
            "- **Fila:** `Queue_0100.02` ➔ `03`\n"
            "- **INIT:** Login ERP Desktop Win32 + `Get Transaction`.\n"
            "- **PROCESS:** Busca PJ via `F2` (CNPJ) ➔ Validar Ativo/Bloqueado ➔ Validar Especialidade PJ ➔ Coletar Metadados (Abas 1, 5, 7, 8, 11) ➔ `Add Queue Item`.\n"
            "- **END:** `SetTransactionStatus` + Logout.\n"
            "- 🧪 **Testes:** `CT-06` (`BRE-003` PJ Inexistente), `CT-07` (`BRE-004` Sem Especialidade), `CT-09` (`SYS-001` Timeout Login)."
        )
    with m3:
        st.markdown("#### 3️⃣ Etapa 03: `Perf_Cad_Vinculo`")
        st.markdown(
            "- **Fila:** `Queue_0100.03` ➔ `04`\n"
            "- **INIT:** Validar Sessão ERP + `Get Transaction`.\n"
            "- **PROCESS:** Consultar CPF (`F2`): Cadastrar PF (Abas 1, 4, 9 Conta `21199319901`, Aba 5 CRM) ou obter código existente ➔ Vincular Aba 6 PJ (`Insert`) ➔ Abas 7/8/11 PF ➔ Modais Importação (`13637`/`90d`) e Divulgação.\n"
            "- **END:** `SetTransactionStatus` + Logout.\n"
            "- 🧪 **Testes:** `CT-01` (Médico Novo), `CT-02` (Médico Existente), 13 constantes `Config.xlsx`."
        )
    with m4:
        st.markdown("#### 4️⃣ Etapa 04: `Perf_SAUDI`")
        st.markdown(
            "- **Fila:** `Queue_0100.04` ➔ Fim\n"
            "- **INIT:** Login Portal Web + `Get Transaction`.\n"
            "- **PROCESS:** Administrar Prestador (`CRM-000000-PR`, Modalidades CRM vs. `SP/SADT`, Glosa=1) ➔ Append Planilha Divulgação Colunas A a K (`RPA-PRC Corpo Clínico`).\n"
            "- **END:** Relatório Consolidado Excel + E-mail Executivo com KPIs.\n"
            "- 🧪 **Testes:** `CT-08` (Modalidade `SP/SADT`), `CT-10` (`SYS-002` Login Portal), `CT-12` (Relatório + E-mail)."
        )

with tab_horas:
    st.subheader("⏱️ Editar, Corrigir ou Zerar Horas Lançadas")
    st.caption(
        "Você pode **digitar qualquer valor** diretamente em **Já Atuado (h)** / **Orçado (h)**, ou marcar a caixinha **🔄 Zerar Horas?** "
        "em uma linha lançada por engano e clicar em **💾 Salvar Alterações de Horas**."
    )

    df_fn_edit = df_fn.copy()
    df_fn_edit["zerar"] = False
    st.markdown("#### 🟣 FN027 — Intercompany (120h Totais • Hipercare 12h)")
    edited_fn = st.data_editor(
        df_fn_edit,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        key="editor_fn",
        column_config={
            "id": None,
            "etapa": st.column_config.TextColumn("Macroatividade"),
            "periodo": st.column_config.TextColumn("Período"),
            "atuado_h": st.column_config.NumberColumn("Já Atuado (h)", min_value=0.0, step=0.5, format="%.1f"),
            "orcado_h": st.column_config.NumberColumn("Orçado (h)", min_value=0.0, step=0.5, format="%.1f"),
            "status": st.column_config.SelectboxColumn(
                "Status",
                options=[
                    "Concluído ✅",
                    "Concluído (Aguard. Pontos)",
                    "A Iniciar (02/11)",
                    "Em Andamento",
                    "Planejado Sem. 2",
                    "Planejado Sem. 5",
                    "Bloqueado (Sem Acesso)",
                    "A Iniciar",
                    "Marco UAT 24/11",
                ],
            ),
            "depende_acesso": st.column_config.CheckboxColumn("Requer ERP?"),
            "zerar": st.column_config.CheckboxColumn("🔄 Zerar Horas?"),
        },
    )

    df_clt_edit = df_clt.copy()
    df_clt_edit["zerar"] = False
    st.markdown("#### 🔵 CLT — Corpo Clínico (`PRC_0100` • Controle Interno 76h / 4 Meses)")
    edited_clt = st.data_editor(
        df_clt_edit,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        key="editor_clt",
        column_config={
            "id": None,
            "etapa": st.column_config.TextColumn("Fase / Etapa"),
            "janela_4m": st.column_config.TextColumn("Prazo 4 Meses"),
            "meta_fast": st.column_config.TextColumn("Meta Fast-Track"),
            "atuado_h": st.column_config.NumberColumn("Já Atuado (h)", min_value=0.0, step=0.5, format="%.1f"),
            "orcado_h": st.column_config.NumberColumn("Orçado Interno (h)", min_value=0.0, step=0.5, format="%.1f"),
            "status": st.column_config.SelectboxColumn(
                "Status",
                options=[
                    "Concluído ✅",
                    "Em Desenvolvimento (Sem Acesso)",
                    "Em Desenvolvimento (Com Acesso)",
                    "A Iniciar (Sem Acesso)",
                    "Em Andamento (Sem Acesso)",
                    "Planejado (Sem Acesso)",
                    "Aguard. Acesso ERP",
                    "Aguard. Acesso Portal",
                    "Em Homologação (UAT)",
                    "A Iniciar",
                ],
            ),
            "zerar": st.column_config.CheckboxColumn("🔄 Zerar Horas?"),
        },
    )

    c_save, c_reset, c_dl = st.columns(3)
    if c_save.button("💾 Salvar Alterações de Horas", type="primary", use_container_width=True):
        fn_records = []
        for idx, r in enumerate(edited_fn.to_dict(orient="records"), start=1):
            if r.get("zerar"):
                r["atuado_h"] = 0.0
            r.pop("zerar", None)
            r["id"] = idx
            fn_records.append(r)

        clt_records = []
        for idx, r in enumerate(edited_clt.to_dict(orient="records"), start=1):
            if r.get("zerar"):
                r["atuado_h"] = 0.0
            r.pop("zerar", None)
            r["id"] = idx
            clt_records.append(r)

        data["fn027_tasks"] = fn_records
        data["clt_tasks"] = clt_records
        save_data(data)
        st.success("Horas salvas e recalculadas com sucesso!")
        st.rerun()

    if c_reset.button("🔄 Restaurar Horas Base (6h FN027 / 10h CLT)", use_container_width=True):
        data["fn027_tasks"] = json.loads(json.dumps(DEFAULT_DATA["fn027_tasks"]))
        data["clt_tasks"] = json.loads(json.dumps(DEFAULT_DATA["clt_tasks"]))
        save_data(data)
        st.success("Horas restauradas para a base padrão!")
        st.rerun()

    c_dl.download_button(
        "📥 Baixar Backup JSON",
        data=json.dumps(data, ensure_ascii=False, indent=2),
        file_name=f"backup_horas_rpa_{datetime.now(TZ_BR).strftime('%Y%m%d_%H%M')}.json",
        mime="application/json",
        use_container_width=True,
    )

with tab_pend:
    st.subheader("🚧 Gestão de Bloqueios (Acessos & PDD FN027)")
    st.caption("Edite qualquer texto/status ou marque **🗑️ Apagar?** para remover uma pendência.")
    df_pend = pd.DataFrame(data["pendencias"])
    df_pend["apagar"] = False
    edited_pend = st.data_editor(
        df_pend,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key="editor_pend",
        column_config={
            "projeto": st.column_config.SelectboxColumn("Projeto", options=["FN027 (Horista)", "CLT (Corpo Clínico)", "Ambos"]),
            "item": st.column_config.TextColumn("Pendência / Ponto Levantado"),
            "status": st.column_config.SelectboxColumn("Status", options=["Pendente", "Em Andamento", "Resolvido ✅"]),
            "Impacto": st.column_config.TextColumn("Impacto no Cronograma"),
            "apagar": st.column_config.CheckboxColumn("🗑️ Apagar?"),
        },
    )
    if st.button("💾 Salvar Pendências / Excluir Marcadas", use_container_width=True):
        kept_pend = []
        for r in edited_pend.to_dict(orient="records"):
            if not r.get("apagar") and str(r.get("item", "")).strip():
                r.pop("apagar", None)
                kept_pend.append(r)
        data["pendencias"] = kept_pend
        save_data(data)
        st.success("Lista de pendências atualizada!")
        st.rerun()

    st.divider()
    st.subheader("📝 Diário de Bordo & Atualizações Rápidas (Adicionar, Editar ou Apagar)")

    # Formulário com clear_on_submit=True para não duplicar notas ao recarregar
    with st.form("novo_log", clear_on_submit=True):
        c_proj, c_nota = st.columns([1, 3])
        proj_sel = c_proj.selectbox("Projeto", ["FN027 (Horista)", "CLT (Corpo Clínico)", "Ambos"])
        nota_txt = c_nota.text_input("O que foi feito / atualizado hoje?")
        submitted = st.form_submit_button("➕ Registrar no Diário")
        if submitted and nota_txt.strip():
            data["diario"].insert(0, {
                "data": now_br_str(),
                "projeto": proj_sel,
                "nota": nota_txt.strip(),
            })
            save_data(data)
            st.success("Registro adicionado ao Diário!")
            st.rerun()

    st.caption("💡 **Para editar um texto ou apagar uma anotação duplicada/errada:** clique diretamente na célula abaixo para corrigir o texto, ou marque a coluna **🗑️ Apagar?** e clique em **💾 Salvar / Apagar Anotações Selecionadas**.")
    df_diario = pd.DataFrame(data.get("diario", []))
    if df_diario.empty:
        df_diario = pd.DataFrame(columns=["data", "projeto", "nota"])
    df_diario["apagar"] = False

    edited_diario = st.data_editor(
        df_diario,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key="editor_diario",
        column_config={
            "data": st.column_config.TextColumn("Data / Hora", width="small"),
            "projeto": st.column_config.SelectboxColumn("Projeto", options=["FN027 (Horista)", "CLT (Corpo Clínico)", "Ambos"], width="small"),
            "nota": st.column_config.TextColumn("Anotação / Registro do Diário (Clique para editar)", width="large"),
            "apagar": st.column_config.CheckboxColumn("🗑️ Apagar?", width="small"),
        },
    )

    if st.button("💾 Salvar Edições / Apagar Anotações Selecionadas no Diário", type="primary", use_container_width=True):
        kept_diario = []
        for r in edited_diario.to_dict(orient="records"):
            if not r.get("apagar") and str(r.get("nota", "")).strip():
                r.pop("apagar", None)
                kept_diario.append(r)
        data["diario"] = kept_diario
        save_data(data)
        st.success("Diário de Bordo atualizado com sucesso!")
        st.rerun()
