from flask_restx.reqparse import RequestParser

page_parser: RequestParser = RequestParser()
page_parser.add_argument(name='page', type=int, location='args', required=False)

status_page_parser: RequestParser = RequestParser()
status_page_parser.add_argument(name='page', type=int, location='args', required=False)
status_page_parser.add_argument(name='status', type=int, location='args', required=False)
