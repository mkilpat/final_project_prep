#!/usr/bin/python
#
# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Read the RAPPOR'd values on stdin, and sum the bits to produce a Counting Bloom
filter by cohort.  This can then be analyzed by R.
"""

import rappor
import pandas as pd


def SumBits(params, csv_in):

    num_cohorts = params.num_cohorts
    num_bloombits = params.num_bloombits
    counts = {}

    sums = [[0] * num_bloombits for _ in range(num_cohorts)]
    num_reports = [0] * num_cohorts

    for i, row in csv_in.iterrows():
        try:
            (index, user_id, cohort, unused_bloom, unused_prr, irr) = row
        except ValueError:
            raise RuntimeError('Error parsing row %r' % row)

        if i == 0:
            continue  # skip header

        cohort = int(cohort)
        num_reports[cohort] += 1

        if not len(irr) == params.num_bloombits:
            raise RuntimeError(
              "Expected %d bits, got %r" % (params.num_bloombits, len(irr)))
        for i, c in enumerate(str(irr)):
            bit_num = num_bloombits - i - 1  # e.g. char 0 = bit 15, char 15 = bit 0
            if c == '1':
                sums[cohort][bit_num] += 1
            else:
                if c != '0':
                    raise RuntimeError('Invalid IRR -- digits should be 0 or 1')

    for cohort in range(num_cohorts):
        # First column is the total number of reports in the cohort.
        row = [num_reports[cohort]] + sums[cohort]
        counts[cohort] = row

    counts = pd.DataFrame.from_dict(counts, orient='index')
    counts.to_csv('/Users/Michael/PycharmProjects/untitled1/data/counts.csv')



def main():
    params = rappor.Params()
    params.num_bloombits = 16
    params.num_hashes = 2
    params.num_cohorts = 64
    params.prob_p = 0.5
    params.prob_q = 0.75
    params.prob_f = 0.5

    csv_in = pd.read_csv('/Users/Michael/PycharmProjects/untitled1/data/output.csv',
                         dtype={'bloom': object, 'prr': object, 'irr': object})

    SumBits(params, csv_in)


if __name__ == '__main__':
    main()
