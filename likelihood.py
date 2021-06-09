import math
from scipy import stats


def get_omega(g, count):
    omega = [0.0 for a in range(count)]
    for node in g.nodes():
        omega[int(g.nodes[node]['attr'])] += 1.0
    for i in range(len(omega)):
        omega[i] /= len(g.nodes)
    return omega


def check_likelihood(g, count, omega, likelihood):
    m = [0.0 for a in range(count)]
    for node in g.nodes():
        m[int(g.nodes[node]['attr'])] += 1.0

    tau = 0.0
    for i in range(len(omega)):
        if omega[i] == 0 or m[i] == 0:
            continue
        tau += 2 * m[i] * math.log(m[i] / (len(g.nodes) * omega[i]))

    return math.fabs(tau) <= stats.chi2.ppf(q=1 - likelihood, df=count)


def check_likelihood2(g, k, omega, alpha):
    m = [0.0] * k
    for node in g.nodes():
        m[int(g.nodes[node]['weight'])] += 1.0

    tau = 0.0
    for i in range(len(omega)):
        if omega[i] == 0 or m[i] == 0:
            continue
        tau += 2 * m[i] * math.log(m[i] / (g.number_of_nodes() * omega[i]))

    distribution = stats.chi2.ppf(q=alpha, df=k-1)
    return math.fabs(tau) <= distribution
