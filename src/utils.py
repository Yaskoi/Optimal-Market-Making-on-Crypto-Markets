import os
import pandas as pd
import numpy as np
import time


def export_trade_logs(trades_df: pd.DataFrame,
                      ses: pd.DataFrame,
                      output_path: str = 'trade_logs.csv') -> pd.DataFrame:
    """
    Export individual trade logs to CSV, enriched with session-level metrics.

    Parameters
    ----------
    trades_df   : DataFrame returned by run_backtest() (4th element)
    ses         : Session DataFrame returned by run_backtest() (2nd element)
    output_path : Output CSV file path

    Exported columns
    ----------------
    date, timestamp, side,
    decision_price, fill_price, slippage_$,
    commission_$, adv_sel_$, total_friction_$,
    inventory_after, mid, bid, ask, spread_$, spread_bps,
    sigma_t, t_rem_min, fut_ret_$,
    session_pnl, session_n_trades, session_final_inv  ← joined from ses

    Returns
    -------
    Enriched DataFrame (trades + session metrics).
    """

    if trades_df.empty:
        print('[export] No trades to export.')
        return trades_df

    # Join session-level metrics onto each individual trade
    ses_slim = ses[['date', 'pnl', 'n_trades', 'final_inv']].rename(columns={
        'pnl':       'session_pnl',
        'n_trades':  'session_n_trades',
        'final_inv': 'session_final_inv',
    })
    df = trades_df.merge(ses_slim, on='date', how='left')

    # Write to CSV
    df.to_csv(output_path, index=False)

    # Summary print
    date_min = df['date'].min()
    date_max = df['date'].max()
    n_sessions = df['date'].nunique()
    trades_per_day = len(df) / max(n_sessions, 1)

    print(f'[export] {len(df):,} trades → {output_path}')
    print(f'[export] Period      : {date_min} → {date_max}')
    print(f'[export] Sessions    : {n_sessions} days with trades')
    print(f'[export] Trades/day  : {trades_per_day:.1f} on average')
    print(f'[export] Columns     : {list(df.columns)}')

    return df