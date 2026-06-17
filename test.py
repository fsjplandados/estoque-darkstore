def test_format():
    rupturas=10
    pct_ruptura=50.123
    skus=10
    cds_mapped=5
    avg_cobertura = 12
    saldo_cd_str = "1200"

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
    print(html)

test_format()
