#!/usr/bin/env python
"""
Simple script to parse dbench results 
and reformat them as JSON for sending back to juju
"""
import sys
import subprocess
import re
from charmbenchmark import Benchmark


def parse_dbench_output():
    output = '\n'.join(sys.stdin.readlines())
    results = {}
    key_values = re.split(r'[\n\r]+', output)
    for pairs in key_values:
        key, value = pairs.partition("{perf}=")[::2]
        if key:
           results[key] = value

    for key in results:
        Benchmark.set_data({"results.%s" % key: results[key]})
#       print({"results.%s" % key: results[key]})

    Benchmark.set_composite_score(results['throughput'],'throughput')

if __name__ == "__main__":
    parse_dbench_output()
