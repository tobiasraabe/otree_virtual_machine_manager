# -*- coding: utf-8 -*-

import os

os.environ['OVMM_PSQL_CONN'] = (
    "{'dbname': 'postgres', 'user': 'postgres', 'host': 'localhost'}")
os.environ['OVMM_PSQL_TABLE'] = 'user_table'
os.environ['OVMM_DAPHNE_RANGE'] = str([i for i in range(8001, 8021)])
os.environ['OVMM_HTTP_RANGE'] = str([i for i in range(7901, 7921)])
os.environ['OVMM_SSL_RANGE'] = str([i for i in range(7801, 7821)])
os.environ['OVMM_REDIS_RANGE'] = str([i for i in range(1, 21)])

os.environ['OVMM_PASSWORD_LENGTH'] = '8'
