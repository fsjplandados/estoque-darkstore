import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

CACHE_FILE = "stokeflow_cache.pkl"

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="StokeFlow - Darkstore São João",
    page_icon="estoque.png",
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
            [data-testid="stHeader"] {display: none !important;}
            .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }

            /* Header Customizado Estilo Tailwind / Modern SaaS */
            .custom-header {
                background-color: white; border-bottom: 1px solid #e2e8f0; padding: 0.5rem 5rem;
                display: flex; justify-content: space-between; align-items: center;
                margin-left: -5rem; margin-right: -5rem; margin-top: -1rem; margin-bottom: 1.5rem;
                box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
            }
            .header-left { display: flex; align-items: center; gap: 1.5rem; }
            .header-divider { width: 1px; height: 32px; background-color: #e2e8f0; }
            .header-title-row { display: flex; align-items: center; gap: 0.75rem; }
            .header-title { font-size: 1.25rem; font-weight: 800; color: #0f172a; margin: 0; line-height: 1; letter-spacing: -0.02em;}
            .header-subtitle { font-size: 0.85rem; color: #64748b; margin: 0; font-weight: 500;}
            .badge-darkstore { background-color: #f8fafc; color: #475569; font-size: 0.65rem; font-weight: 800; padding: 0.2rem 0.6rem; border-radius: 0.375rem; letter-spacing: 0.05em; border: 1px solid #e2e8f0;}
            
            .header-right { display: flex; align-items: center; gap: 1rem; }
            .sync-container { display: flex; flex-direction: column; align-items: flex-end; justify-content: center; }
            .sync-badge { display: flex; align-items: center; gap: 0.4rem; color: #059669; font-size: 0.8rem; font-weight: 700; line-height: 1;}
            .sync-dot { width: 8px; height: 8px; background-color: #10b981; border-radius: 50%; box-shadow: 0 0 0 2px #d1fae5; animation: pulse 2s infinite;}
            .sync-time { font-size: 0.7rem; color: #94a3b8; font-weight: 500; margin-top: 0.25rem;}
            
            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
                70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
                100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
            }

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

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def render_header():
    try:
        logo_b64 = get_base64_of_bin_file('logo.png')
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height: 50px; width: auto; object-fit: contain;">'
    except Exception:
        logo_html = ''

    try:
        estoque_b64 = get_base64_of_bin_file('estoque.png')
        estoque_html = f'<img src="data:image/png;base64,{estoque_b64}" style="height: 40px; width: auto; object-fit: contain;">'
    except Exception:
        estoque_html = '<div class="header-logo-box"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg></div>'

    st.markdown(f"""
        <div class="custom-header">
            <div class="header-left">
                {logo_html}
                <div class="header-divider"></div>
                <div class="header-title-row">
                    <h1 class="header-title">StokeFlow</h1>
                    <span class="badge-darkstore">DARKSTORE</span>
                    <span class="header-subtitle" style="margin-left: 0.25rem;">|&nbsp;&nbsp;&nbsp;Inteligência de Abastecimento e Controle de Ruptura</span>
                </div>
            </div>
            <div class="header-right">
                <div class="sync-container">
                    <div class="sync-badge"><div class="sync-dot"></div> CONECTADO</div>
                    <div class="sync-time">ERP Sincronizado</div>
                </div>
            </div>
        </div>
        <div class="tabs-container">
            <div class="tab-active"><svg width="16" height="16" style="display:inline; margin-bottom:-2px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg> Painel & Inventário</div>
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
def process_data(file_darkstore, file_cds):
    # 1. Carregar CDs e Consolidar
    df_cds = pd.read_excel(file_cds)
    
    col_filial = next((c for c in df_cds.columns if 'filial' in str(c).lower()), None)
    col_cod_cd = next((c for c in df_cds.columns if 'cod' in str(c).lower() and 'produto' in str(c).lower()), None)
    col_qtde_cd = next((c for c in df_cds.columns if 'qtde' in str(c).lower() and 'estoque' in str(c).lower()), None)
    
    cd_map = {}
    if col_cod_cd and col_qtde_cd:
        for _, row in df_cds.iterrows():
            cod = clean_cod(row[col_cod_cd])
            filial = str(row[col_filial]) if col_filial else "CD Padrao"
            qtde = int(row[col_qtde_cd]) if pd.notna(row[col_qtde_cd]) else 0
            if cod not in cd_map:
                cd_map[cod] = []
            if qtde > 0:
                cd_map[cod].append({"filial": filial, "qtde": qtde})
                
    # 2. Carregar Darkstore e Montar Base Final
    df_dark = pd.read_excel(file_darkstore)
    df_dark = df_dark[df_dark['Desc_Filial'].str.strip().str.upper() != 'TOTAL']
    
    col_cod = next((c for c in df_dark.columns if 'cod' in str(c).lower() and 'produto' in str(c).lower()), None)
    col_name = next((c for c in df_dark.columns if 'desc' in str(c).lower() and 'produto' in str(c).lower()), None)
    col_custo = next((c for c in df_dark.columns if 'custo' in str(c).lower() and 'estoque' in str(c).lower()), None)
    col_qtde = next((c for c in df_dark.columns if 'qtde' in str(c).lower() and 'estoque' in str(c).lower()), None)
    col_giro = next((c for c in df_dark.columns if 'giro' in str(c).lower() and '030' in str(c).lower()), None)
    col_transit = next((c for c in df_dark.columns if 'transito' in str(c).lower() and 'c/' in str(c).lower()), None)
    col_filial_dark = next((c for c in df_dark.columns if 'filial' in str(c).lower()), None)
    col_dias_estoque = next((c for c in df_dark.columns if 'dias estoque' in str(c).lower()), None)
    col_liquido = next((c for c in df_dark.columns if 'liquido' in str(c).lower()), None)
    
    if not col_transit:
        col_transit = next((c for c in df_dark.columns if 'transito' in str(c).lower()), None)

    # 3. Calcular Curva ABC Dinâmica (Pareto)
    if col_liquido and col_cod:
        df_dark[col_liquido] = pd.to_numeric(df_dark[col_liquido], errors='coerce').fillna(0)
        df_dark = df_dark.sort_values(by=col_liquido, ascending=False)
        
        soma_total = df_dark[col_liquido].clip(lower=0).sum() # Ignorar valores negativos na soma
        if soma_total > 0:
            df_dark['perc_liquido'] = df_dark[col_liquido].clip(lower=0) / soma_total
            df_dark['perc_acumulado'] = df_dark['perc_liquido'].cumsum()
        else:
            df_dark['perc_acumulado'] = 1.0
            
        def classificar_curva(acumulado, faturamento):
            if faturamento <= 0: return "CURVA C"
            if acumulado <= 0.60: return "CURVA A"
            elif acumulado <= 0.80: return "CURVA B"
            else: return "CURVA C"
            
        df_dark['Curva'] = df_dark.apply(lambda x: classificar_curva(x['perc_acumulado'], x[col_liquido]), axis=1)
    else:
        df_dark['Curva'] = "SEM CURVA"

    products = []
    for _, row in df_dark.iterrows():
        cod = clean_cod(row[col_cod]) if col_cod else None
        if cod:
            curva = str(row['Curva']) if 'Curva' in df_dark.columns else "SEM CURVA"
            giro_30d = float(row[col_giro]) if col_giro and pd.notna(row[col_giro]) else 0.0
            venda_liq = float(row[col_liquido]) if col_liquido and pd.notna(row[col_liquido]) else 0.0
            
            estoque_fisico = int(row[col_qtde]) if col_qtde and pd.notna(row[col_qtde]) else 0
            estoque_transito = int(row[col_transit]) if col_transit and pd.notna(row[col_transit]) else 0
            
            cds_associados = cd_map.get(cod, [])
            estoque_cd_total = sum(cd['qtde'] for cd in cds_associados)
            cds_nomes = ", ".join(list(set([cd['filial'] for cd in cds_associados])))
            
            products.append({
                "Filial Origem": str(row[col_filial_dark]) if col_filial_dark else "Darkstore",
                "Código Prod.": cod,
                "Descrição": str(row[col_name]) if col_name else f"Produto {cod}",
                "Curva": curva,
                "Custo R$": float(row[col_custo]) if col_custo and pd.notna(row[col_custo]) else 0.0,
                "Venda 30d (R$)": venda_liq,
                "Estoque Físico": estoque_fisico,
                "Estoque Trânsito": estoque_transito,
                "Giro 30d (Un)": giro_30d,
                "Dias Est. Original": float(row[col_dias_estoque]) if col_dias_estoque and pd.notna(row[col_dias_estoque]) else 0.0,
                "Total em CDs": estoque_cd_total,
                "CDs Parceiros": cds_nomes
            })
            
    df_final = pd.DataFrame(products)
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
        # TELA DE ONBOARDING PARA DEPLOY
        st.markdown('<br>', unsafe_allow_html=True)
        st.info("👋 Bem-vindo ao StokeFlow! Carregue os relatórios de estoque oficiais para gerar o painel inteligente.")
        
        col1, col2 = st.columns(2)
        with col1:
            file_darkstore = st.file_uploader("1. Base Darkstore (Estoque e Giro)", type=['xlsx', 'xls'])
        with col2:
            file_cds = st.file_uploader("2. Parceiros (Estoque CDs)", type=['xlsx', 'xls'])
            
        if st.button("Processar Dados", type="primary", use_container_width=True):
            if file_darkstore and file_cds:
                with st.spinner("Analisando faturamento, calculando Curvas ABC e cruzando inventário..."):
                    df = process_data(file_darkstore, file_cds)
                    st.session_state['df'] = df
                    st.rerun()
            else:
                st.error("Por favor, faça o upload das 2 planilhas obrigatórias para prosseguir.")
        return

    # TELA DO DASHBOARD (Memória Carregada)
    df = st.session_state['df']
    
    # Failsafe de Migração: se a memória na sessão for da versão antiga, força o reset
    if 'Giro 30d (Un)' not in df.columns:
        clear_memory()
        st.rerun()
    
    render_header()
    
    # ------------------------------------------
    # CÁLCULO DE COBERTURA E STATUS
    # ------------------------------------------
    df['Giro Diário'] = df['Giro 30d (Un)'] / 30.0
    
    def calculate_cobertura(row):
        transito = row['Estoque Trânsito']
        giro_d = row['Giro Diário']
        if transito <= 0:
            return 0
        if giro_d == 0 and transito > 0:
            return 999
        return round(transito / giro_d)
        
    df['Dias Cobertura'] = df.apply(calculate_cobertura, axis=1)
    
    def calculate_status(row):
        transito = row['Estoque Trânsito']
        dias = row['Dias Cobertura']
        if transito <= 0: return "Ruptura"
        if dias < 15: return "Crítico"
        if dias <= 60: return "Saudável"
        return "Excesso"
        
    df['Status'] = df.apply(calculate_status, axis=1)

    # ------------------------------------------
    # FILTROS PRINCIPAIS (EXPANDER)
    # ------------------------------------------
    with st.expander("⚙️ Filtros e Pesquisa", expanded=True):
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        
        with col_f1:
            search_query = st.text_input("🔍 Buscar por Código ou Descrição", "")
            action_buttons_container = st.empty()
                
        with col_f2:
            if df.empty:
                st.error("Nenhum dado encontrado! Verifique a classificação da curva.")
                return

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
                fig_pie.update_traces(textposition='inside', textinfo='percent+label', textfont_size=11)
                fig_pie.update_layout(
                    margin=dict(l=0, r=0, t=10, b=0), 
                    showlegend=True, 
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                    paper_bgcolor='rgba(0,0,0,0)'
                )
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
            "Filial Origem": st.column_config.TextColumn("Filial", width="small"),
            "Código Prod.": st.column_config.TextColumn("Cód.", width="small"),
            "Descrição": st.column_config.TextColumn("Descrição do Item", width="large"),
            "Custo R$": st.column_config.NumberColumn("Custo Total", format="R$ %.2f"),
            "Venda 30d (R$)": st.column_config.NumberColumn("Rotatividade 30d", format="R$ %.2f"),
            "Estoque Físico": st.column_config.NumberColumn("Estoque Loja"),
            "Giro 30d (Un)": st.column_config.NumberColumn("Giro Mensal"),
            "Estoque Trânsito": st.column_config.NumberColumn("C/ Trânsito"),
            "Dias Est. Original": st.column_config.NumberColumn("Rotatividade (Dias Est.)"),
            "Dias Cobertura": st.column_config.ProgressColumn(
                "Cobertura Calculada",
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
