import numpy as np
from datetime import datetime, timedelta

def compute_dtw_matrix(x, y, window=5):
    N, M = len(x), len(y)
    # Initialize with Infinity
    dtw_matrix = np.full((N + 1, M + 1), np.inf)
    dtw_matrix[0, 0] = 0
    
    # Sakoe-Chiba constraint band
    w = max(window, abs(N - M))
    
    for i in range(1, N + 1):
        # Only calculate within the diagonal band
        for j in range(max(1, i - w), min(M + 1, i + w + 1)):
            cost = abs(x[i - 1] - y[j - 1])
            dtw_matrix[i, j] = cost + min(
                dtw_matrix[i - 1, j],    # insertion
                dtw_matrix[i, j - 1],    # deletion
                dtw_matrix[i - 1, j - 1] # match
            )
    return dtw_matrix

def compare_dtw_patterns(target_pattern, historical_prices, price_window=50, dtw_window=5):
    """
    Compares a SINGLE target price pattern against all historical prices.
    """
    results = []
    
    # Extract just the numeric price data for the SINGLE target pattern
    t_seq = target_pattern[:price_window]
    t_dates = target_pattern[-2] 
    
    # Iterate through all tickers in the historical dictionary
    for ticker, hist_patterns in historical_prices.items():
        for h_idx, hist_pattern in enumerate(hist_patterns):
            
            # Extract just the numeric price data and metadata for the historical pattern
            h_seq = hist_pattern[:price_window]
            h_future_change = hist_pattern[-3]
            h_dates = hist_pattern[-2]
            
            # Compute the matrix using your DTW function
            dtw_mat = compute_dtw_matrix(t_seq, h_seq, window=dtw_window)
            
            # The DTW distance score is the bottom-right value of the matrix
            dtw_distance = dtw_mat[-1, -1]
            
            results.append({
                "historical_ticker": ticker,
                "historical_dates_end": h_dates[0].strftime('%Y-%m-%d'),
                "historical_dates_start": h_dates[1].strftime('%Y-%m-%d'),
                "dtw_distance": dtw_distance,
                "future_change_%": round(h_future_change * 100, 2),
                "prices": h_seq
            })

            
    # Sort the results so the closest DTW matches (lowest distance) appear first
    sorted_results = sorted(results, key=lambda x: x["dtw_distance"])
    return sorted_results

def get_top_matches(target_pattern, historical_prices, price_window=50, dtw_window=5, n_top_match=10, blackout_window=50):
    sorted_results = compare_dtw_patterns(target_pattern, historical_prices, price_window, dtw_window)

    top_matches = []

    for result in sorted_results:
        historical_date_end = datetime.strptime(result["historical_dates_end"], "%Y-%m-%d").date()

        if len(top_matches) > n_top_match:
            break
        
        add_date = True

        for matched in top_matches:
            matched = datetime.strptime(matched["historical_dates_end"], "%Y-%m-%d").date() 

            if historical_date_end < matched + timedelta(days=blackout_window) and historical_date_end > matched - timedelta(days=blackout_window):
                add_date = False

        if add_date:
            top_matches.append(result)

    return top_matches