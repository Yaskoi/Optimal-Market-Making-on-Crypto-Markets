import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def plot_results(st_is_nf, st_is_f, st_oos_nf, st_oos_f, ticker, model,
                 save_path: str = None):
    """
    Plot backtest results in a light theme.

    Parameters
    ----------
    st_is_nf  : stats dict — IS without frictions
    st_is_f   : stats dict — IS with frictions
    st_oos_nf : stats dict — OOS without frictions
    st_oos_f  : stats dict — OOS with frictions
    ticker    : str — asset name
    model     : str — model label
    save_path : str or None — if provided, saves figure to this path (300 dpi)
    """

    # ── Color palette ──
    BG    = '#ffffff'   # white background
    PANEL = '#f7f8fc'   # very light gray panels
    DARK  = '#1e2130'   # near-black for text/lines
    GRAY  = '#6b7280'   # medium gray for labels
    GRID  = '#e5e7eb'   # light gray grid

    BLUE  = '#2563eb'   # strong blue  — no-friction line / buy inventory
    ORNG  = '#ea580c'   # burnt orange — with-friction IS line
    YELL  = '#d97706'   # amber        — with-friction OOS line / mean line
    GREEN = '#16a34a'   # green        — positive area fill
    RED   = '#dc2626'   # red          — negative area fill / sell inventory
    TEAL  = '#0891b2'   # teal         — commission bar

    plt.rcParams.update({
        'font.family':     'serif',
        'font.size':       9,
        'axes.labelcolor': GRAY,
        'xtick.color':     GRAY,
        'ytick.color':     GRAY,
    })

    def style(ax, title):
        """Apply light report theme to an axis."""
        ax.set_facecolor(PANEL)
        ax.set_title(title, color=DARK, fontsize=8.5, pad=6,
                     loc='left', fontweight='bold')
        ax.tick_params(colors=GRAY, labelsize=7.5)
        for sp in ax.spines.values():
            sp.set_edgecolor(GRID)
        ax.grid(True, color=GRID, lw=0.6, ls='--', zorder=0)

    fig = plt.figure(figsize=(12, 14))
    fig.patch.set_facecolor(BG)
    gs  = gridspec.GridSpec(4, 2, hspace=0.60, wspace=0.35)

    # ── IS cumulative P&L ──
    ax1 = fig.add_subplot(gs[0, 0])
    style(ax1, 'Cumulative P&L — IS')
    c_nf, c_f = st_is_nf['cum'], st_is_f['cum']
    ax1.plot(c_nf, color=BLUE, lw=1.4, ls='--',
             label=f'No frictions  ${c_nf[-1]:+,.0f}')
    ax1.plot(c_f,  color=ORNG, lw=1.4,
             label=f'With frictions  ${c_f[-1]:+,.0f}')
    ax1.fill_between(range(len(c_f)), c_f, 0,
                     where=np.array(c_f) >= 0, alpha=0.08, color=GREEN)
    ax1.fill_between(range(len(c_f)), c_f, 0,
                     where=np.array(c_f) <  0, alpha=0.08, color=RED)
    ax1.axhline(0, color=GRAY, lw=0.7, ls=':')
    ax1.set_xlabel('Session (#)', fontsize=8)
    ax1.set_ylabel('P&L ($)', fontsize=8)
    ax1.legend(fontsize=7.5, framealpha=0.8, facecolor=BG,
               edgecolor=GRID, labelcolor=DARK)

    # ── OOS cumulative P&L ──
    ax2 = fig.add_subplot(gs[0, 1])
    style(ax2, 'Cumulative P&L — OOS')
    c_nf2, c_f2 = st_oos_nf['cum'], st_oos_f['cum']
    ax2.plot(c_nf2, color=BLUE, lw=1.4, ls='--',
             label=f'No frictions  ${c_nf2[-1]:+,.0f}')
    ax2.plot(c_f2,  color=YELL, lw=1.4,
             label=f'With frictions  ${c_f2[-1]:+,.0f}')
    ax2.fill_between(range(len(c_f2)), c_f2, 0,
                     where=np.array(c_f2) >= 0, alpha=0.08, color=GREEN)
    ax2.fill_between(range(len(c_f2)), c_f2, 0,
                     where=np.array(c_f2) <  0, alpha=0.08, color=RED)
    ax2.axhline(0, color=GRAY, lw=0.7, ls=':')
    ax2.set_xlabel('Session (#)', fontsize=8)
    ax2.set_ylabel('P&L ($)', fontsize=8)
    ax2.legend(fontsize=7.5, framealpha=0.8, facecolor=BG,
               edgecolor=GRID, labelcolor=DARK)

    # ── IS friction decomposition ──
    ax3 = fig.add_subplot(gs[1, 0])
    style(ax3, 'Frictions / session — IS')
    ses_i  = st_is_f['ses']
    cats   = ['Commission', 'Slippage', 'Adv. sel.']
    vi     = [ses_i['comm'].mean(), ses_i['slippage'].mean(),
              ses_i['adv_sel'].mean()]
    cols_b = [TEAL, ORNG, RED]
    bars   = ax3.bar(cats, vi, color=cols_b, alpha=0.85,
                     edgecolor='white', linewidth=0.8, zorder=3)
    for bar, v in zip(bars, vi):
        ax3.text(bar.get_x() + bar.get_width()/2, v + max(vi)*0.01,
                 f'${v:.1f}', ha='center', va='bottom',
                 color=DARK, fontsize=8, fontweight='bold')
    ax3.set_ylabel('$ / session', fontsize=8)

    # ── OOS friction decomposition ──
    ax4 = fig.add_subplot(gs[1, 1])
    style(ax4, 'Frictions / session — OOS')
    ses_o = st_oos_f['ses']
    vo    = [ses_o['comm'].mean(), ses_o['slippage'].mean(),
             ses_o['adv_sel'].mean()]
    bars2 = ax4.bar(cats, vo, color=cols_b, alpha=0.85,
                    edgecolor='white', linewidth=0.8, zorder=3)
    for bar, v in zip(bars2, vo):
        ax4.text(bar.get_x() + bar.get_width()/2, v + max(vo)*0.01,
                 f'${v:.1f}', ha='center', va='bottom',
                 color=DARK, fontsize=8, fontweight='bold')
    ax4.set_ylabel('$ / session', fontsize=8)

    # ── IS final inventory distribution ──
    ax5 = fig.add_subplot(gs[2, 0])
    style(ax5, 'Final inventory IS — distribution per session')
    inv_is = st_is_f['ses']['final_inv']
    ax5.bar(range(len(inv_is)), inv_is,
            color=np.where(inv_is >= 0, BLUE, RED),
            alpha=0.75, edgecolor='white', linewidth=0.4, width=0.8, zorder=3)
    ax5.axhline(0, color=GRAY, lw=0.7, ls=':')
    ax5.axhline(inv_is.mean(), color=DARK, lw=1.2, ls='--',
                label=f'Mean = {inv_is.mean():.2f}')
    ax5.set_xlabel('Session (#)', fontsize=8)
    ax5.set_ylabel('Final inventory (BTC)', fontsize=8)
    ax5.legend(fontsize=7.5, framealpha=0.8, facecolor=BG,
               edgecolor=GRID, labelcolor=DARK)

    # ── OOS final inventory distribution ──
    ax6 = fig.add_subplot(gs[2, 1])
    style(ax6, 'Final inventory OOS — distribution per session')
    inv_oos = st_oos_f['ses']['final_inv']
    ax6.bar(range(len(inv_oos)), inv_oos,
            color=np.where(inv_oos >= 0, BLUE, RED),
            alpha=0.75, edgecolor='white', linewidth=0.4, width=0.8, zorder=3)
    ax6.axhline(0, color=GRAY, lw=0.7, ls=':')
    ax6.axhline(inv_oos.mean(), color=DARK, lw=1.2, ls='--',
                label=f'Mean = {inv_oos.mean():.2f}')
    ax6.set_xlabel('Session (#)', fontsize=8)
    ax6.set_ylabel('Final inventory (BTC)', fontsize=8)
    ax6.legend(fontsize=7.5, framealpha=0.8, facecolor=BG,
               edgecolor=GRID, labelcolor=DARK)

    # ── OOS P&L waterfall — gross vs. net per session ──
    ax7 = fig.add_subplot(gs[3, :])
    style(ax7, 'P&L waterfall OOS — gross vs. net per session')
    gross = st_oos_nf['pnls']
    net   = st_oos_f['pnls']
    x     = np.arange(len(gross))
    w     = 0.38
    ax7.bar(x - w/2, gross, w, color=BLUE, alpha=0.80,
            label='Gross P&L', edgecolor='white', linewidth=0.4, zorder=3)
    ax7.bar(x + w/2, net,   w, color=YELL, alpha=0.80,
            label='Net P&L',   edgecolor='white', linewidth=0.4, zorder=3)
    ax7.axhline(0, color=GRAY, lw=0.7, ls=':')
    ax7.set_xlabel('OOS Session (#)', fontsize=8)
    ax7.set_ylabel('P&L ($)', fontsize=8)
    ax7.legend(fontsize=7.5, framealpha=0.8, facecolor=BG,
               edgecolor=GRID, labelcolor=DARK)

    plt.suptitle(
        f'{model}  |  {ticker} 1s  |  IS (Jul–Nov) vs OOS (Dec)'
        f'  |  Realistic transaction costs',
        color=DARK, fontsize=11, fontweight='bold', y=1.002
    )

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight', facecolor=BG)
        print(f'[plot] Figure saved → {save_path}')

    plt.show()