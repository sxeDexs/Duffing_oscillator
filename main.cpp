#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>
#include <random>
#include <array>

struct State {
    double x;
    double v;
};

void duffing(const State& s, State& dsdt, double t, 
             double delta, double alpha, double beta, double gamma, double omega) {
    dsdt.x = s.v;
    dsdt.v = -delta * s.v - alpha * s.x - beta * s.x * s.x * s.x
             + gamma * std::cos(omega * t);
}

void rk_step(State& s, double t, double dt, 
             const std::vector<double>& c, 
             const std::vector<std::vector<double>>& a,
             const std::vector<double>& b,
             double delta, double alpha, double beta, double gamma, double omega) {
    int stages = c.size();
    std::vector<State> k(stages);
    State s_temp = s;

    for (int i = 0; i < stages; i++) {
        State sum_a_k = {0.0, 0.0};
        for (int j = 0; j < i; j++) {
            sum_a_k.x += a[i][j] * k[j].x;
            sum_a_k.v += a[i][j] * k[j].v;
        }
        s_temp.x = s.x + dt * sum_a_k.x;
        s_temp.v = s.v + dt * sum_a_k.v;
        duffing(s_temp, k[i], t + c[i] * dt, delta, alpha, beta, gamma, omega);
    }

    State ds = {0.0, 0.0};
    for (int i = 0; i < stages; i++) {
        ds.x += b[i] * k[i].x;
        ds.v += b[i] * k[i].v;
    }
    s.x += dt * ds.x;
    s.v += dt * ds.v;
}

int main() {
    double delta = 0.00001;
    double alpha = 0.5;
    double beta = 0.0625;
    double gamma = 5;
    double omega = 2.0;
    
    double dt = 0.01;
    double T = 200.0;
    int steps = static_cast<int>(T / dt);
    int N = 1000;

    std::vector<double> c_rk4 = {0.0, 0.5, 0.5, 1.0};
    std::vector<std::vector<double>> a_rk4 = {
        {0.0}, {0.5, 0.0}, {0.0, 0.5, 0.0}, {0.0, 0.0, 1.0}
    };
    std::vector<double> b_rk4 = {1.0/6.0, 1.0/3.0, 1.0/3.0, 1.0/6.0};

    std::vector<double> c_dp = {
        0.0, 1.0/18.0, 1.0/12.0, 1.0/8.0, 5.0/16.0, 3.0/8.0, 
        59.0/400.0, 93.0/200.0, 5490023248.0/9719169821.0, 
        13.0/20.0, 1201146811.0/1299019798.0, 1.0, 1.0
    };
    std::vector<std::vector<double>> a_dp = {
        {0.0},
        {1.0/18.0, 0.0},
        {1.0/48.0, 1.0/16.0, 0.0},
        {1.0/32.0, 0.0, 3.0/32.0, 0.0},
        {5.0/16.0, 0.0, -75.0/64.0, 75.0/64.0, 0.0},
        {3.0/80.0, 0.0, 0.0, 3.0/16.0, 3.0/20.0, 0.0},
        {29443841.0/614563906.0, 0.0, 0.0, 77736538.0/692538347.0, -28693883.0/1125000000.0, 23124283.0/1800000000.0, 0.0},
        {16016141.0/946692911.0, 0.0, 0.0, 61564180.0/158732637.0, 22789713.0/633445777.0, 545815736.0/2771057229.0, -180193667.0/1043307555.0, 0.0},
        {39632708.0/573591083.0, 0.0, 0.0, -433636366.0/683701615.0, -421739975.0/2616292301.0, 100302831.0/723423059.0, 790204164.0/839813087.0, 800635310.0/3783071287.0, 0.0},
        {246121993.0/1340847787.0, 0.0, 0.0, -37695042795.0/15268766246.0, -309121744.0/1061227803.0, -12992083.0/490766935.0, 6005943493.0/2108947869.0, 393006217.0/1396673457.0, 123872331.0/1001029789.0, 0.0},
        {-1028468189.0/846180014.0, 0.0, 0.0, 8478235783.0/508512852.0, 1311729495.0/1432422823.0, -10304129995.0/1701304382.0, -48777925059.0/3047939560.0, 15336726248.0/1032824649.0, -45442868181.0/3398467696.0, 3065993473.0/597172653.0, 0.0},
        {185892177.0/718116043.0, 0.0, 0.0, -3185094517.0/667107341.0, -477755414.0/1098053517.0, -703635378.0/230739211.0, 5731566787.0/1027545527.0, 5232866602.0/850066563.0, -4093664535.0/808688257.0, 3962137247.0/1805957418.0, 65686358.0/487910083.0, 0.0},
        {403863854.0/491063109.0, 0.0, 0.0, -5068492393.0/434740067.0, -411421997.0/543043805.0, 652783627.0/914296604.0, 11173962825.0/925320556.0, -13158990841.0/6184727034.0, 3936647629.0/1978049680.0, -160528059.0/685178525.0, 248638103.0/1413531060.0, 0.0}
    };
    std::vector<double> b_dp = {
        13451932.0/455176623.0, 0.0, 0.0, 0.0, 0.0, 
        -808719846.0/976000145.0, 1757004468.0/5645159321.0, 
        656045339.0/265891186.0, -3867574721.0/1518517206.0, 
        465885868.0/322736535.0, 53011238.0/667516719.0, 2.0/45.0, 0.0
    };

    std::vector<State> particles_rk4(N);
    std::vector<State> particles_dp(N);

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<double> dist_x(-10.0, 10.0);
    std::uniform_real_distribution<double> dist_v(-10.0, 10.0);

    for (int i = 0; i < N; i++) {
        particles_rk4[i].x = particles_dp[i].x = dist_x(gen);
        particles_rk4[i].v = particles_dp[i].v = dist_v(gen);
    }

    std::ofstream fout_rk4("duffing_rk4.dat");
    std::ofstream fout_dp("duffing_dp.dat");
    std::ofstream fout_diff("diff.dat");
    if (!fout_rk4.is_open() || !fout_dp.is_open() || !fout_diff.is_open()) {
        std::cerr << "Ошибка открытия файлов!\n";
        return 1;
    }

    double t = 0.0;
    double max_global_diff_x = 0.0;
    double max_global_diff_v = 0.0;

    for (int i = 0; i < steps; i++) {
        double sum_diff_x = 0.0;  // Сумма разностей по x
        double sum_diff_v = 0.0;  // Сумма разностей по v
        double max_local_diff_x = 0.0;
        double max_local_diff_v = 0.0;

        for (int j = 0; j < N; j++) {
            fout_rk4 << particles_rk4[j].x << " " << particles_rk4[j].v << " ";
            fout_dp << particles_dp[j].x << " " << particles_dp[j].v << " ";

            double diff_x = std::abs(particles_rk4[j].x - particles_dp[j].x);
            double diff_v = std::abs(particles_rk4[j].v - particles_dp[j].v);
            sum_diff_x += diff_x;  // Накапливаем сумму разностей по x
            sum_diff_v += diff_v;  // Накапливаем сумму разностей по v

            max_local_diff_x = std::max(max_local_diff_x, diff_x);
            max_local_diff_v = std::max(max_local_diff_v, diff_v);
            max_global_diff_x = std::max(max_global_diff_x, diff_x);
            max_global_diff_v = std::max(max_global_diff_v, diff_v);
        }
        double avg_local_diff_x = sum_diff_x / N;  // Средняя локальная ошибка по x
        double avg_local_diff_v = sum_diff_v / N;  // Средняя локальная ошибка по v
        fout_diff << avg_local_diff_x << " " << avg_local_diff_v << "\n";

        fout_rk4 << "\n";
        fout_dp << "\n";

        for (int j = 0; j < N; j++) {
            rk_step(particles_rk4[j], t, dt, c_rk4, a_rk4, b_rk4, delta, alpha, beta, gamma, omega);
            rk_step(particles_dp[j], t, dt, c_dp, a_dp, b_dp, delta, alpha, beta, gamma, omega);
        }
        t += dt;
    }

    fout_rk4.close();
    fout_dp.close();
    fout_diff.close();

    std::cout << "Готово! Данные сохранены в 'duffing_rk4.dat', 'duffing_dp.dat' и 'diff.dat'.\n";
    std::cout << "Максимальная глобальная разница по x: " << max_global_diff_x << "\n";
    std::cout << "Максимальная глобальная разница по v: " << max_global_diff_v << "\n";

    return 0;
}