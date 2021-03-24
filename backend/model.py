import numpy as np
from hmmlearn.hmm import GaussianHMM


def train_hmm_model(data, num_states):
    model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000)
    model.fit(data)

    return model




def next_hidden_states(model, data):



    post_prob = model.predict_proba(data)
    trans = model.transmat_

    next_state_prob = np.dot(post_prob[-1], trans)

    return next_state_prob, np.argmax(next_state_prob)

def Euler_Maruyama(last_v, last_return, mu, sigma, seed=5, N=2**6, M=1):
    dt = M * (1 / N)  # EM step size
    L = N / M
    wi = np.zeros(int(L))
    wi[0] = last_return
    np.random.seed(seed)

    for i in range(1, int(L)):
        dw = np.random.normal(loc=0.0, scale=np.sqrt(dt))
        # dw = np.sum(b[(M*(i-1)+M):(M*i + M)])
        wi[i] = wi[i - 1] + mu * wi[i - 1] * dt + sigma * wi[i - 1] * dw

    prices = np.zeros_like(wi)
    prices[0] = last_v
    for i in range(1, len(wi)):
        prices[i] = last_v + last_v * wi[i]

    return prices