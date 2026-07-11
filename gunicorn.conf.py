accesslog = "-"
errorlog = "-"
capture_output = True
access_log_format = (
    '%(t)s %(p)s INFO gunicorn.access method="%(m)s" path="%(U)s" '
    "status=%(s)s bytes=%(B)s duration_us=%(D)s"
)
