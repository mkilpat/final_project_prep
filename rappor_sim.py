import pandas as pd
import rappor


def RapporClientSim(params, irr_rand, csv_in):
    """Read true values from csv_in and output encoded values on csv_out."""
    header = ['client', 'cohort', 'bloom', 'prr', 'irr']
    out_rows = {}

    # TODO: It would be more instructive/efficient to construct an encoder
    # instance up front per client, rather than one per row below.

    for i, (index, client_str, cohort_str, true_value) in csv_in.iterrows():


        cohort = int(cohort_str)
        secret = client_str
        e = rappor.Encoder(params, cohort, secret, irr_rand)

        # Real users should call e.encode().  For testing purposes, we also want
        # the PRR.
        bloom, prr, irr = e._internal_encode(true_value)

        bloom_str = rappor.bit_string(bloom, params.num_bloombits)
        prr_str = rappor.bit_string(prr, params.num_bloombits)
        irr_str = rappor.bit_string(irr, params.num_bloombits)

        out_rows[i] = [client_str, cohort_str, bloom_str, prr_str, irr_str]

    output = pd.DataFrame.from_dict(out_rows, orient='index')
    output.columns = header
    output.to_csv('/Users/Michael/PycharmProjects/untitled1/data/output.csv')


def main():
    params = rappor.Params()
    params.num_bloombits = 16
    params.num_hashes = 2
    params.num_cohorts = 64
    params.prob_p = 0.5
    params.prob_q = 0.75
    params.prob_f = 0.5

    irr_rand = rappor.SecureIrrRand(params)
    csv_in = pd.read_csv('/Users/Michael/PycharmProjects/untitled1/data/input.csv')
    RapporClientSim(params, irr_rand, csv_in)


if __name__ == "__main__":
    main()