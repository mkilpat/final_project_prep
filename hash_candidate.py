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
Given a list of candidates on stdin, produce a file of hashes ("map file").
"""


import rappor
import pandas as pd


def HashCandidates(params, vals, out):
    num_bloombits = params.num_bloombits
    hashed = {}

    for line in vals:
        word = line.strip()
        bits = []
        for cohort in range(params.num_cohorts):
            bloom_bits = rappor.get_bloom_bits(word, cohort, params.num_hashes, num_bloombits)

            for bit_to_set in bloom_bits:
                bits.append(cohort * num_bloombits + (bit_to_set + 1))

        hashed[word] = bits

    hashed = pd.DataFrame.from_dict(hashed, orient='index')
    hashed.to_csv(out)


def main():
    params = rappor.Params()
    params.num_bloombits = 16
    params.num_hashes = 2
    params.num_cohorts = 64
    params.prob_p = 0.5
    params.prob_q = 0.75
    params.prob_f = 0.5

    vals = list(map(lambda x: 'v'+str(x), range(60)))
    out = '/Users/Michael/PycharmProjects/untitled1/data/hashed.csv'

    HashCandidates(params, vals, out)


if __name__ == '__main__':
    main()
