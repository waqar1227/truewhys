# Kaggle CLI wrapper: token is injected by the network proxy, so skip local token introspection.
import os, sys
os.environ["KAGGLE_API_TOKEN"] = "KGAT_proxy_injected_placeholder"
from kaggle.api import kaggle_api_extended as k
k.KaggleApi._introspect_token = lambda self, t: os.environ.get("KAGGLE_USERNAME","anam318")
from kaggle.cli import main
sys.exit(main())
