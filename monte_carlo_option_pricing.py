import numpy as np


def monte_carlo_gbm_option_price(S0, K, r, sigma, T, N, option_type):
    """
    Estimate the price of a European call or put option using Monte Carlo simulation.

    The stock price is simulated using geometric Brownian motion:

        S_T = S0 * exp((r - 0.5 * sigma^2) * T + sigma * sqrt(T) * Z)

    Parameters:
        S0: initial stock price
        K: strike price
        r: risk-free interest rate
        sigma: volatility
        T: time to maturity
        N: number of simulations
        option_type: "call" or "put"

    Returns:
        Estimated option price
    """

    if option_type != "call" and option_type != "put":
        return "invalid option type"

    Z = np.random.normal(0, 1, N)

    S_T = S0 * np.exp((r - 0.5 * sigma**2)*T + sigma*np.sqrt(T) * Z)

    if option_type == "call":
        payoffs = np.maximum(S_T - K, 0)
    else:
        payoffs = np.maximum(K - S_T, 0)

    average_payoff = np.mean(payoffs)
    discounted_payoff = np.exp(-r * T) * average_payoff

    return discounted_payoff


if __name__ == "__main__":
    S0 = 100
    K = 100
    r = 0.05
    sigma = 0.2
    T = 1
    N = 100000

    call_price = monte_carlo_gbm_option_price(S0, K, r, sigma, T, N, "call")
    put_price = monte_carlo_gbm_option_price(S0, K, r, sigma, T, N, "put")

    print("Monte Carlo call price:", round(call_price, 4))
    print("Monte Carlo put price:", round(put_price, 4))

    # Black-Scholes benchmark for these parameters:
    # call ≈ 10.45
    # put ≈ 5.57
