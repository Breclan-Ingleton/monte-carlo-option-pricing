import numpy as np
import matplotlib.pyplot as plt

from monte_carlo_option_pricing import monte_carlo_gbm_option_price
from black_scholes import black_scholes_option_price


def discounted_gbm_call_payoffs(S0, K, r, sigma, T, N):
    """
    Simulate discounted call option payoffs using geometric Brownian motion.
    """

    Z = np.random.normal(0, 1, N)

    S_T = S0 * np.exp((r - 0.5 * sigma**2)*T + sigma*np.sqrt(T) * Z)

    payoffs = np.maximum(S_T - K, 0)

    discounted_payoffs = np.exp(-r*T) * payoffs

    return discounted_payoffs


def plot_monte_carlo_convergence():
    """
    Plot Monte Carlo call and put prices against the number of simulations.
    """

    S0 = 100
    K = 100
    r = 0.05
    sigma = 0.2
    T = 1

    simulation_counts = [100, 500, 1000, 5000, 10000, 50000, 100000]

    call_prices = []
    put_prices = []

    for N in simulation_counts:
        call_price = monte_carlo_gbm_option_price(S0, K, r, sigma, T, N, "call")
        put_price = monte_carlo_gbm_option_price(S0, K, r, sigma, T, N, "put")

        call_prices.append(call_price)
        put_prices.append(put_price)

    black_scholes_call = black_scholes_option_price(S0, K, r, sigma, T, "call")
    black_scholes_put = black_scholes_option_price(S0, K, r, sigma, T, "put")

    plt.plot(simulation_counts, call_prices, marker="o", label="Monte Carlo call")
    plt.plot(simulation_counts, put_prices, marker="o", label="Monte Carlo put")

    plt.axhline(black_scholes_call, linestyle="--", label="Black-Scholes call")
    plt.axhline(black_scholes_put, linestyle="--", label="Black-Scholes put")

    plt.xscale("log")
    plt.title("GBM Monte Carlo Convergence")
    plt.xlabel("Number of simulations")
    plt.ylabel("Estimated option price")
    plt.legend()

    os.makedirs("plots", exist_ok=True)
    plt.savefig("plots/gbm_convergence_plot.png", dpi=300, bbox_inches="tight")
    plt.show()


def plot_confidence_interval_width():
    """
    Plot 95% confidence interval width against the number of simulations.
    """

    S0 = 100
    K = 100
    r = 0.05
    sigma = 0.2
    T = 1

    simulation_counts = [100, 500, 1000, 5000, 10000, 50000, 100000]

    ci_widths = []

    for N in simulation_counts:
        discounted_payoffs = discounted_gbm_call_payoffs(S0, K, r, sigma, T, N)

        sample_sd = np.std(discounted_payoffs, ddof=1)
        standard_error = sample_sd / np.sqrt(N)

        ci_width = 2 * 1.96 * standard_error
        ci_widths.append(ci_width)

    plt.plot(simulation_counts, ci_widths, marker="o")

    plt.xscale("log")
    plt.title("Confidence Interval Width vs Number of Simulations")
    plt.xlabel("Number of simulations")
    plt.ylabel("95% confidence interval width")

    plt.savefig("gbm_convergence_plot.png", dpi=300, bbox_inches="tight")
    plt.savefig("gbm_ci_width_vs_simulations.png", dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    np.random.seed(42)

    plot_monte_carlo_convergence()
    plot_confidence_interval_width()
