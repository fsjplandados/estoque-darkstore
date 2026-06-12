import streamlit as st
import pandas as pd
import plotly.express as px
import os

CACHE_FILE = "stokeflow_cache.pkl"

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="StokeFlow - Darkstore São João",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CSS PERSONALIZADO E COMPONENTES HTML
# ==========================================
def inject_custom_css():
    st.markdown("""
        <style>
            .stApp { background-color: #f8fafc; }
            #MainMenu {display: none;}
            header {display: none;}
            .block-container { padding-top: 0rem; padding-bottom: 1rem; max-width: 95%; }

            /* Header Customizado Estilo Tailwind */
            .custom-header {
                background-color: white; border-bottom: 1px solid #e2e8f0; padding: 1.5rem 5%;
                display: flex; justify-content: space-between; align-items: center;
                margin-left: -5.5%; margin-right: -5.5%; margin-top: 0rem; margin-bottom: 2rem;
            }
            .header-left { display: flex; align-items: center; gap: 1rem; }
            .header-logo-box { background-color: #4f46e5; padding: 0.5rem; border-radius: 0.5rem; color: white; display: flex; align-items: center;}
            .header-title { font-size: 1.25rem; font-weight: 800; color: #0f172a; margin: 0; display: flex; align-items: center; gap: 0.5rem;}
            .header-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
            .badge-darkstore { background-color: #e0e7ff; color: #4338ca; font-size: 0.65rem; font-weight: 800; padding: 0.15rem 0.5rem; border-radius: 9999px; }
            
            .header-right { display: flex; align-items: center; gap: 1rem; }
            .sync-badge { display: flex; align-items: center; gap: 0.35rem; background-color: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; font-size: 0.75rem; font-weight: 700; padding: 0.25rem 0.75rem; border-radius: 0.375rem; }
            .sync-dot { width: 6px; height: 6px; background-color: #22c55e; border-radius: 50%; }

            /* Abas */
            .tabs-container { display: flex; gap: 1.5rem; border-bottom: 1px solid #e2e8f0; margin-bottom: 2rem; }
            .tab-active { font-weight: 700; color: #0f172a; border-bottom: 2px solid #0f172a; padding-bottom: 0.5rem; cursor: pointer; }
            .tab-inactive { font-weight: 600; color: #64748b; padding-bottom: 0.5rem; cursor: pointer; }

            /* Cartões KPI Customizados */
            .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
            .kpi-card { background: white; border: 1px solid #f1f5f9; border-radius: 1rem; padding: 1.25rem; display: flex; justify-content: space-between; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
            .kpi-left { display: flex; flex-direction: column; gap: 0.25rem; }
            .kpi-title { font-size: 0.7rem; font-weight: 800; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; }
            .kpi-value { font-size: 1.875rem; font-weight: 800; color: #0f172a; line-height: 1; }
            .kpi-value-red { color: #e11d48; }
            .kpi-value-green { color: #10b981; }
            .kpi-desc { font-size: 0.75rem; color: #64748b; }
            .kpi-desc-blue { color: #4f46e5; font-weight: 700; }
            
            .kpi-icon-box { width: 3rem; height: 3rem; border-radius: 0.75rem; display: flex; align-items: center; justify-content: center; flex-shrink: 0;}
            .bg-slate { background-color: #f8fafc; color: #475569; }
            .bg-red { background-color: #fff1f2; color: #e11d48; }
            .bg-indigo { background-color: #eef2ff; color: #4f46e5; }
            .bg-emerald { background-color: #ecfdf5; color: #10b981; }
            
            /* Gráficos customizados e fundos brancos */
            .chart-title { font-weight: 700; color: #0f172a; display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;}
            
            [data-testid="stExpander"] details {
                background-color: white;
                border-radius: 0.5rem;
                border: 1px solid #e2e8f0;
            }
            
            [data-testid="stVerticalBlockBorderWrapper"] {
                background-color: white;
                border-radius: 0.5rem;
                border: 1px solid #e2e8f0 !important;
            }
        </style>
    """, unsafe_allow_html=True)

def render_header():
    st.markdown("""
        <div class="custom-header">
            <div class="header-left">
                <div class="header-logo-box">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
                </div>
                <div>
                    <h1 class="header-title">StokeFlow <span class="badge-darkstore">DARKSTORE</span></h1>
                    <p class="header-subtitle">Gestão Exclusiva: São João</p>
                </div>
            </div>
            <div class="header-right">
                <div class="sync-badge"><div class="sync-dot"></div> Sincronizado</div>
            </div>
        </div>
        <div class="tabs-container">
            <div class="tab-active"><svg width="16" height="16" style="display:inline; margin-bottom:-2px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg> Painel & Inventário</div>
            <div class="tab-inactive"><svg width="16" height="16" style="display:inline; margin-bottom:-2px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="4" y1="21" x2="4" y2="14"></line><line x1="4" y1="10" x2="4" y2="3"></line><line x1="12" y1="21" x2="12" y2="12"></line><line x1="12" y1="8" x2="12" y2="3"></line><line x1="20" y1="21" x2="20" y2="16"></line><line x1="20" y1="12" x2="20" y2="3"></line><line x1="1" y1="14" x2="7" y2="14"></line><line x1="9" y1="8" x2="15" y2="8"></line><line x1="17" y1="16" x2="23" y2="16"></line></svg> Simulador de Demanda</div>
        </div>
    """, unsafe_allow_html=True)

def render_kpis(skus, cds_mapped, rupturas, pct_ruptura, avg_cobertura, saldo_cd):
    # Formatação Pt-BR
    saldo_cd_str = f"{saldo_cd:,.0f}".replace(",", ".")
    
    html = f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-left">
                <span class="kpi-title">SKUS MAPEADOS</span>
                <span class="kpi-value">{skus}</span>
                <span class="kpi-desc kpi-desc-blue">{cds_mapped} CDs mapeados para abastecimento</span>
            </div>
            <div class="kpi-icon-box bg-slate">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path><line x1="7" y1="7" x2="7.01" y2="7"></line></svg>
            </div>
        </div>
        <div class="kpi-card">
            <div class="kpi-left">
                <span class="kpi-title">ITENS EM RUPTURA IMINENTE</span>
                <span class="kpi-value kpi-value-red">{rupturas} <span style="font-size:0.9rem">({pct_ruptura:.0f}%)</span></span>
                <span class="kpi-desc">Estoque c/ Trânsito zerado</span>
            </div>
            <div class="kpi-icon-box bg-red">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
            </div>
        </div>
        <div class="kpi-card">
            <div class="kpi-left">
                <span class="kpi-title">COBERTURA MÉDIA</span>
                <span class="kpi-value kpi-value-green">{avg_cobertura:.0f} dias</span>
                <span class="kpi-desc">Tempo de segurança da Darkstore</span>
            </div>
            <div class="kpi-icon-box bg-indigo">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
            </div>
        </div>
        <div class="kpi-card">
            <div class="kpi-left">
                <span class="kpi-title">SALDO TOTAL NOS CDS</span>
                <span class="kpi-value kpi-value-green">{saldo_cd_str} un</span>
                <span class="kpi-desc">Mapeado por Cód. de Produto</span>
            </div>
            <div class="kpi-icon-box bg-emerald">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# ==========================================
# FUNÇÕES DE ETL E MEMÓRIA
# ==========================================
def clean_column_names(df):
    df.columns = [str(c).encode('ascii', 'ignore').decode('utf-8').lower().replace(' ', '').replace('.', '').replace('_', '') for c in df.columns]
    return df

def clean_cod(val):
    if pd.isna(val): return None
    val_str = str(val).split('.')[0].strip()
    return val_str if val_str else None

@st.cache_data(show_spinner=False)
def process_data(file_curvas, file_darkstore, file_cds):
    df_curvas = pd.read_excel(file_curvas)
    df_curvas = clean_column_names(df_curvas)
    
    col_cod_curva = next((c for c in df_curvas.columns if 'codproduto' in c), None)
    col_curva = next((c for c in df_curvas.columns if c == 'curvavalor'), None)
    
    valid_skus = {}
    if col_cod_curva and col_curva:
        for _, row in df_curvas.iterrows():
            curva = str(row[col_curva]).upper().strip()
            if curva in ['CURVA A', 'CURVA B']:
                cod = clean_cod(row[col_cod_curva])
                if cod: valid_skus[cod] = curva

    df_cds = pd.read_excel(file_cds)
    df_cds = clean_column_names(df_cds)
    
    col_cod_cd = next((c for c in df_cds.columns if 'codproduto' in c), None)
    col_filial = next((c for c in df_cds.columns if 'descfilial' in c), None)
    col_qtde_cd = next((c for c in df_cds.columns if c == 'estoqueqtde'), None)
    
    cd_map = {}
    if col_cod_cd and col_qtde_cd:
        for _, row in df_cds.iterrows():
            cod = clean_cod(row[col_cod_cd])
            if cod in valid_skus:
                filial = str(row[col_filial]) if col_filial else "CD Padrao"
                qtde = int(row[col_qtde_cd]) if pd.notna(row[col_qtde_cd]) else 0
                if cod not in cd_map:
                    cd_map[cod] = []
                cd_map[cod].append({"filial": filial, "qtde": qtde})

    df_dark = pd.read_excel(file_darkstore)
    df_dark = clean_column_names(df_dark)
    
    col_cod = next((c for c in df_dark.columns if 'codproduto' in c), None)
    col_name = next((c for c in df_dark.columns if 'descproduto' in c or 'descri' in c), None)
    col_custo = next((c for c in df_dark.columns if c == 'estoqueacusto'), None)
    col_qtde = next((c for c in df_dark.columns if c == 'estoqueqtde'), None)
    col_giro = next((c for c in df_dark.columns if 'giro030dias' in c or 'giro' in c), None)
    col_transit = next((c for c in df_dark.columns if 'transito' in c), None)

    products = []
    for _, row in df_dark.iterrows():
        cod = clean_cod(row[col_cod])
        if cod in valid_skus:
            giro_30d = float(row[col_giro]) if col_giro and pd.notna(row[col_giro]) else 0.0
            estoque_transito = int(row[col_transit]) if col_transit and pd.notna(row[col_transit]) else 0
            
            giro_diario = giro_30d / 30
            if giro_diario > 0:
                days = round(estoque_transito / giro_diario)
            elif estoque_transito <= 0:
                days = 0
            else:
                days = 999
                
            if estoque_transito <= 0:
                status = "Ruptura"
            elif days < 15:
                status = "Crítico"
            elif days <= 60:
                status = "Saudável"
            else:
                status = "Excesso"
                
            cds_associados = cd_map.get(cod, [])
            estoque_cd_total = sum(cd['qtde'] for cd in cds_associados)
            cds_nomes = ", ".join(list(set([cd['filial'] for cd in cds_associados])))

            products.append({
                "Código Prod.": cod,
                "Descrição": str(row[col_name]) if col_name else f"Produto {cod}",
                "Curva": valid_skus[cod],
                "Custo R$": float(row[col_custo]) if col_custo and pd.notna(row[col_custo]) else 0.0,
                "Estoque Físico": int(row[col_qtde]) if col_qtde and pd.notna(row[col_qtde]) else 0,
                "Giro 30d": giro_30d,
                "Estoque Trânsito": estoque_transito,
                "Dias Cobertura": days,
                "Status": status,
                "Total em CDs": estoque_cd_total,
                "CDs Parceiros": cds_nomes
            })
            
    df_final = pd.DataFrame(products)
    
    # Salvar cache persistente (memória UX)
    df_final.to_pickle(CACHE_FILE)
    
    return df_final

def load_memory():
    if os.path.exists(CACHE_FILE):
        return pd.read_pickle(CACHE_FILE)
    return None

def clear_memory():
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
    if 'df' in st.session_state:
        del st.session_state['df']
    st.cache_data.clear()

# ==========================================
# INTERFACE PRINCIPAL
# ==========================================
def main():
    inject_custom_css()
    
    # Recupera memória (se existir) na session_state para manter a tela limpa
    if 'df' not in st.session_state:
        cached_df = load_memory()
        if cached_df is not None:
            st.session_state['df'] = cached_df

    if 'df' not in st.session_state:
        # TELA DE ONBOARDING
        st.markdown('<br>', unsafe_allow_html=True)
        st.info("👋 Bem-vindo ao StokeFlow! Carregue as 3 planilhas para gerar o seu painel instantâneo.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            file_curvas = st.file_uploader("1. Produtos por Curva (Excel)", type=['xlsx', 'xls'])
        with col2:
            file_darkstore = st.file_uploader("2. Estoque Darkstore (Excel)", type=['xlsx', 'xls'])
        with col3:
            file_cds = st.file_uploader("3. Estoque CDs (Excel)", type=['xlsx', 'xls'])
            
        if st.button("Processar Dados", type="primary", use_container_width=True):
            if file_curvas and file_darkstore and file_cds:
                with st.spinner("Extraindo e processando dados..."):
                    df = process_data(file_curvas, file_darkstore, file_cds)
                    st.session_state['df'] = df
                    st.rerun()
            else:
                st.error("Por favor, faça o upload das 3 planilhas para prosseguir.")
        return

    # TELA DO DASHBOARD (Memória Carregada)
    df = st.session_state['df']
    
    render_header()
    
    # ------------------------------------------
    # FILTROS PRINCIPAIS (EXPANDER)
    # ------------------------------------------
    with st.expander("⚙️ Filtros e Pesquisa", expanded=True):
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        
        with col_f1:
            search_query = st.text_input("🔍 Buscar por Código ou Descrição", "")
            action_buttons_container = st.empty()
                
        with col_f2:
            all_curvas = sorted(df['Curva'].unique().tolist())
            selected_curvas = st.multiselect("Curva", all_curvas, default=all_curvas)
            
        with col_f3:
            all_status = ["Ruptura", "Crítico", "Saudável", "Excesso"]
            selected_status = st.multiselect("Status", all_status, default=all_status)
            
        with col_f4:
            cd_sets = df['CDs Parceiros'].dropna().apply(lambda x: [cd.strip() for cd in x.split(',') if cd.strip()])
            all_cds = sorted(list(set([item for sublist in cd_sets for item in sublist])))
            selected_cds = st.multiselect("Distribuidoras (CDs)", all_cds, default=all_cds)

    # ------------------------------------------
    # APLICAÇÃO DE FILTROS
    # ------------------------------------------
    mask = df['Curva'].isin(selected_curvas) & df['Status'].isin(selected_status)
    
    if search_query:
        query_lower = search_query.lower()
        search_mask = df['Descrição'].str.lower().str.contains(query_lower) | df['Código Prod.'].astype(str).str.contains(query_lower)
        mask = mask & search_mask
        
    if len(selected_cds) < len(all_cds):
        def has_selected_cd(cd_str):
            if not cd_str: return False
            row_cds = [c.strip() for c in cd_str.split(',')]
            return any(c in selected_cds for c in row_cds)
        
        cd_mask = df['CDs Parceiros'].apply(has_selected_cd)
        mask = mask & cd_mask

    df_filtered = df[mask]

    # ------------------------------------------
    # BOTÕES DE AÇÃO E EXPORTAÇÃO
    # ------------------------------------------
    with action_buttons_container.container():
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("🔄 Novos Arquivos", use_container_width=True):
                clear_memory()
                st.rerun()
        with btn_col2:
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_filtered.to_excel(writer, index=False, sheet_name='Inventário')
                # Ajuste automático de largura de colunas para excel "bem formatado"
                worksheet = writer.sheets['Inventário']
                for idx, col in enumerate(df_filtered.columns):
                    max_len = max(df_filtered[col].astype(str).map(len).max(), len(col)) + 2
                    worksheet.column_dimensions[chr(65 + idx)].width = min(max_len, 40)
            
            st.download_button(
                label="📥 Exportar Excel",
                data=output.getvalue(),
                file_name="Inventario_Filtrado_StokeFlow.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

    # ------------------------------------------
    # KPIS SUPERIORES
    # ------------------------------------------
    total_skus = len(df_filtered)
    total_rupturas = len(df_filtered[df_filtered['Status'] == 'Ruptura'])
    pct_ruptura = (total_rupturas / total_skus * 100) if total_skus > 0 else 0
    
    df_valid_cov = df_filtered[df_filtered['Estoque Trânsito'] > 0]
    avg_cobertura = df_valid_cov['Dias Cobertura'].mean() if not df_valid_cov.empty else 0
    
    saldo_cd_total = df_filtered['Total em CDs'].sum()
    cds_unicos_list = list(set([item for sublist in df_filtered['CDs Parceiros'].dropna().apply(lambda x: [cd.strip() for cd in x.split(',') if cd.strip()]) for item in sublist]))
    cds_unicos = len(cds_unicos_list)
    
    render_kpis(
        skus=total_skus, 
        cds_mapped=cds_unicos, 
        rupturas=total_rupturas, 
        pct_ruptura=pct_ruptura, 
        avg_cobertura=avg_cobertura, 
        saldo_cd=saldo_cd_total
    )

    # ------------------------------------------
    # GRÁFICOS
    # ------------------------------------------
    col_chart1, col_chart2 = st.columns([2, 1])
    
    with col_chart1:
        with st.container(border=True):
            st.markdown('<p class="chart-title"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg> Dias de Cobertura de Estoque c/ Trânsito por SKU</p>', unsafe_allow_html=True)
            df_valid_charts = df_filtered[df_filtered['Dias Cobertura'] < 999]
            df_top10 = df_valid_charts.sort_values(by="Dias Cobertura", ascending=False).head(10)
            
            if not df_top10.empty:
                df_top10['Label'] = df_top10['Descrição'].apply(lambda x: x[:20] + "..." if len(x) > 20 else x)
                fig_bar = px.bar(df_top10, x='Label', y='Dias Cobertura', 
                                 color_discrete_sequence=['#6366f1']) # Indigo blue
                
                fig_bar.update_layout(xaxis_title="", yaxis_title="Dias de Cobertura", margin=dict(l=0, r=0, t=10, b=0), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("Nenhum dado para exibir.")

    with col_chart2:
        with st.container(border=True):
            st.markdown('<p class="chart-title"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"></path><path d="M22 12A10 10 0 0 0 12 2v10z"></path></svg> Saúde do Catálogo (Darkstore)</p>', unsafe_allow_html=True)
            status_counts = df_filtered['Status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Quantidade']
            
            color_map = {
                'Ruptura': '#e11d48',
                'Crítico': '#f59e0b',
                'Saudável': '#10b981',
                'Excesso': '#3b82f6'
            }
            
            if not status_counts.empty:
                fig_pie = px.pie(status_counts, values='Quantidade', names='Status', hole=0.6,
                                 color='Status', color_discrete_map=color_map)
                fig_pie.update_layout(margin=dict(l=0, r=0, t=10, b=0), showlegend=False, paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("Nenhum dado.")

    # ------------------------------------------
    # TABELA PRINCIPAL
    # ------------------------------------------
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('**Inventário Detalhado**')
    
    st.dataframe(
        df_filtered,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Código Prod.": st.column_config.TextColumn("Cód.", width="small"),
            "Descrição": st.column_config.TextColumn("Descrição do Item", width="large"),
            "Custo R$": st.column_config.NumberColumn("Custo Total", format="R$ %.2f"),
            "Estoque Físico": st.column_config.NumberColumn("Estoque Loja"),
            "Giro 30d": st.column_config.NumberColumn("Giro Mensal"),
            "Estoque Trânsito": st.column_config.NumberColumn("C/ Trânsito"),
            "Dias Cobertura": st.column_config.ProgressColumn(
                "Cobertura",
                help="Dias de cobertura projetados",
                format="%d d",
                min_value=0,
                max_value=120,
            ),
            "Total em CDs": st.column_config.NumberColumn("Total CDs Parceiros"),
            "Status": st.column_config.TextColumn("Status de Saúde")
        }
    )

if __name__ == '__main__':
    main()
