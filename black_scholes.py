from math import log, sqrt, exp, erf


def normal_cdf(x):
    """
    Standard normal cumulative distribution function.

    This gives N(x) in the Black-Scholes formula.
    """
    return 0.5 * (1 + erf(x / sqrt(2)))


def black_scholes_option_price(S0, K, r, sigma, T, option_type):
    """
    Price a European call or put option using the Black-Scholes formula.

    Parameters:
        S0: initial stock price
        K: strike price
        r: risk-free interest rate
        sigma: volatility
        T: time to maturity
        option_type: "call" or "put"

    Returns:
        Black-Scholes option price
    """

    if option_type != "call" and option_type != "put":
        return "invalid option type"

    d1 = (log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)

    if option_type == "call":
        price = S0 * normal_cdf(d1) - K * exp(-r * T) * normal_cdf(d2)
    else:
        price = K * exp(-r * T) * normal_cdf(-d2) - S0 * normal_cdf(-d1)

    return price


if __name__ == "__main__":
    S0 = 100
    K = 100
    r = 0.05
    sigma = 0.2
    T = 1

    call_price = black_scholes_option_price(S0, K, r, sigma, T, "call")
    put_price = black_scholes_option_price(S0, K, r, sigma, T, "put")

    print("Black-Scholes call price:", round(call_price, 4))
    print("Black-Scholes put price:", round(put_price, 4))
