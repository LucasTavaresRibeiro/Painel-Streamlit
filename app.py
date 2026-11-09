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
    "schema_version": 6,
    "last_updated": "09/11/2026 17:20",
    "taxa_horaria_fn027": 50.0,
    "titulos": {
        "painel_titulo": "🤖 Central Mobile RPA — CLT (Meta Urgente 27/11) & FN027 (120h)",
        "clt_secao": "1. Cronograma CLT — Corpo Clínico (PRC_0100 • Sprint Acelerada: Go-Live 27/11/2026 • 76h)",
        "clt_gantt_titulo": "🗓️ Cronograma Visual Acelerado — RPA Corpo Clínico (Entrega Final: 27/11/2026)",
        "fn_secao": "2. Cronograma FN027 — Intercompany (Horista PJ • 120h Totais c/ Hipercare 12h)",
        "fn_gantt_titulo": "🗓️ Cronograma Visual Dia a Dia — FN027 Intercompany (Semanas 1 a 5 • Outubro e Novembro/2026)",
    },
    "clt_gantt": [
        {"atividade": "1. Discovery, Modeler BPMN (4 Etapas) & Testes (10h)", "periodos": "S1", "cor": "Concluído (Verde)"},
        {"atividade": "2. Etapa 01 (Disp_CFM): REFramework + Leitura CFM + CT-03/04/05/08", "periodos": "S2", "cor": "Em Andamento (Azul)"},
        {"atividade": "3. Etapa 02 (Perf_ERP_Validacoes): Consulta PJ Desktop Win32 + CT-06/07/09", "periodos": "S2, S3", "cor": "Em Andamento (Azul)"},
        {"atividade": "4. Etapa 03 (Perf_ERP_Cad_Vinculo): Cadastro PF, Vínculos, Modais + CT-01/02", "periodos": "S3, S4", "cor": "Em Andamento (Azul)"},
        {"atividade": "5. Etapa 04 (Perf_Portal SAUDI): Divulgação Web + Planilha A-K + CT-10/12", "periodos": "S4", "cor": "Aguardando / Dependente (Amarelo)"},
        {"atividade": "6. Testes Integrados E2E (CT-01 a CT-12) em HML", "periodos": "S4", "cor": "UAT & Hypercare (Roxo)"},
        {"atividade": "7. UAT Assistida, Homologação Formal & GO-LIVE (27/11/2026)", "periodos": "S4", "cor": "UAT & Hypercare (Roxo)"},
        {"atividade": "8. Operação Assistida / Monitoramento (Margem Contratual 4 Meses)", "periodos": "S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16", "cor": "Concluído (Verde)"},
    ],
    "fn027_gantt": [
        {"atividade": "1. Assessment / Criação de PDD (6h concluídas)", "periodos": "27, 28, 29", "cor": "Concluído (Verde)"},
        {"atividade": "Aprovação PDD (Aguardando retorno dos pontos)", "periodos": "30, 2, 3", "cor": "Aguardando / Dependente (Amarelo)"},
        {"atividade": "2 & 3. Arquitetura inicial (RPA 8h) + Transversais (5h)", "periodos": "30, 2, 3, 10, 11", "cor": "Em Andamento (Azul)"},
        {"atividade": "4. Geração das NDs - leitura e apuração (10h)", "periodos": "11, 12", "cor": "Em Andamento (Azul)"},
        {"atividade": "5. Geração das NDs - montagem do Aviso de Débito (10h)", "periodos": "12, 13", "cor": "Em Andamento (Azul)"},
        {"atividade": "6 & 7. Leitura das NDs aprovadas, DE-PARA e idempotência (10h)", "periodos": "13, 16", "cor": "Em Andamento (Azul)"},
        {"atividade": "8 & 9. Oracle EBS R12 - Login e AR Contas a Receber (20h)", "periodos": "16, 17", "cor": "Aguardando / Dependente (Amarelo)"},
        {"atividade": "10. Oracle EBS R12 - AP Contas a Pagar (12h)", "periodos": "18, 19", "cor": "Aguardando / Dependente (Amarelo)"},
        {"atividade": "11 & 12. Planilha de controle, relatório e pós-processamento (9h)", "periodos": "14, 19", "cor": "Em Andamento (Azul)"},
        {"atividade": "13 & 14. Exceções, logs e testes integrados (12h)", "periodos": "19, 21", "cor": "UAT & Hypercare (Roxo)"},
        {"atividade": "15 & 16. Homologação (UAT) e Deploy (6h)", "periodos": "23, 24", "cor": "UAT & Hypercare (Roxo)"},
        {"atividade": "17. Operação assistida / Hipercare (Aumentado: 12h)", "periodos": "24, 25, 26, 27", "cor": "UAT & Hypercare (Roxo)"},
    ],
    "fn027_tasks": [
        {"id": 1, "etapa": "1. Levantamento Legado & PDD v1.1", "periodo": "Sem 1 (27-30/10)", "orcado_h": 6.0, "atuado_h": 6.0, "status": "Concluído (Aguard. Pontos)", "depende_acesso": False},
        {"id": 2, "etapa": "2. Arquitetura RPA (REFramework, Config e Filas)", "periodo": "Sem 2 (10/11)", "orcado_h": 8.0, "atuado_h": 0.0, "status": "Prioridade 10/11 Manhã", "depende_acesso": False},
        {"id": 3, "etapa": "3. Componentes Transversais (API, Alertas, Erros)", "periodo": "Sem 2 (10-11/11)", "orcado_h": 5.0, "atuado_h": 0.0, "status": "A Iniciar (10/11 Noite)", "depende_acesso": False},
        {"id": 4, "etapa": "4. Geração NDs - Leitura e Apuração", "periodo": "Sem 2 (11-12/11)", "orcado_h": 10.0, "atuado_h": 0.0, "status": "Planejado", "depende_acesso": False},
        {"id": 5, "etapa": "5. Geração NDs - Montagem Aviso Débito", "periodo": "Sem 2 (12-13/11)", "orcado_h": 10.0, "atuado_h": 0.0, "status": "Planejado", "depende_acesso": False},
        {"id": 6, "etapa": "6. Leitura NDs Aprovadas e DE-PARA", "periodo": "Sem 2-3 (13/11)", "orcado_h": 6.0, "atuado_h": 0.0, "status": "Planejado", "depende_acesso": False},
        {"id": 7, "etapa": "7. Controle Idempotência e Retry", "periodo": "Sem 2-3 (13/11)", "orcado_h": 4.0, "atuado_h": 0.0, "status": "Planejado", "depende_acesso": False},
        {"id": 8, "etapa": "8. ERP R12 - Login, Resp. e JNLP", "periodo": "Sem 3 (16/11)", "orcado_h": 8.0, "atuado_h": 0.0, "status": "Bloqueado (Sem Acesso)", "depende_acesso": True},
        {"id": 9, "etapa": "9. ERP R12 - Módulo AR (Transações)", "periodo": "Sem 3 (16-17/11)", "orcado_h": 12.0, "atuado_h": 0.0, "status": "Bloqueado (Sem Acesso)", "depende_acesso": True},
        {"id": 10, "etapa": "10. ERP R12 - Módulo AP (NFF)", "periodo": "Sem 3 (18-19/11)", "orcado_h": 12.0, "atuado_h": 0.0, "status": "Bloqueado (Sem Acesso)", "depende_acesso": True},
        {"id": 11, "etapa": "11. Planilha Controle e Relatório.xlsx", "periodo": "Sem 3 (14-19/11)", "orcado_h": 5.0, "atuado_h": 0.0, "status": "A Iniciar (Fim de Sem.)", "depende_acesso": False},
        {"id": 12, "etapa": "12. Pós-processamento ND (Mover + PDF)", "periodo": "Sem 3 (14-19/11)", "orcado_h": 4.0, "atuado_h": 0.0, "status": "A Iniciar", "depende_acesso": False},
        {"id": 13, "etapa": "13. Tratamento de Exceções (BE/SE)", "periodo": "Sem 3 (19/11)", "orcado_h": 6.0, "atuado_h": 0.0, "status": "A Iniciar", "depende_acesso": False},
        {"id": 14, "etapa": "14. Testes Integrados", "periodo": "Sem 3 (21/11)", "orcado_h": 6.0, "atuado_h": 0.0, "status": "A Iniciar (Sábado)", "depende_acesso": True},
        {"id": 15, "etapa": "15. Deploy e Agendamentos Orchestrator", "periodo": "Sem 4 (23/11)", "orcado_h": 2.0, "atuado_h": 0.0, "status": "A Iniciar", "depende_acesso": True},
        {"id": 16, "etapa": "16. Homologação Assistida (UAT)", "periodo": "Sem 4 (24/11)", "orcado_h": 4.0, "atuado_h": 0.0, "status": "Marco UAT 24/11", "depende_acesso": True},
        {"id": 17, "etapa": "17. Hipercare (Produção Assistida - Aumentado)", "periodo": "Sem 4 (24-27/11)", "orcado_h": 12.0, "atuado_h": 0.0, "status": "Planejado Reta Final", "depende_acesso": True},
    ],
    "clt_tasks": [
        {"id": 1, "etapa": "Fase 1: Discovery, Modeler 4 Etapas (BPMN) & Simulador", "janela_4m": "Sem 1 (02-06/11)", "meta_fast": "Concluído (10h)", "orcado_h": 16.0, "atuado_h": 10.0, "status": "Concluído ✅"},
        {"id": 2, "etapa": "Fase 2: Etapa 01 (Disp_CFM) + REFramework + Config + Testes CFM", "janela_4m": "Sem 2 (10-12/11)", "meta_fast": "10/11 a 12/11", "orcado_h": 14.0, "atuado_h": 0.0, "status": "Prioridade Imediata 🔥"},
        {"id": 3, "etapa": "Fase 3: Etapa 02 (Perf_ERP_Validacoes) - Consulta PJ Desktop", "janela_4m": "Sem 2-3 (13-17/11)", "meta_fast": "13/11 a 17/11", "orcado_h": 14.0, "atuado_h": 0.0, "status": "Acesso Win32 OK ✅"},
        {"id": 4, "etapa": "Fase 4: Etapa 03 (Perf_ERP_Cad_Vinculo) - Cadastro PF & Vínculos", "janela_4m": "Sem 3 (18-23/11)", "meta_fast": "18/11 a 23/11", "orcado_h": 14.0, "atuado_h": 0.0, "status": "Planejado"},
        {"id": 5, "etapa": "Fase 5: Etapa 04 (Perf_Portal SAUDI) + Planilha A-K", "janela_4m": "Sem 4 (24-25/11)", "meta_fast": "24/11 a 25/11", "orcado_h": 8.0, "atuado_h": 0.0, "status": "Planejado"},
        {"id": 6, "etapa": "Fase 6: Testes Integrados E2E (CT-01 a CT-12), UAT & Go-Live Final", "janela_4m": "Sem 4 (26-27/11)", "meta_fast": "26/11 a 27/11", "orcado_h": 10.0, "atuado_h": 0.0, "status": "🏁 Go-Live 27/11"},
    ],
    "pendencias": [
        {"projeto": "FN027 (Horista)", "item": "Retorno dos pontos levantados no PDD v1.1 junto à área de negócio", "status": "Em Andamento", "Impacto": "Regras finas de exceção"},
        {"projeto": "FN027 (Horista)", "item": "Liberação de acesso ao ambiente de Homologação e ERP R12 (AR/AP)", "status": "Em Andamento", "Impacto": "Gate 1 em 16/11"},
        {"projeto": "CLT (Corpo Clínico)", "item": "Liberação de credenciais e acesso ao sistema Desktop (Win32)", "status": "Resolvido ✅", "Impacto": "Seletores Etapas 02 e 03 Liberados"},
        {"projeto": "CLT (Corpo Clínico)", "item": "Liberação de acesso ao Portal Web de Divulgação (HML)", "status": "Em Andamento", "Impacto": "Seletores Etapa 04"},
    ],
    "diario": [
        {"data": "09/11/2026 17:20", "projeto": "Ambos", "nota": "🚨 REPLANEJAMENTO URGENTE: CLT readequado para entrega final em 27/11/2026. Rotina blindada: 06h-08h45 FN027, 09h-18h CLT, 19h-21h FN027. Foco total de pai: bebê nasce em 4 meses!"},
        {"data": "03/11/2026 18:04", "projeto": "FN027 (Horista)", "nota": "Revisões em relação ao PDD. Faltando pontos com João Buso e código do Fortra para avançarmos."},
        {"data": "02/11/2026 17:30", "projeto": "Ambos", "nota": "Baseline ajustada: FN027 em 120h totais (Hipercare 12h) com 6h PDD contabilizadas. CLT com esboço de desenvolvimento e testes apartados nas 4 Etapas do Modeler (10h/76h)."}
    ],
    "rotina_blocos": [
        {"horario": "06:00 - 06:25", "tipo": "Ativação & Hábitos", "projeto": "Pessoal", "descricao": "Levantar no 1º toque (regra dos 5s), 500ml água gelada, café preto, banho rápido. Zero telas.", "icone": "⏰"},
        {"horario": "06:30 - 08:45", "tipo": "BLOCO OURO 1 (2h15)", "projeto": "FN027 (Horista PJ)", "descricao": "Código puro no Studio: Arquitetura, Filas Orchestrator, Transversais e Leitura NDs.", "icone": "🟣"},
        {"horario": "08:45 - 09:00", "tipo": "Transição & Água", "projeto": "Pessoal", "descricao": "Alongamento, mais água, abrir ambiente corporativo e chat da equipe CLT.", "icone": "🔄"},
        {"horario": "09:00 - 12:30", "tipo": "COMERCIAL 1 (3h30)", "projeto": "CLT (Corpo Clínico)", "descricao": "Desenvolvimento pesado da etapa do dia no Studio (Etapas 01, 02 ou 03). Foco absoluto.", "icone": "🔵"},
        {"horario": "12:30 - 13:30", "tipo": "Almoço & Reset (1h)", "projeto": "Pessoal", "descricao": "Comida nutritiva, 10 min de caminhada, 20 min sem telas para reset cognitivo.", "icone": "🥗"},
        {"horario": "13:30 - 18:00", "tipo": "COMERCIAL 2 (4h30)", "projeto": "CLT (Corpo Clínico)", "descricao": "Testes unitários da etapa, refinamento de seletores Win32/Web e commit Git do dia.", "icone": "🔵"},
        {"horario": "18:00 - 19:00", "tipo": "Família & Jantar (1h)", "projeto": "Pessoal", "descricao": "Estar 100% presente com a esposa, falar sobre o bebê, refeição tranquila.", "icone": "❤️"},
        {"horario": "19:00 - 21:00", "tipo": "BLOCO OURO 2 (2h00)", "projeto": "FN027 (Horista PJ)", "descricao": "Testes de carga, apuração NDs, módulo EBS Oracle ou relatórios finais.", "icone": "🟣"},
        {"horario": "21:00 - 22:15", "tipo": "Desaceleração", "projeto": "Pessoal", "descricao": "Banho morno, checar checklist do dia seguinte, relaxamento mental.", "icone": "📖"},
        {"horario": "22:30", "tipo": "Sono Reparador (7h30)", "projeto": "Pessoal", "descricao": "Dormir impreterivelmente. Recuperação essencial para acordar às 06h.", "icone": "🌙"},
    ],
    "steps_diarios": [
        {"data": "10/11 (Ter)", "projeto": "FN027 (Manhã 06h30)", "step": "Item 2: Fechar Arquitetura REFramework, Config.xlsx e Filas Orchestrator", "status": "Pendente", "horas": "2.25h"},
        {"data": "10/11 (Ter)", "projeto": "CLT (Comercial 09h-18h)", "step": "Etapa 01 (Disp_CFM): REFramework base + Leitura planilha CFM + CT-03/04", "status": "Pendente", "horas": "7.0h"},
        {"data": "10/11 (Ter)", "projeto": "FN027 (Noite 19h-21h)", "step": "Item 3: Componentes Transversais (Logs estruturados, alertas e regex)", "status": "Pendente", "horas": "2.0h"},

        {"data": "11/11 (Qua)", "projeto": "FN027 (Manhã 06h30)", "step": "Item 3: Conclusão Transversais + Início Item 4 (Leitura NDs)", "status": "Pendente", "horas": "2.25h"},
        {"data": "11/11 (Qua)", "projeto": "CLT (Comercial 09h-18h)", "step": "Etapa 01 (Disp_CFM): Validação Web CFM + CT-05 e CT-08 (Etapa 01 Pronta!)", "status": "Pendente", "horas": "7.0h"},
        {"data": "11/11 (Qua)", "projeto": "FN027 (Noite 19h-21h)", "step": "Item 4: Geração NDs (Apuração de valores e filtros de exceção)", "status": "Pendente", "horas": "2.0h"},

        {"data": "12/11 (Qui)", "projeto": "FN027 (Manhã 06h30)", "step": "Item 5: Geração NDs (Montagem do Aviso de Débito em PDF/Word)", "status": "Pendente", "horas": "2.25h"},
        {"data": "12/11 (Qui)", "projeto": "CLT (Comercial 09h-18h)", "step": "Etapa 02 (Perf_ERP_Validacoes): Login Desktop Win32 Homepar + Consulta PJ + CT-06", "status": "Pendente", "horas": "7.0h"},
        {"data": "12/11 (Qui)", "projeto": "FN027 (Noite 19h-21h)", "step": "Item 5: Conclusão Aviso de Débito + Verificação de layouts", "status": "Pendente", "horas": "2.0h"},

        {"data": "13/11 (Sex)", "projeto": "FN027 (Manhã 06h30)", "step": "Item 6: Leitura NDs Aprovadas e motor DE-PARA", "status": "Pendente", "horas": "2.25h"},
        {"data": "13/11 (Sex)", "projeto": "CLT (Comercial 09h-18h)", "step": "Etapa 02 (Perf_ERP_Validacoes): Regras fiscais/tributárias + CT-07/09 (Etapa 02 Pronta!)", "status": "Pendente", "horas": "7.0h"},
        {"data": "13/11 (Sex)", "projeto": "FN027 (Noite 19h-21h)", "step": "Item 7: Controle de Idempotência, hash de unicidade e política de retry", "status": "Pendente", "horas": "2.0h"},

        {"data": "14/11 (Sáb)", "projeto": "FN027 (Fim de Semana)", "step": "Item 11 & 12: Planilha de Controle e Relatório Excel de Fechamento (07h-12h)", "status": "Pendente", "horas": "5.0h"},

        {"data": "16/11 (Seg)", "projeto": "FN027 (Manhã 06h30)", "step": "Item 8: Oracle EBS R12 (Login, navegação JNLP e módulo AR)", "status": "Pendente", "horas": "2.25h"},
        {"data": "16/11 (Seg)", "projeto": "CLT (Comercial 09h-18h)", "step": "Etapa 03 (Perf_ERP_Cad_Vinculo): Telas de Cadastro PF no Homepar Win32", "status": "Pendente", "horas": "7.0h"},
        {"data": "16/11 (Seg)", "projeto": "FN027 (Noite 19h-21h)", "step": "Item 8: Oracle EBS R12 AR (Digitação e validação de transações)", "status": "Pendente", "horas": "2.0h"},

        {"data": "17/11 (Ter)", "projeto": "FN027 (Manhã 06h30)", "step": "Item 9: Oracle EBS R12 AR (Lançamento de Contas a Receber e baixa)", "status": "Pendente", "horas": "2.25h"},
        {"data": "17/11 (Ter)", "projeto": "CLT (Comercial 09h-18h)", "step": "Etapa 03 (Perf_ERP_Cad_Vinculo): Vínculos de Especialidades e Unidades", "status": "Pendente", "horas": "7.0h"},
        {"data": "17/11 (Ter)", "projeto": "FN027 (Noite 19h-21h)", "step": "Item 9: Oracle EBS R12 AR (Tratamento de popups e confirmação)", "status": "Pendente", "horas": "2.0h"},

        {"data": "18/11 (Qua)", "projeto": "FN027 (Manhã 06h30)", "step": "Item 10: Oracle EBS R12 AP (Contas a Pagar / NFF)", "status": "Pendente", "horas": "2.25h"},
        {"data": "18/11 (Qua)", "projeto": "CLT (Comercial 09h-18h)", "step": "Etapa 03 (Perf_ERP_Cad_Vinculo): Modais, validações de erro + CT-01/02 (Etapa 03 Pronta!)", "status": "Pendente", "horas": "7.0h"},
        {"data": "18/11 (Qua)", "projeto": "FN027 (Noite 19h-21h)", "step": "Item 10: Oracle EBS R12 AP (Digitação de faturas e centros de custo)", "status": "Pendente", "horas": "2.0h"},

        {"data": "19/11 (Qui)", "projeto": "FN027 (Manhã 06h30)", "step": "Item 10: Conclusão Oracle AP + Início Item 13 (Exceções de Sistema/Negócio)", "status": "Pendente", "horas": "2.25h"},
        {"data": "19/11 (Qui)", "projeto": "CLT (Comercial 09h-18h)", "step": "Etapa 04 (Perf_Portal SAUDI): Automação Web Portal + Layout Planilha A-K", "status": "Pendente", "horas": "7.0h"},
        {"data": "19/11 (Qui)", "projeto": "FN027 (Noite 19h-21h)", "step": "Item 13: Tratamento de Exceções de Sistema e Negócio no REFramework", "status": "Pendente", "horas": "2.0h"},

        {"data": "20/11 (Sex)", "projeto": "Ambos (Feriado)", "step": "Feriado Consciência Negra: Folga merecida ou 3h de avanço flexível sem pressão", "status": "Pendente", "horas": "3.0h"},
        {"data": "21/11 (Sáb)", "projeto": "FN027 (Fim de Semana)", "step": "Item 14: Testes Integrados E2E com massa de homologação (07h-12h)", "status": "Pendente", "horas": "5.0h"},

        {"data": "23/11 (Seg)", "projeto": "FN027 (Manhã 06h30)", "step": "Item 15: Deploy no Orchestrator, assets e agendamentos de disparo", "status": "Pendente", "horas": "2.25h"},
        {"data": "23/11 (Seg)", "projeto": "CLT (Comercial 09h-18h)", "step": "Etapa 04 (Perf_Portal SAUDI): Validação de carga planilha + CT-10 a 12 (Etapa 04 Pronta!)", "status": "Pendente", "horas": "7.0h"},
        {"data": "23/11 (Seg)", "projeto": "FN027 (Noite 19h-21h)", "step": "Item 16: Preparação de massa para UAT assistida com o negócio", "status": "Pendente", "horas": "2.0h"},

        {"data": "24/11 (Ter)", "projeto": "FN027 (Manhã 06h30)", "step": "Item 16: Homologação Assistida (UAT) com time fiscal/financeiro", "status": "Pendente", "horas": "2.25h"},
        {"data": "24/11 (Ter)", "projeto": "CLT (Comercial 09h-18h)", "step": "Fase 6: Testes Integrados E2E (CT-01 a CT-12) encadeando as 4 Etapas em HML", "status": "Pendente", "horas": "7.0h"},
        {"data": "24/11 (Ter)", "projeto": "FN027 (Noite 19h-21h)", "step": "Item 17: Início Hipercare / Produção Assistida (Acompanhamento 1º ciclo)", "status": "Pendente", "horas": "2.0h"},

        {"data": "25/11 (Qua)", "projeto": "FN027 (Manhã 06h30)", "step": "Item 17: Hipercare (Monitoramento e validação de relatórios)", "status": "Pendente", "horas": "2.25h"},
        {"data": "25/11 (Qua)", "projeto": "CLT (Comercial 09h-18h)", "step": "Fase 6: Refinamento de timeouts, tratamento de telas lentas e evidências UAT", "status": "Pendente", "horas": "7.0h"},
        {"data": "25/11 (Qua)", "projeto": "FN027 (Noite 19h-21h)", "step": "Item 17: Hipercare (Auditoria dos lançamentos no Oracle EBS)", "status": "Pendente", "horas": "2.0h"},

        {"data": "26/11 (Qui)", "projeto": "FN027 (Manhã 06h30)", "step": "Item 17: Hipercare (Ajustes finos e validação final com João Buso)", "status": "Pendente", "horas": "2.25h"},
        {"data": "26/11 (Qui)", "projeto": "CLT (Comercial 09h-18h)", "step": "Fase 6: UAT Formal com a liderança do CLT + Aprovação e Documentação", "status": "Pendente", "horas": "7.0h"},
        {"data": "26/11 (Qui)", "projeto": "FN027 (Noite 19h-21h)", "step": "Item 17: Hipercare (Empacotamento final e encerramento)", "status": "Pendente", "horas": "2.0h"},

        {"data": "27/11 (Sex)", "projeto": "FN027 (Manhã 06h30)", "step": "🏁 FN027 FECHADO: Emissão do relatório de 120h (Faturamento R$ 6.000,00!)", "status": "Pendente", "horas": "2.25h"},
        {"data": "27/11 (Sex)", "projeto": "CLT (Comercial 09h-18h)", "step": "🏁 GO-LIVE CLT CORPO CLÍNICO: Deploy em Produção e Robô Entregue!", "status": "Pendente", "horas": "7.0h"},
        {"data": "27/11 (Sex)", "projeto": "Família (Noite)", "step": "❤️ COMEMORAÇÃO EM FAMÍLIA: Missão cumprida, bebê protegido e 100% no controle!", "status": "Pendente", "horas": "0.0h"},
    ],
}

COLOR_MAP = {
    "Concluído (Verde)": "bar-done",
    "Em Andamento (Azul)": "bar-now",
    "Aguardando / Dependente (Amarelo)": "bar-wait",
    "UAT & Hypercare (Roxo)": "bar-uat",
}


def load_data():
    if DATA_FILE.exists():
        try:
            saved = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            # Migração automática para a versão 6 (Meta Acelerada 27/11 e Rotina Diária)
            cur_ver = saved.get("schema_version", 0)
            if cur_ver < 6:
                saved["schema_version"] = 6
                saved["titulos"] = json.loads(json.dumps(DEFAULT_DATA["titulos"]))
                # Preserva horas já atuadas pelo usuário se houver
                atuado_map = {t["id"]: t.get("atuado_h", 0.0) for t in saved.get("clt_tasks", [])}
                new_clt_tasks = json.loads(json.dumps(DEFAULT_DATA["clt_tasks"]))
                for t in new_clt_tasks:
                    if t["id"] in atuado_map and atuado_map[t["id"]] > 0:
                        t["atuado_h"] = atuado_map[t["id"]]
                saved["clt_tasks"] = new_clt_tasks
                saved["clt_gantt"] = json.loads(json.dumps(DEFAULT_DATA["clt_gantt"]))
                saved["rotina_blocos"] = json.loads(json.dumps(DEFAULT_DATA["rotina_blocos"]))
                saved["steps_diarios"] = json.loads(json.dumps(DEFAULT_DATA["steps_diarios"]))
            else:
                if "titulos" not in saved:
                    saved["titulos"] = json.loads(json.dumps(DEFAULT_DATA["titulos"]))
                if "clt_gantt" not in saved:
                    saved["clt_gantt"] = json.loads(json.dumps(DEFAULT_DATA["clt_gantt"]))
                if "fn027_gantt" not in saved:
                    saved["fn027_gantt"] = json.loads(json.dumps(DEFAULT_DATA["fn027_gantt"]))
                if "rotina_blocos" not in saved:
                    saved["rotina_blocos"] = json.loads(json.dumps(DEFAULT_DATA["rotina_blocos"]))
                if "steps_diarios" not in saved:
                    saved["steps_diarios"] = json.loads(json.dumps(DEFAULT_DATA["steps_diarios"]))
            return saved
        except Exception:
            return json.loads(json.dumps(DEFAULT_DATA))
    return json.loads(json.dumps(DEFAULT_DATA))


def save_data(data):
    data["schema_version"] = 6
    data["last_updated"] = now_br_str()
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


data = load_data()
titulos = data["titulos"]

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-size: 12.5px !important;
    }
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

hoje_dt = datetime.now(TZ_BR)
hoje_str = hoje_dt.strftime("%d/%m/%Y")
hoje_dia = hoje_dt.day
hoje_mes = hoje_dt.month

st.title(titulos.get("painel_titulo", DEFAULT_DATA["titulos"]["painel_titulo"]))
st.caption(f"📅 Hoje: **{hoje_str}** • Início: **02 de Novembro de 2026** • Última alteração salva: `{data['last_updated']}`")

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

fn_val_atuado_str = f"R$ {fn_valor_atuado:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
fn_val_total_str = f"R$ {fn_valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

col1, col2, col3, col4 = st.columns(4)
col1.metric("🟣 FN027 (Horista)", f"{fn_atuado:g}h / {fn_orcado:g}h", f"Restam {fn_restante:g}h (Hipercare 12h)")
col2.metric("💰 FN027 Acumulado", fn_val_atuado_str, f"Total: {fn_val_total_str} ({taxa:.0f}/h)")
col3.metric("🔵 CLT (Corpo Clínico)", f"{clt_atuado:g}h / {clt_orcado:g}h", f"Restam {clt_restante:g}h (Meta 27/11)")
col4.metric("🚨 Entrega CLT (Acelerada)", "27 de Novembro", "Sprint Final: 10/11 a 27/11")

tab_rotina, tab_visao, tab_modeler, tab_horas, tab_pend = st.tabs([
    "🔥 Rotina Blindada & Steps (27/11)",
    "📊 Cronogramas (FN027 120h & CLT 27/11)",
    "🧩 Esboço Modeler 4 Etapas & Testes",
    "⏱️ Apontar / Editar / Zerar Horas",
    "🚧 Pendências PDD, Acessos & Diário",
])

with tab_rotina:
    st.error(
        "### 👶 O Motivo Inegociável: Meu Filho Nasce em 4 Meses (Março/2027)\n"
        "Esta sprint de **14 dias úteis (10 a 27 de Novembro)** não é sobre trabalhar desesperado. É sobre **método, disciplina e honra**.\n\n"
        "- **Projeto CLT (Corpo Clínico):** Entrega formal e Go-Live em **27 de Novembro de 2026** (fechando as 66h restantes no comercial).\n"
        "- **Projeto Horista (FN027):** 114h restantes executadas antes das 09h e após as 18h (+ fins de semana) para colocar **R$ 6.000,00 limpos** no bolso da família.\n"
        "- **A Regra:** Sem negociação com o despertador às 06h. Celular longe da cama. Um dia de cada vez, fatiado por etapas."
    )

    st.subheader("⏰ Grade Horária Diária Blindada (Segunda a Sexta)")
    df_rotina = pd.DataFrame(data.get("rotina_blocos", DEFAULT_DATA["rotina_blocos"]))
    st.dataframe(
        df_rotina[["horario", "icone", "tipo", "projeto", "descricao"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "horario": st.column_config.TextColumn("Horário", width="small"),
            "icone": st.column_config.TextColumn(" ", width="small"),
            "tipo": st.column_config.TextColumn("Bloco / Tipo", width="medium"),
            "projeto": st.column_config.TextColumn("Alvo / Projeto", width="small"),
            "descricao": st.column_config.TextColumn("O que fazer exatamente (Foco Absoluto)", width="large"),
        },
    )

    c_m1, c_m2, c_m3 = st.columns(3)
    c_m1.info("☀️ **Manhã Horista (06h30 - 08h45)**\n\n**2h15 líquidas** no FN027 antes do mundo acordar. Foco em código puro, sem interrupções.")
    c_m2.success("🏢 **Comercial CLT (09h00 - 18h00)**\n\n**7h30 a 8h** de desenvolvimento e testes no Corpo Clínico. Fatiado em Etapa 01, 02, 03 e 04.")
    c_m3.info("🌙 **Noite Horista (19h00 - 21h00)**\n\n**2h00 líquidas** no FN027 após a janta com a família. Total de **4h15/dia** no horista!")

    st.divider()
    st.subheader("🎯 Steps Diários de Batalha (10/11 a 27/11) — Marque o Progresso")
    st.caption("Acompanhe o que deve ser entregue em cada turno de cada dia. Atualize o status para manter o controle absoluto.")

    df_steps = pd.DataFrame(data.get("steps_diarios", DEFAULT_DATA["steps_diarios"]))
    ed_steps = st.data_editor(
        df_steps,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key="editor_steps_diarios",
        column_config={
            "data": st.column_config.TextColumn("Dia / Data", width="small"),
            "projeto": st.column_config.TextColumn("Turno / Projeto", width="medium"),
            "step": st.column_config.TextColumn("Entrega do Turno (Step)", width="large"),
            "horas": st.column_config.TextColumn("Horas", width="small"),
            "status": st.column_config.SelectboxColumn("Status", options=["Pendente", "Em Andamento", "Concluído ✅"], width="small"),
        },
    )

    if st.button("💾 Salvar Progresso dos Steps Diários", type="primary", use_container_width=True):
        data["steps_diarios"] = [r for r in ed_steps.to_dict(orient="records") if str(r.get("step", "")).strip()]
        save_data(data)
        st.success("Steps diários atualizados com sucesso!")
        st.rerun()

    st.divider()
    st.subheader("🛡️ Checklist de Hábitos Diários do Pai")
    c_h1, c_h2 = st.columns(2)
    with c_h1:
        st.checkbox("⏰ 06:00: Pulei da cama no primeiro toque (sem botão soneca)")
        st.checkbox("💧 06:05: Tomei 500ml de água gelada e banho para ativar")
        st.checkbox("🟣 06:30 - 08:45: Cumpri as 2h15 do FN027 antes do comercial")
        st.checkbox("🔵 09:00 - 18:00: Cumpri o comercial CLT focado na etapa do dia")
    with c_h2:
        st.checkbox("🥗 12:30 & 18:00: Almocei e jantei com atenção plena à família")
        st.checkbox("🟣 19:00 - 21:00: Cumpri as 2h00 da noite no FN027")
        st.checkbox("📱 22:00: Celular fora de alcance da cama")
        st.checkbox("🌙 22:30: Luzes apagadas para garantir 7h30 de sono")

with tab_visao:
    with st.expander("✏️ Editar Títulos e Nomes das Linhas dos Cronogramas Visuais"):
        st.caption("Altere qualquer título ou nome de atividade abaixo e clique em **💾 Salvar Títulos e Cronogramas Visuais**.")
        t_painel = st.text_input("Título Principal do Painel", value=titulos.get("painel_titulo", ""))
        c_t1, c_t2 = st.columns(2)
        t_clt_sec = c_t1.text_input("Título da Seção CLT", value=titulos.get("clt_secao", ""))
        t_clt_gantt = c_t2.text_input("Subtítulo do Cronograma Visual CLT", value=titulos.get("clt_gantt_titulo", ""))
        c_t3, c_t4 = st.columns(2)
        t_fn_sec = c_t3.text_input("Título da Seção FN027", value=titulos.get("fn_secao", ""))
        t_fn_gantt = c_t4.text_input("Subtítulo do Cronograma Visual FN027", value=titulos.get("fn_gantt_titulo", ""))

        st.markdown("**Linhas do Cronograma Visual CLT (Semanas S1 a S16):**")
        df_clt_g = pd.DataFrame(data.get("clt_gantt", DEFAULT_DATA["clt_gantt"]))
        ed_clt_g = st.data_editor(
            df_clt_g,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            key="ed_clt_gantt",
            column_config={
                "atividade": st.column_config.TextColumn("Nome da Atividade / Etapa (Editável)", width="large"),
                "periodos": st.column_config.TextColumn("Semanas Ativas (ex: S1, S2)", width="medium"),
                "cor": st.column_config.SelectboxColumn("Cor / Status", options=list(COLOR_MAP.keys()), width="medium"),
            },
        )

        st.markdown("**Linhas do Cronograma Visual FN027 (Dias 26..30 Out e 2..27 Nov):**")
        df_fn_g = pd.DataFrame(data.get("fn027_gantt", DEFAULT_DATA["fn027_gantt"]))
        ed_fn_g = st.data_editor(
            df_fn_g,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            key="ed_fn_gantt",
            column_config={
                "atividade": st.column_config.TextColumn("Nome da Atividade / Dia (Editável)", width="large"),
                "periodos": st.column_config.TextColumn("Dias Ativos (ex: 2, 3, 4)", width="medium"),
                "cor": st.column_config.SelectboxColumn("Cor / Status", options=list(COLOR_MAP.keys()), width="medium"),
            },
        )

        if st.button("💾 Salvar Títulos e Cronogramas Visuais", type="primary", use_container_width=True):
            data["titulos"] = {
                "painel_titulo": t_painel,
                "clt_secao": t_clt_sec,
                "clt_gantt_titulo": t_clt_gantt,
                "fn_secao": t_fn_sec,
                "fn_gantt_titulo": t_fn_gantt,
            }
            data["clt_gantt"] = [r for r in ed_clt_g.to_dict(orient="records") if str(r.get("atividade", "")).strip()]
            data["fn027_gantt"] = [r for r in ed_fn_g.to_dict(orient="records") if str(r.get("atividade", "")).strip()]
            save_data(data)
            st.success("Títulos e cronogramas visuais atualizados!")
            st.rerun()

    st.subheader(titulos.get("clt_secao", DEFAULT_DATA["titulos"]["clt_secao"]))
    st.info(
        "**Status Atual (Meta Acelerada 27/11):** Modeler fechado no UiPath (`BPMN` em 4 Etapas) com 10h concluídas. "
        "Acesso ao sistema Desktop (Win32) liberado ✅. "
        "**Meta Final:** Go-Live e entrega de todas as 4 etapas até **27 de Novembro de 2026** (66h restantes em 14 dias úteis de horário comercial)."
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

    st.markdown(f"#### {titulos.get('clt_gantt_titulo', DEFAULT_DATA['titulos']['clt_gantt_titulo'])}")
    # Cálculo automático da Semana Atual (S1..S16) e Mês Atual a partir de 02/11 no fuso de Brasília
    ref_clt_start = datetime(hoje_dt.year if hoje_dt.month >= 10 else hoje_dt.year - 1, 11, 2, tzinfo=TZ_BR)
    delta_days_clt = (hoje_dt - ref_clt_start).days
    curr_clt_idx = max(1, min(16, (delta_days_clt // 7) + 1)) if delta_days_clt >= 0 else 1
    curr_clt_week = f"S{curr_clt_idx}"
    curr_clt_month = ((curr_clt_idx - 1) // 4) + 1

    clt_weeks = [f"S{i}" for i in range(1, 17)]
    clt_months = [
        (1, "Mês 1: Novembro/26"),
        (2, "Mês 2: Dezembro/26"),
        (3, "Mês 3: Janeiro/27"),
        (4, "Mês 4: Fevereiro/27"),
    ]
    html_clt = '<table class="gantt-table"><thead><tr><th rowspan="2">Atividade / Etapa (CLT)</th>'
    for m_idx, m_label in clt_months:
        if m_idx == curr_clt_month:
            html_clt += f'<th colspan="4" style="background:#1e40af;">📍 {m_label}</th>'
        else:
            html_clt += f'<th colspan="4">{m_label}</th>'
    html_clt += "</tr><tr>"
    for w in clt_weeks:
        style_th = ' style="background:#2563eb; color:#ffffff; font-weight:700;"' if w == curr_clt_week else ""
        html_clt += f"<th{style_th}>{w}</th>"
    html_clt += "</tr></thead><tbody>"
    for row in data.get("clt_gantt", DEFAULT_DATA["clt_gantt"]):
        label = row.get("atividade", "")
        active_w = [x.strip() for x in str(row.get("periodos", "")).split(",") if x.strip()]
        cls = COLOR_MAP.get(row.get("cor", ""), "bar-now")
        html_clt += f'<tr><td class="act-name">{label}</td>'
        for w in clt_weeks:
            cell = f'<div class="{cls}"></div>' if w in active_w else ""
            html_clt += f"<td>{cell}</td>"
        html_clt += "</tr>"
    html_clt += "</tbody></table>"
    st.markdown(html_clt, unsafe_allow_html=True)

    st.markdown("##### 🗓️ Cronograma Visual Dia a Dia de Novembro — CLT Corpo Clínico (Sprint Final: 02/11 a 27/11)")
    clt_nov_cols = [
        ("2", 1), ("3", 1), ("4", 1), ("5", 1), ("6", 1),
        ("9", 2), ("10", 2), ("11", 2), ("12", 2), ("13", 2),
        ("16", 3), ("17", 3), ("18", 3), ("19", 3), ("20", 3),
        ("23", 4), ("24", 4), ("25", 4), ("26", 4), ("27", 4),
    ]
    clt_nov_weeks_meta = [
        (1, "Semana 1 (02-06/11 • Concluída)"),
        (2, "📍 Semana 2 (09-13/11 • Atual)"),
        (3, "Semana 3 (16-20/11)"),
        (4, "🏁 Semana 4 (23-27/11 • Go-Live)"),
    ]
    curr_nov_week = 2 if hoje_dia <= 15 else (3 if hoje_dia <= 22 else 4)

    html_clt_daily = '<table class="gantt-table"><thead><tr><th rowspan="2">Atividade / Dia (CLT Novembro)</th>'
    for w_idx, w_label in clt_nov_weeks_meta:
        style_w = ' style="background:#1e40af;"' if w_idx == curr_nov_week else ""
        html_clt_daily += f'<th colspan="5"{style_w}>{w_label}</th>'
    html_clt_daily += "</tr><tr>"
    for d_str, _ in clt_nov_cols:
        is_today = (int(d_str) == hoje_dia and hoje_mes == 11)
        if is_today:
            style_d = ' style="background:#2563eb; color:#ffffff; font-weight:700;" title="Hoje"'
        elif d_str in ("2", "20"):
            style_d = ' style="color:#f87171; font-weight:700;" title="Feriado"'
        elif d_str == "27":
            style_d = ' style="color:#10b981; font-weight:700; background:rgba(16,185,129,0.15);" title="Go-Live 27/11"'
        else:
            style_d = ""
        html_clt_daily += f"<th{style_d}>{d_str}</th>"
    html_clt_daily += "</tr></thead><tbody>"

    clt_daily_plan = [
        {"atividade": "1. Discovery, Modeler BPMN (4 Etapas) & Testes (10h)", "dias": ["2", "3", "4", "5", "6"], "cls": "bar-done"},
        {"atividade": "2. Etapa 01 (Disp_CFM): REFramework + Leitura CFM + CT-03/04", "dias": ["9", "10", "11", "12"], "cls": "bar-now"},
        {"atividade": "3. Etapa 02 (Perf_ERP_Validacoes): Consulta PJ Desktop Win32", "dias": ["12", "13", "16", "17"], "cls": "bar-now"},
        {"atividade": "4. Etapa 03 (Perf_ERP_Cad_Vinculo): Cadastro PF, Vínculos e Modais", "dias": ["17", "18", "19", "23"], "cls": "bar-now"},
        {"atividade": "5. Etapa 04 (Perf_Portal SAUDI): Divulgação Web + Planilha A-K", "dias": ["23", "24", "25"], "cls": "bar-wait"},
        {"atividade": "6. Testes Integrados E2E (CT-01 a CT-12) em HML", "dias": ["25", "26"], "cls": "bar-uat"},
        {"atividade": "7. UAT Assistida, Homologação Formal & GO-LIVE (27/11/2026)", "dias": ["27"], "cls": "bar-uat"},
    ]
    for row in clt_daily_plan:
        label = row["atividade"]
        active_days = row["dias"]
        cls = row["cls"]
        html_clt_daily += f'<tr><td class="act-name">{label}</td>'
        for d_str, _ in clt_nov_cols:
            cell = f'<div class="{cls}"></div>' if d_str in active_days else ""
            html_clt_daily += f"<td>{cell}</td>"
        html_clt_daily += "</tr>"
    html_clt_daily += "</tbody></table>"
    st.markdown(html_clt_daily, unsafe_allow_html=True)

    st.divider()
    st.subheader(titulos.get("fn_secao", DEFAULT_DATA["titulos"]["fn_secao"]))
    st.warning(
        "**Status Atual:** Contabilizadas **6h de PDD** até o momento (`R$ 300,00`). Aguardando pontos com João Buso e código do Fortra para avançarmos. "
        "Próximo passo imediato: **Arquitetura RPA, REFramework e Filas (8h)** seguido dos **Componentes Transversais (5h)**."
    )

    st.markdown(f"#### {titulos.get('fn_gantt_titulo', DEFAULT_DATA['titulos']['fn_gantt_titulo'])}")
    # Colunas do FN027 com (dia_str, mes_int, semana_idx) para destacar automaticamente o dia atual e evitar conflito entre 26-27/Out e 26-27/Nov
    fn_cols = [
        ("26", 10, 1), ("27", 10, 1), ("28", 10, 1), ("29", 10, 1), ("30", 10, 1),
        ("2", 11, 2),  ("3", 11, 2),  ("4", 11, 2),  ("5", 11, 2),  ("6", 11, 2),
        ("9", 11, 3),  ("10", 11, 3), ("11", 11, 3), ("12", 11, 3), ("13", 11, 3),
        ("16", 11, 4), ("17", 11, 4), ("18", 11, 4), ("19", 11, 4), ("20", 11, 4),
        ("23", 11, 5), ("24", 11, 5), ("25", 11, 5), ("26", 11, 5), ("27", 11, 5),
    ]
    # Determina automaticamente qual semana (1..5) está ativa conforme a data de hoje
    if hoje_mes == 10 and 26 <= hoje_dia <= 31:
        curr_fn_week = 1
    elif hoje_mes == 11:
        if hoje_dia <= 8:
            curr_fn_week = 2
        elif hoje_dia <= 15:
            curr_fn_week = 3
        elif hoje_dia <= 22:
            curr_fn_week = 4
        else:
            curr_fn_week = 5
    else:
        curr_fn_week = 2

    fn_weeks_meta = [
        (1, "Semana 1 (Outubro)"),
        (2, "Semana 2 (Novembro)"),
        (3, "Semana 3 (Novembro)"),
        (4, "Semana 4 (Novembro)"),
        (5, "Semana 5 (Novembro)"),
    ]
    html_fn = '<table class="gantt-table"><thead><tr><th rowspan="2">Atividade / Dia (FN027)</th>'
    for w_idx, w_title in fn_weeks_meta:
        if w_idx == curr_fn_week:
            html_fn += f'<th colspan="5" style="background:#1e40af;">📍 {w_title}</th>'
        else:
            html_fn += f'<th colspan="5">{w_title}</th>'
    html_fn += "</tr><tr>"
    for d_str, m_int, _ in fn_cols:
        is_today = (int(d_str) == hoje_dia and m_int == hoje_mes)
        if is_today:
            style_th = ' style="background:#2563eb; color:#ffffff; font-weight:700;" title="Hoje"'
        elif (d_str, m_int) in (("2", 11), ("20", 11)):
            style_th = ' style="color:#f87171; font-weight:700;" title="Feriado"'
        else:
            style_th = ""
        html_fn += f"<th{style_th}>{d_str}</th>"
    html_fn += "</tr></thead><tbody>"
    for row in data.get("fn027_gantt", DEFAULT_DATA["fn027_gantt"]):
        label = row.get("atividade", "")
        active_tokens = [x.strip() for x in str(row.get("periodos", "")).split(",") if x.strip()]
        # Desambigua 26 e 27 de Outubro vs. 26 e 27 de Novembro automaticamente
        has_oct_neighbors = any(t in ("28", "29", "30", "26/10", "27/10") for t in active_tokens)
        has_nov_end_neighbors = any(t in ("23", "24", "25", "26/11", "27/11") for t in active_tokens)
        cls = COLOR_MAP.get(row.get("cor", ""), "bar-now")
        html_fn += f'<tr><td class="act-name">{label}</td>'
        for d_str, m_int, _ in fn_cols:
            explicit_token = f"{d_str}/{m_int}"
            is_active = False
            if explicit_token in active_tokens:
                is_active = True
            elif d_str in active_tokens:
                if d_str in ("26", "27"):
                    if m_int == 10 and (has_oct_neighbors or not has_nov_end_neighbors):
                        is_active = True
                    elif m_int == 11 and (has_nov_end_neighbors or not has_oct_neighbors):
                        is_active = True
                elif d_str in ("28", "29", "30"):
                    is_active = (m_int == 10)
                else:
                    is_active = (m_int == 11)
            if is_active:
                cell = f'<div class="{cls}"></div>'
            elif d_str == "20" and m_int == 11 and "Hipercare" in label:
                cell = '<span style="opacity:0.6;">x</span>'
            else:
                cell = ""
            html_fn += f"<td>{cell}</td>"
        html_fn += "</tr>"
    html_fn += "</tbody></table>"
    st.markdown(html_fn, unsafe_allow_html=True)

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
    st.subheader("⏱️ Editar Nomes das Etapas, Corrigir ou Zerar Horas Lançadas")
    st.caption(
        "Você pode **editar o nome de qualquer Macroatividade / Fase**, **digitar qualquer valor** em **Já Atuado (h)** / **Orçado (h)**, "
        "ou marcar **🔄 Zerar Horas?** e clicar em **💾 Salvar Alterações de Horas**."
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
            "etapa": st.column_config.TextColumn("Macroatividade (Editável)"),
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
            "etapa": st.column_config.TextColumn("Fase / Etapa (Editável)"),
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
        st.success("Horas e nomes salvos com sucesso!")
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
