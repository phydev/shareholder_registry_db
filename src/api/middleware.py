
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://127.0.0.1",
]

CORS = {'middleware_class' : CORSMiddleware,
'allow_origins' : origins,
'allow_origin_regex' : r"http://(localhost|127\.0\.0\.1)(:\d+)?",
'allow_credentials' : True,
'allow_methods' : ["*"],
'allow_headers' : ["*"]}

