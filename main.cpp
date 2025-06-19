#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cmath>

struct SpinData {
    int spinNumber;
    double winAmount;
    std::string winningSymbol;
};

int main() {
    std::ifstream file("summary.csv");
    if (!file.is_open()) {
        std::cerr << "Error: Could not open summary.csv\n";
        return 1;
    }

    std::vector<SpinData> spins;
    std::string line;
    std::getline(file, line); // Skip header

    // Read data
    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::string token;
        SpinData spin;

        std::getline(ss, token, ',');
        spin.spinNumber = std::stoi(token);

        std::getline(ss, token, ',');
        spin.winAmount = std::stod(token);

        std::getline(ss, token, ',');
        spin.winningSymbol = token;

        // Optional 4th column: ReelsMatched
        spins.push_back(spin);
    }

    // Calculate RTP and volatility
    double totalWin = 0.0, sumSquared = 0.0;
    for (const auto& spin : spins) {
        totalWin += spin.winAmount;
        sumSquared += spin.winAmount * spin.winAmount;
    }

    int totalSpins = spins.size();
    double rtp = totalWin / totalSpins;
    double mean = rtp;
    double variance = (sumSquared / totalSpins) - (mean * mean);
    double stddev = std::sqrt(variance);

    std::cout << "📊 VolatilityTuner Summary\n";
    std::cout << "----------------------------\n";
    std::cout << "Total Spins: " << totalSpins << "\n";
    std::cout << "Total Win: " << totalWin << "\n";
    std::cout << "RTP: " << rtp << "\n";
    std::cout << "Estimated Volatility (std dev): " << stddev << "\n";

    return 0;
}
