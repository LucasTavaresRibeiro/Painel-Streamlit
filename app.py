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
    "last_updated": "02/11/2026 17:15",
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
        {"id": 1, "etapa": "Fase 1: Discovery, PDD, TDD & Modeler (BPMN)", "janela_4m": "Mês 1 (Até 02/11)", "meta_fast": "Concluído", "orcado_h": 16.0, "atuado_h": 16.0, "status": "Concluído ✅"},
        {"id": 2, "etapa": "Fase 2: Esboço Studio REFramework + Config + Filas", "janela_4m": "Mês 1 (Nov/2026)", "meta_fast": "02/11 a 13/11", "orcado_h": 14.0, "atuado_h": 0.0, "status": "A Iniciar (Sem Acesso)"},
        {"id": 3, "etapa": "Fase 3: Esboço Cascas Modulares ERP (9) & Portal Web (3)", "janela_4m": "Mês 1 (Nov/2026)", "meta_fast": "16/11 a 27/11", "orcado_h": 14.0, "atuado_h": 0.0, "status": "Planejado (Sem Acesso)"},
        {"id": 4, "etapa": "Fase 4: Seletores Reais ERP Desktop (Etapas 02, 03 e 04)", "janela_4m": "Mês 2 (Dez/2026)", "meta_fast": "Dez/2026 (Pós-Acesso)", "orcado_h": 14.0, "atuado_h": 0.0, "status": "Aguard. Acesso ERP"},
        {"id": 5, "etapa": "Fase 5: Seletores Portal Web + Planilha A-K + E-mail", "janela_4m": "Mês 3 (Jan/2027)", "meta_fast": "Dez/2026 - Jan/2027", "orcado_h": 8.0, "atuado_h": 0.0, "status": "Aguard. Acesso Portal"},
        {"id": 6, "etapa": "Fase 6: Testes E2E (CT-01 a CT-12), UAT & Go-Live", "janela_4m": "Mês 3-4 (Jan-Fev/2027)", "meta_fast": "Jan/2027", "orcado_h": 10.0, "atuado_h": 0.0, "status": "A Iniciar"},
    ],
    "pendencias": [
        {"projeto": "FN027 (Horista)", "item": "Retorno dos pontos levantados no PDD v1.1 junto à área de negócio", "status": "Pendente", "Impacto": "Regras finas de exceção"},
        {"projeto": "FN027 (Horista)", "item": "Liberação de acesso ao ambiente de Homologação e ERP R12 (AR/AP)", "status": "Pendente", "Impacto": "Gate 1 em 09/11"},
        {"projeto": "CLT (Corpo Clínico)", "item": "Liberação de credenciais e acesso ao sistema Desktop (Win32)", "status": "Pendente", "Impacto": "Seletores Mês 2 (Esboço segue normal)"},
        {"projeto": "CLT (Corpo Clínico)", "item": "Liberação de acesso ao Portal Web de Divulgação (HML)", "status": "Pendente", "Impacto": "Seletores Etapa 05"},
    ],
    "diario": [
        {"data": "02/11/2026", "projeto": "Ambos", "nota": "Baseline ajustada: FN027 com 120h totais (Hipercare aumentado para 12h) e 6h contabilizadas no PDD até aqui. Próximo passo: iniciar Arquitetura/REFramework/Filas (8h) e Componentes Transversais (5h)."}
    ]
}


def load_data():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except Exception:
            return DEFAULT_DATA.copy()
    return DEFAULT_DATA.copy()


def save_data(data):
    data["last_updated"] = datetime.now().strftime("%d/%m/%Y %H:%M")
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


data = load_data()

st.markdown(
    """
    <style>
    .block-container { padding-top: 1.2rem; padding-bottom: 2rem; }
    div[data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.2);
        padding: 10px 14px;
        border-radius: 10px;
    }
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

tab_visao, tab_horas, tab_pend = st.tabs([
    "📊 Cronogramas (FN027 120h & CLT 4 Meses)",
    "⏱️ Apontar / Revisar Horas",
    "🚧 Pendências PDD, Acessos & Diário",
])

with tab_visao:
    st.subheader("1. Cronograma CLT — Corpo Clínico (`PRC_0100` • Prazo 4 Meses vs. Fast-Track 76h)")
    st.info(
        "**Status 02/11:** Modeler fechado no UiPath (`BPMN`). Sem acesso aos sistemas-alvo no momento. "
        "Iniciando os **esboços no Studio** conforme orientação da liderança. "
        "O prazo oficial é de **4 meses (Nov/2026 a Fev/2027)**, com controle interno em **76h** para entrega antecipada."
    )
    st.dataframe(
        df_clt[["etapa", "janela_4m", "meta_fast", "atuado_h", "orcado_h", "status"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "etapa": "Fase / Etapa (Pipeline 5 Etapas)",
            "janela_4m": "Cronograma Oficial (4 Meses)",
            "meta_fast": "Meta Interna (Fast-Track)",
            "atuado_h": st.column_config.NumberColumn("Atuado (h)", format="%.1f h"),
            "orcado_h": st.column_config.NumberColumn("Meta Interna (h)", format="%.1f h"),
            "status": "Status Atual",
        },
    )

    st.divider()
    st.subheader("2. Cronograma FN027 — Intercompany (`Horista PJ` • 120h Totais c/ Hipercare 12h)")
    st.warning(
        "**Status 02/11:** Contabilizadas **6h de PDD** até o momento. Próximo passo imediato: **Arquitetura RPA, REFramework e Filas (8h)** "
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

with tab_horas:
    st.subheader("⏱️ Atualização Rápida de Horas pelo Celular")
    st.caption("Toque em qualquer célula de **Já Atuado (h)**, **Orçado (h)** ou **Status** para editar e clique em **💾 Salvar Alterações**.")

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
                    "A Iniciar (Sem Acesso)",
                    "Em Andamento (Sem Acesso)",
                    "Planejado (Sem Acesso)",
                    "Aguard. Acesso ERP",
                    "Aguard. Acesso Portal",
                    "Em Desenvolvimento (Com Acesso)",
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
