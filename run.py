#!/usr/bin/env python3

import os
import schort

if __name__ == '__main__':
  os.chdir(os.path.dirname(os.path.realpath(__file__)))
  schort.initDB()
  schort.app.run(host='0.0.0.0', port=8000)
