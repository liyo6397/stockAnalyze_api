def LPPLS(data):

    # convert index col to evenly spaced numbers over a specified interval
    time = np.linspace(0, len(data) - 1, len(data))

    price = np.log(data)

    # create Mx2 matrix (expected format for LPPLS observations)
    training_data = np.array([time, price])

    # set the max number for searches to perform before giving-up
    # the literature suggests 25
    MAX_SEARCHES = 25

    # instantiate a new LPPLS model with the S&P 500 dataset
    lppls_model = lppls.LPPLS(observations=training_data)

    # fit the model to the data and get back the params
    tc, m, w, a, b, c, c1, c2 = lppls_model.fit(training_data, MAX_SEARCHES, minimizer='Nelder-Mead')

    print(f"tc: {tc}, m: {m}, w: {w}, a: {a}")
    print(f"b: {b}, c: {c}, c1: {c1}, c2: {c2}")

    confidence_indicator(lppls_model)

def confidence_indicator(lppls_model):
    # define custom filter condition
    filter_conditions_config = [
        {'condition_1': [
            (0.0, 0.1),  # tc_range
            (0, 1),  # m_range
            (4, 25),  # w_range
            2.5,  # O_min
            0.5,  # D_min
        ]},
    ]

    # compute the confidence indicator
    res = lppls_model.mp_compute_indicator(
        workers=4,
        window_size=120,
        smallest_window_size=30,
        increment=5,
        max_searches=25,
        filter_conditions_config=filter_conditions_config
    )
    res_df = lppls_model.res_to_df(res, 'condition_1')
    lppls_model.plot_confidence_indicators(res_df, title='Short Term Indicator 120-30')

    plt.show()

