import pandas as pd
import matplotlib.pyplot as plt

def generate_report():
    # Load CSV
    df = pd.read_csv('summary.csv')

    # Overall stats
    total_spins = len(df)
    total_win = df['WinAmount'].sum()
    rtp = total_win / total_spins

    print(f"Total Spins: {total_spins}")
    print(f"Total Win: {total_win:.2f}")
    print(f"RTP: {rtp:.4f}")

    # Symbol-wise analysis
    symbol_stats = df.groupby('WinningSymbol')['WinAmount'].agg(['count', 'sum'])
    symbol_stats['RTP'] = symbol_stats['sum'] / total_spins
    symbol_stats = symbol_stats.sort_values(by='RTP', ascending=False)
    print("\nSymbol Stats:\n", symbol_stats)

    # Plot RTP contribution
    plt.figure(figsize=(8,5))
    symbol_stats['RTP'].plot(kind='bar', color='skyblue')
    plt.title('Symbol RTP Contribution')
    plt.ylabel('RTP')
    plt.tight_layout()
    plt.savefig('symbol_rtp.png')
    plt.close()

    # Volatility proxy: standard deviation of spin results
    volatility = df['WinAmount'].std()
    print(f"\nEstimated Volatility (std dev): {volatility:.4f}")

    # Histogram of all wins
    plt.hist(df['WinAmount'], bins=50, color='orange', edgecolor='black')
    plt.title('Distribution of Win Amounts')
    plt.xlabel('Win Amount')
    plt.ylabel('Frequency')
    plt.savefig('win_distribution.png')
    plt.close()

if __name__ == "__main__":
    generate_report()
