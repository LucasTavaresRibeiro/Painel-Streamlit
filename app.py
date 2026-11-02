import json
from pathlib import Path
from datetime import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Painel RPA • CLT & FN027 (120h)",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DATA_FILE = Path(__file__).parent / "dados_projetos_rpa.json"

DEFAULT_DATA = {
    "schema_version": 3,
    "last_updated": "02/11/2026 17:30",
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
        {"id": 1, "etapa": "Fase 1: Discovery, PDD, TDD & Modeler 4 Etapas (BPMN)", "janela_4m": "Mês 1 (Até 02/11)", "meta_fast": "Concluído", "orcado_h": 16.0, "atuado_h": 10.0, "status": "Em Desenvolvimento (Sem Acesso)"},
        {"id": 2, "etapa": "Fase 2: Esboço Etapa 01 (Disp_CFM) + REFramework + Config + Testes", "janela_4m": "Mês 1 (Nov/2026)", "meta_fast": "02/11 a 13/11", "orcado_h": 14.0, "atuado_h": 0.0, "status": "Em Andamento (Sem Acesso)"},
        {"id": 3, "etapa": "Fase 3: Esboço Etapas 02, 03 (ERP) e 04 (Portal) + Testes", "janela_4m": "Mês 1 (Nov/2026)", "meta_fast": "16/11 a 27/11", "orcado_h": 14.0, "atuado_h": 0.0, "status": "Planejado (Sem Acesso)"},
        {"id": 4, "etapa": "Fase 4: Seletores Reais ERP Desktop (Etapas 02 e 03)", "janela_4m": "Mês 2 (Dez/2026)", "meta_fast": "Dez/2026 (Pós-Acesso)", "orcado_h": 14.0, "atuado_h": 0.0, "status": "Aguard. Acesso ERP"},
        {"id": 5, "etapa": "Fase 5: Seletores Portal Web (Etapa 04) + Planilha A-K", "janela_4m": "Mês 3 (Jan/2027)", "meta_fast": "Dez/2026 - Jan/2027", "orcado_h": 8.0, "atuado_h": 0.0, "status": "Aguard. Acesso Portal"},
        {"id": 6, "etapa": "Fase 6: Testes E2E (CT-01 a CT-12), UAT & Go-Live", "janela_4m": "Mês 3-4 (Jan-Fev/2027)", "meta_fast": "Jan/2027", "orcado_h": 10.0, "atuado_h": 0.0, "status": "A Iniciar"},
    ],
    "pendencias": [
        {"projeto": "FN027 (Horista)", "item": "Retorno dos pontos levantados no PDD v1.1 junto à área de negócio", "status": "Pendente", "Impacto": "Regras finas de exceção"},
        {"projeto": "FN027 (Horista)", "item": "Liberação de acesso ao ambiente de Homologação e ERP R12 (AR/AP)", "status": "Pendente", "Impacto": "Gate 1 em 09/11"},
        {"projeto": "CLT (Corpo Clínico)", "item": "Liberação de credenciais e acesso ao sistema Desktop (Win32)", "status": "Pendente", "Impacto": "Seletores Mês 2 (Esboço segue normal)"},
        {"projeto": "CLT (Corpo Clínico)", "item": "Liberação de acesso ao Portal Web de Divulgação (HML)", "status": "Pendente", "Impacto": "Seletores Etapa 04"},
    ],
    "diario": [
        {"data": "02/11/2026", "projeto": "Ambos", "nota": "Baseline ajustada: FN027 em 120h totais (Hipercare 12h) com 6h PDD contabilizadas. CLT com esboço de desenvolvimento e testes apartados nas 4 Etapas do Modeler (10h/76h)."}
    ]
}


def load_data():
    if DATA_FILE.exists():
        try:
            saved = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            # Atualiza automaticamente para schema_version 3 (120h com Hipercare 12h) se vier de versão anterior
            if saved.get("schema_version", 1) < 3:
                saved_clt_acted = {r["id"]: r["atuado_h"] for r in saved.get("clt_tasks", [])}
                new_data = json.loads(json.dumps(DEFAULT_DATA))
                for r in new_data["clt_tasks"]:
                    if r["id"] in saved_clt_acted:
                        r["atuado_h"] = saved_clt_acted[r["id"]]
                save_data(new_data)
                return new_data
            return saved
        except Exception:
            return json.loads(json.dumps(DEFAULT_DATA))
    return json.loads(json.dumps(DEFAULT_DATA))


def save_data(data):
    data["schema_version"] = 3
    data["last_updated"] = datetime.now().strftime("%d/%m/%Y %H:%M")
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


data = load_data()

# CSS calibrado para reproduzir em 100% de zoom a proporção exata de 70% de zoom do navegador
st.markdown(
    """
    <style>
    /* Escala tipográfica compacta (equivalente a 70% de zoom nativo em 100%) */
    html, body, [class*="css"] {
        font-size: 12.5px !important;
    }
    .block-container {
        padding-top: 0.8rem !important;
        padding-bottom: 1.2rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 98% !important;
    }
    h1 {
        font-size: 1.45rem !important;
        line-height: 1.8rem !important;
        margin-bottom: 0.1rem !important;
        padding-bottom: 0 !important;
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
    /* Cards de KPI compactos como no print de 70% */
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
    /* Abas e Alertas compactos */
    button[data-baseweb="tab"] p {
        font-size: 0.78rem !important;
    }
    div[data-testid="stAlert"] p {
        font-size: 0.76rem !important;
    }
    /* Tabela Visual Estilo FN027 */
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

col1, col2, col3, col4 = st.columns(4)
col1.metric("🟣 FN027 (Horista)", f"{fn_atuado:.0f}h / {fn_orcado:.0f}h", f"Restam {fn_restante:.0f}h (Hipercare 12h)")
col2.metric("💰 FN027 Acumulado", f"R$ {fn_valor_atuado:,.2f}", f"Total: R$ {fn_valor_total:,.2f} (R$ {taxa:.0f}/h)")
col3.metric("🔵 CLT (Corpo Clínico)", f"{clt_atuado:.0f}h / {clt_orcado:.0f}h", f"Restam {clt_restante:.0f}h (Controle Interno)")
col4.metric("🗓️ Prazo Oficial CLT", "4 Meses (Nov–Fev)", "Meta Fast-Track: Jan/2027")

tab_visao, tab_modeler, tab_horas, tab_pend = st.tabs([
    "📊 Cronogramas (FN027 120h & CLT 4 Meses)",
    "🧩 Esboço Modeler 4 Etapas & Testes",
    "⏱️ Apontar / Revisar Horas",
    "🚧 Pendências PDD, Acessos & Diário",
])

with tab_visao:
    st.subheader("1. Cronograma CLT — Corpo Clínico (`PRC_0100` • Prazo 4 Meses vs. Fast-Track 76h)")
    st.info(
        "**Status 02/11:** Modeler fechado no UiPath (`BPMN` em 4 Etapas). Sem acesso aos sistemas-alvo no momento. "
        "Iniciando os **esboços de desenvolvimento e testes no Modeler/Studio** conforme orientação da liderança. "
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

    # Cronograma Visual do CLT no mesmo estilo de grade do FN027
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
        "**Status 02/11:** Contabilizadas **6h de PDD** até o momento (`R$ 300,00`). Próximo passo imediato: **Arquitetura RPA, REFramework e Filas (8h)** "
        "seguido dos **Componentes Transversais (5h)**."
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
    st.subheader("⏱️ Atualização Rápida de Horas")
    st.caption("Edite **Já Atuado (h)**, **Orçado (h)** ou **Status** e clique em **💾 Salvar Alterações de Horas**.")

    st.markdown("#### 🟣 FN027 — Intercompany (120h Totais • Hipercare 12h)")
    edited_fn = st.data_editor(
        df_fn,
        use_container_width=True,
        hide_index=True,
        key="editor_fn",
        column_config={
            "id": None,
            "etapa": st.column_config.TextColumn("Macroatividade", disabled=True),
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
        },
    )

    st.markdown("#### 🔵 CLT — Corpo Clínico (`PRC_0100` • Controle Interno 76h / 4 Meses)")
    edited_clt = st.data_editor(
        df_clt,
        use_container_width=True,
        hide_index=True,
        key="editor_clt",
        column_config={
            "id": None,
            "etapa": st.column_config.TextColumn("Fase / Etapa", disabled=True),
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
        },
    )

    c_save, c_dl = st.columns(2)
    if c_save.button("💾 Salvar Alterações de Horas", type="primary", use_container_width=True):
        data["fn027_tasks"] = edited_fn.to_dict(orient="records")
        data["clt_tasks"] = edited_clt.to_dict(orient="records")
        save_data(data)
        st.success("Horas e status salvos com sucesso! Recarregando indicadores...")
        st.rerun()

    c_dl.download_button(
        "📥 Baixar Backup JSON (Celular/PC)",
        data=json.dumps(data, ensure_ascii=False, indent=2),
        file_name=f"backup_horas_rpa_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json",
        use_container_width=True,
    )

with tab_pend:
    st.subheader("🚧 Gestão de Bloqueios (Acessos & PDD FN027)")
    df_pend = pd.DataFrame(data["pendencias"])
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
        },
    )
    if st.button("💾 Salvar Pendências", use_container_width=True):
        data["pendencias"] = edited_pend.to_dict(orient="records")
        save_data(data)
        st.success("Lista de pendências atualizada!")
        st.rerun()

    st.divider()
    st.subheader("📝 Diário de Bordo & Atualizações Rápidas")
    with st.form("novo_log"):
        c_proj, c_nota = st.columns([1, 3])
        proj_sel = c_proj.selectbox("Projeto", ["Ambos", "FN027 (Horista)", "CLT (Corpo Clínico)"])
        nota_txt = c_nota.text_input("O que foi feito / atualizado hoje?")
        submitted = st.form_submit_button("➕ Registrar no Diário")
        if submitted and nota_txt.strip():
            data["diario"].insert(0, {
                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "projeto": proj_sel,
                "nota": nota_txt.strip(),
            })
            save_data(data)
            st.success("Registro adicionado!")
            st.rerun()

    for entry in data.get("diario", []):
        st.markdown(f"- **`{entry['data']}` [{entry['projeto']}]**: {entry['nota']}")
