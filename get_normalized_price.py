def get_normalized_prices(prices, ticker, window=50):
    if prices["Date"].iloc[0] < prices["Date"].iloc[-1]:
        prices = prices[::-1].reset_index(drop=True)

    normalized_prices = []

    for i in range(len(prices["Close"])):
        if i + window >= len(prices["Close"]):
            break

        temp = prices["Close"].iloc[i:i+window]
        temp = (temp - min(temp)) / (max(temp) - min(temp))
        
        per_change = (prices["Close"].iloc[i + window] - prices["Close"].iloc[i + window - 1]) / prices["Close"].iloc[i + window - 1]
        
        temp = list(temp)
        # temp.append(per_change)
        
        # temp.append([prices["Date"].iloc[i], prices["Date"].iloc[i + window - 1]])
        # temp.append(ticker)
        normalized_prices.append(temp)
    return normalized_prices