
import streamlit as st
from datetime import date
from html import escape

from database import init_db
from tasks import (
    create_task,
    get_tasks,
    get_task,
    update_task,
    delete_task,
    get_dashboard_stats,
    STATUSES,
    PRIORITIES
)

# =====================================================
# CONFIGURAÇÃO
# =====================================================

st.set_page_config(
    page_title="TaskFlow",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()

# =====================================================
# IDENTIDADE VISUAL
# =====================================================

st.markdown("""
<style>

/* PALETA */

:root {
    --background: #E3EBE3;
    --surface: #F4F7F2;
    --surface-hover: #EAF1E9;
    --sidebar: #173C2B;
    --primary: #25834B;
    --primary-dark: #176B39;
    --text: #20372A;
    --muted: #586B5D;
    --border: #CCD9CE;
}

/* FUNDO GERAL */

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background: #E3EBE3 !important;
    color: #20372A !important;
}

[data-testid="stHeader"] {
    background: #E3EBE3 !important;
}

.block-container {
    max-width: 1500px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* TEXTOS GERAIS */

html, body, [class*="css"] {
    color: #20372A;
}

h1, h2, h3, h4, h5, h6 {
    color: #20372A !important;
    font-weight: 750 !important;
}

p, li, label, span {
    color: inherit;
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: #20372A !important;
}

[data-testid="stCaptionContainer"] p {
    color: #586B5D !important;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: #173C2B !important;
    border-right: none !important;
}

[data-testid="stSidebar"] * {
    color: #F4F7F2 !important;
}

/* CORRIGIR TEXTO DOS CAMPOS */

[data-testid="stSidebar"] [data-baseweb="select"] *,
[data-testid="stSidebar"] [data-testid="stDateInput"] *,
[data-testid="stSidebar"] [data-testid="stSelectbox"] * {
    color: #20372A !important;
    -webkit-text-fill-color: #20372A !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-testid="stDateInput"] input {
    background: #FFFFFF !important;
}


[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #D0E0D3 !important;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #C0D2C3 !important;
}

[data-testid="stSidebar"] hr {
    border-color: #41634D !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: transparent;
    border-radius: 9px;
    padding: 9px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #28523A;
}

/* CABEÇALHO */

.eyebrow {
    color: #25834B !important;
    font-size: 11px;
    font-weight: 850;
    letter-spacing: 1.8px;
    margin-bottom: 9px;
}

.page-title {
    color: #183326 !important;
    font-size: 34px;
    font-weight: 850;
    letter-spacing: -1.2px;
    line-height: 1.2;
}

.page-subtitle {
    color: #586B5D !important;
    font-size: 14px;
    margin-top: 9px;
    margin-bottom: 28px;
}

/* CARDS E MÉTRICAS */

[data-testid="stMetric"],
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stExpander"] {
    background: #F4F7F2 !important;
    border: 1px solid #CCD9CE !important;
    border-radius: 15px !important;
    box-shadow: 0 4px 14px rgba(30, 60, 40, 0.045);
}

[data-testid="stMetric"] {
    padding: 20px 22px;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: #586B5D !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {
    color: #183326 !important;
    font-size: 29px !important;
    font-weight: 800 !important;
}

[data-testid="stMetricDelta"] {
    color: #25834B !important;
}

/* FORMULÁRIOS E CAMPOS */

.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stDateInput label,
.stRadio label {
    color: #20372A !important;
    font-weight: 650 !important;
}

.stTextInput input,
.stTextArea textarea,
[data-baseweb="select"] > div,
[data-testid="stDateInput"] input {
    background: #FFFFFF !important;
    color: #20372A !important;
    border: 1px solid #C5D5C8 !important;
    border-radius: 9px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #78877B !important;
    opacity: 1 !important;
}

[data-baseweb="select"] * {
    color: #20372A !important;
}

[data-baseweb="popover"],
[data-baseweb="menu"] {
    background: #FFFFFF !important;
}

[data-baseweb="menu"] * {
    color: #20372A !important;
}


/* CORREÇÃO: CAMPOS DA SIDEBAR */

[data-testid="stSidebar"] [data-baseweb="select"] {
    background-color: #FFFFFF !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border-color: #C5D5C8 !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] input,
[data-testid="stSidebar"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-baseweb="select"] div,
[data-testid="stSidebar"] [data-baseweb="select"] svg {
    color: #20372A !important;
    fill: #20372A !important;
}

[data-testid="stSidebar"] [data-testid="stDateInput"] input {
    background-color: #FFFFFF !important;
    color: #20372A !important;
    -webkit-text-fill-color: #20372A !important;
    border: 1px solid #C5D5C8 !important;
}

/* OPÇÕES ABERTAS DOS MENUS */

[data-baseweb="popover"],
[data-baseweb="popover"] *,
[data-baseweb="menu"],
[data-baseweb="menu"] * {
    background-color: #FFFFFF !important;
    color: #20372A !important;
    -webkit-text-fill-color: #20372A !important;
}

/* OPÇÃO SELECIONADA */

[data-baseweb="select"] [aria-selected="true"] {
    background-color: #DCEBDD !important;
    color: #20372A !important;
}


/* BOTÕES */

.stButton > button {
    background: #F4F7F2 !important;
    color: #20372A !important;
    border: 1px solid #C5D5C8 !important;
    border-radius: 9px !important;
    font-weight: 650 !important;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: #DCEBDD !important;
    border-color: #25834B !important;
    color: #176B39 !important;
}

.stFormSubmitButton > button {
    background: #25834B !important;
    color: #FFFFFF !important;
    border: 1px solid #25834B !important;
    border-radius: 9px !important;
    font-weight: 750 !important;
}

.stFormSubmitButton > button:hover {
    background: #176B39 !important;
    color: #FFFFFF !important;
}

/* KANBAN */

.kanban-heading {
    background: #D4E1D5;
    color: #20372A !important;
    border: 1px solid #C5D5C8;
    border-radius: 11px;
    padding: 14px;
    margin-bottom: 15px;
    font-size: 15px;
    font-weight: 800;
}

.kanban-count {
    color: #25834B !important;
    font-weight: 850;
    float: right;
}

/* TAREFAS */

.task-title {
    color: #183326 !important;
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 8px;
}

.task-description {
    color: #586B5D !important;
    font-size: 13px;
    line-height: 1.6;
    margin-bottom: 13px;
}

.task-meta {
    color: #586B5D !important;
    font-size: 12px;
    margin-top: 12px;
}

/* PRIORIDADES */

.priority-high {
    display: inline-block;
    background: #FCE8E8;
    color: #A92F36 !important;
    padding: 5px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 800;
}

.priority-medium {
    display: inline-block;
    background: #FFF0D5;
    color: #885609 !important;
    padding: 5px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 800;
}

.priority-low {
    display: inline-block;
    background: #DCEFE0;
    color: #176B39 !important;
    padding: 5px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 800;
}

/* GRÁFICO PERSONALIZADO */

.chart-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 19px 0;
}

.chart-label {
    width: 115px;
    flex-shrink: 0;
    color: #304638 !important;
    font-size: 13px;
    font-weight: 650;
}

.chart-track {
    flex: 1;
    height: 12px;
    background: #DDE7DE;
    border-radius: 20px;
    overflow: hidden;
}

.chart-fill {
    height: 100%;
    background: #25834B;
    border-radius: 20px;
}

.chart-value {
    width: 25px;
    text-align: right;
    color: #20372A !important;
    font-size: 13px;
    font-weight: 800;
}

/* PROGRESSO */

.progress-number {
    color: #25834B !important;
    font-size: 40px;
    font-weight: 850;
    margin: 15px 0 3px 0;
}

.progress-description {
    color: #586B5D !important;
    font-size: 13px;
    margin-bottom: 15px;
}

.stProgress > div {
    background: #DDE7DE !important;
}

.stProgress > div > div > div {
    background: #25834B !important;
}

/* DIVISÓRIAS E ALERTAS */

hr {
    border-color: #CCD9CE !important;
}

[data-testid="stAlert"] {
    background: #F4F7F2 !important;
    color: #20372A !important;
    border-radius: 10px;
}

/* RODAPÉ */

.footer {
    color: #586B5D !important;
    font-size: 11px;
    text-align: center;
    padding: 25px 0;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# FUNÇÕES AUXILIARES
# =====================================================

def refresh():
    st.rerun()


def priority_class(priority):
    classes = {
        "Alta": "priority-high",
        "Média": "priority-medium",
        "Baixa": "priority-low"
    }
    return classes.get(priority, "priority-low")


def render_header(title, subtitle, section="TASKFLOW"):

    st.markdown(
        f"""
        <div class="eyebrow">{escape(section)}</div>
        <div class="page-title">{escape(title)}</div>
        <div class="page-subtitle">{escape(subtitle)}</div>
        """,
        unsafe_allow_html=True
    )


def render_task_card(task, kanban=False):

    with st.container(border=True):

        title = escape(str(task["title"]))
        description = escape(str(task["description"] or ""))

        st.markdown(
            f'<div class="task-title">{title}</div>',
            unsafe_allow_html=True
        )

        if description:
            st.markdown(
                f'<div class="task-description">{description}</div>',
                unsafe_allow_html=True
            )

        st.markdown(
            f'<span class="{priority_class(task["priority"])}">'
            f'{escape(str(task["priority"]))} prioridade'
            '</span>',
            unsafe_allow_html=True
        )

        if task["due_date"]:
            st.markdown(
                f'<div class="task-meta">📅 '
                f'{escape(str(task["due_date"]))}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="task-meta">Sem vencimento definido</div>',
                unsafe_allow_html=True
            )

        if kanban:

            current_index = STATUSES.index(task["status"])

            if current_index < len(STATUSES) - 1:

                if st.button(
                    "Avançar →",
                    key=f"advance_{task['id']}",
                    use_container_width=True
                ):

                    update_task(
                        task["id"],
                        task["title"],
                        task["description"] or "",
                        task["priority"],
                        task["due_date"],
                        STATUSES[current_index + 1]
                    )

                    refresh()

            if current_index > 0:

                if st.button(
                    "← Voltar",
                    key=f"back_{task['id']}",
                    use_container_width=True
                ):

                    update_task(
                        task["id"],
                        task["title"],
                        task["description"] or "",
                        task["priority"],
                        task["due_date"],
                        STATUSES[current_index - 1]
                    )

                    refresh()

        if st.button(
            "Excluir tarefa",
            key=f"delete_{task['id']}",
            use_container_width=True
        ):

            delete_task(task["id"])
            refresh()


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("""
    <div style="padding: 5px 5px 18px 5px;">
        <div style="font-size: 28px; font-weight: 850;
                    letter-spacing: -1px; color: #FFFFFF;">
            🌿 TaskFlow
        </div>
        <div style="font-size: 12px; color: #D0E0D3;
                    margin-top: 5px;">
            Organize. Execute. Conquer.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("**MENU PRINCIPAL**")

    page = st.radio(
        "Navegação",
        [
            "Dashboard",
            "Quadro Kanban",
            "Todas as tarefas"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("**+ NOVA TAREFA**")

    with st.form("new_task_form", clear_on_submit=True):

        new_title = st.text_input(
            "Título",
            placeholder="Ex: Estudar Python"
        )

        new_description = st.text_area(
            "Descrição",
            placeholder="Descreva sua tarefa...",
            height=90
        )

        new_priority = st.selectbox(
            "Prioridade",
            PRIORITIES
        )

        new_status = st.selectbox(
            "Status",
            STATUSES
        )

        new_due_date = st.date_input(
            "Vencimento",
            value=None,
            format="DD/MM/YYYY"
        )

        submitted = st.form_submit_button(
            "Criar tarefa +",
            use_container_width=True
        )

        if submitted:

            try:

                create_task(
                    title=new_title,
                    description=new_description,
                    priority=new_priority,
                    due_date=(
                        new_due_date.isoformat()
                        if new_due_date else None
                    ),
                    status=new_status
                )

                st.success("Tarefa criada!")
                st.rerun()

            except ValueError as error:
                st.error(str(error))

    st.divider()

    st.markdown("""
    <div style="font-size: 11px; color: #D0E0D3;">
        TASKFLOW<br>
        <b>Personal Productivity System</b>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# CARREGAMENTO DOS DADOS
# =====================================================

stats = get_dashboard_stats()
tasks = get_tasks()


# =====================================================
# DASHBOARD
# =====================================================

if page == "Dashboard":

    render_header(
        "Visão geral",
        "Acompanhe suas atividades e veja seu progresso.",
        "SEU ESPAÇO DE TRABALHO"
    )

    # INDICADORES

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total de tarefas", stats["total"])

    with col2:
        st.metric("Pendentes", stats["pending"])

    with col3:
        st.metric("Em andamento", stats["in_progress"])

    with col4:
        st.metric("Concluídas", stats["completed"])

    st.write("")

    # GRÁFICO E PROGRESSO

    left, right = st.columns([1.5, 1])

    with left:

        with st.container(border=True):

            st.markdown("### Atividades por status")

            st.caption("Distribuição das suas tarefas.")

            total = stats["total"]

            chart_items = [
                ("Pendentes", stats["pending"]),
                ("Em andamento", stats["in_progress"]),
                ("Concluídas", stats["completed"])
            ]

            for label, value in chart_items:

                percentage = (
                    (value / total) * 100
                    if total > 0 else 0
                )

                st.markdown(
                    f"""
                    <div class="chart-row">
                        <div class="chart-label">{label}</div>
                        <div class="chart-track">
                            <div class="chart-fill"
                                 style="width: {percentage}%;">
                            </div>
                        </div>
                        <div class="chart-value">{value}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    with right:

        with st.container(border=True):

            st.markdown("### Seu progresso")

            st.caption("Percentual de tarefas concluídas.")

            total = stats["total"]
            completed = stats["completed"]

            progress = completed / total if total else 0

            st.markdown(
                f"""
                <div class="progress-number">
                    {progress * 100:.0f}%
                </div>
                <div class="progress-description">
                    {completed} de {total} tarefas finalizadas
                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(progress)

            st.divider()

            st.markdown("**Tarefas atrasadas**")

            st.markdown(
                f"""
                <div style="font-size: 29px; font-weight: 850;
                            color: #B83D42;">
                    {stats["overdue"]}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")

    # TAREFAS RECENTES

    st.markdown("### Tarefas recentes")

    st.caption("Suas últimas atividades adicionadas.")

    recent_tasks = sorted(
        tasks,
        key=lambda task: task["id"],
        reverse=True
    )[:5]

    if recent_tasks:

        for task in recent_tasks:
            render_task_card(task)

    else:

        st.info(
            "Você ainda não possui tarefas. "
            "Use o menu lateral para criar sua primeira tarefa."
        )


# =====================================================
# QUADRO KANBAN
# =====================================================

elif page == "Quadro Kanban":

    render_header(
        "Quadro Kanban",
        "Visualize e organize suas tarefas por etapa.",
        "GERENCIAMENTO DE PROJETOS"
    )

    columns = st.columns(3)

    for index, status in enumerate(STATUSES):

        with columns[index]:

            status_tasks = [
                task for task in tasks
                if task["status"] == status
            ]

            st.markdown(
                f"""
                <div class="kanban-heading">
                    {escape(status)}
                    <span class="kanban-count">
                        {len(status_tasks)}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

            if status_tasks:

                for task in status_tasks:
                    render_task_card(task, kanban=True)

            else:

                with st.container(border=True):
                    st.caption("Nenhuma tarefa nesta etapa.")


# =====================================================
# TODAS AS TAREFAS
# =====================================================

elif page == "Todas as tarefas":

    render_header(
        "Todas as tarefas",
        "Pesquise, filtre e gerencie suas atividades.",
        "GERENCIAMENTO"
    )

    with st.container(border=True):

        st.markdown("### Filtros")

        col1, col2, col3 = st.columns(3)

        with col1:
            filter_status = st.selectbox(
                "Status",
                ["Todos"] + STATUSES
            )

        with col2:
            filter_priority = st.selectbox(
                "Prioridade",
                ["Todas"] + PRIORITIES
            )

        with col3:
            search = st.text_input(
                "Pesquisar tarefa",
                placeholder="Digite um título ou descrição..."
            )

    filtered_tasks = get_tasks(
        status=filter_status,
        priority=filter_priority,
        search=search
    )

    st.write("")

    st.markdown(
        f"**{len(filtered_tasks)} tarefa(s) encontrada(s)**"
    )

    if filtered_tasks:

        for task in filtered_tasks:
            render_task_card(task)

    else:

        st.info("Nenhuma tarefa encontrada com esses filtros.")

    st.divider()

    st.markdown("### Editar tarefa")

    st.caption(
        "Selecione uma tarefa para modificar suas informações."
    )

    if tasks:

        task_options = {
            f"#{task['id']} — {task['title']}": task["id"]
            for task in tasks
        }

        selected_label = st.selectbox(
            "Tarefa",
            list(task_options.keys())
        )

        selected_id = task_options[selected_label]
        selected_task = get_task(selected_id)

        if selected_task:

            with st.container(border=True):

                with st.form("edit_task_form"):

                    edit_title = st.text_input(
                        "Título",
                        value=selected_task["title"]
                    )

                    edit_description = st.text_area(
                        "Descrição",
                        value=selected_task["description"] or ""
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        edit_priority = st.selectbox(
                            "Prioridade",
                            PRIORITIES,
                            index=PRIORITIES.index(
                                selected_task["priority"]
                            )
                        )

                    with col2:

                        edit_status = st.selectbox(
                            "Status",
                            STATUSES,
                            index=STATUSES.index(
                                selected_task["status"]
                            )
                        )

                    with col3:

                        saved_date = (
                            date.fromisoformat(
                                selected_task["due_date"]
                            )
                            if selected_task["due_date"]
                            else None
                        )

                        edit_due_date = st.date_input(
                            "Vencimento",
                            value=saved_date,
                            format="DD/MM/YYYY"
                        )

                    save = st.form_submit_button(
                        "Salvar alterações",
                        use_container_width=True
                    )

                    if save:

                        try:

                            update_task(
                                selected_id,
                                edit_title,
                                edit_description,
                                edit_priority,
                                (
                                    edit_due_date.isoformat()
                                    if edit_due_date else None
                                ),
                                edit_status
                            )

                            st.success("Tarefa atualizada!")
                            st.rerun()

                        except ValueError as error:
                            st.error(str(error))

    else:

        st.info("Cadastre uma tarefa para começar.")


# =====================================================
# RODAPÉ
# =====================================================

st.markdown(
    """
    <div class="footer">
        TaskFlow · Personal Productivity System
    </div>
    """,
    unsafe_allow_html=True
)
