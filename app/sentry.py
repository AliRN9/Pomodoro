import sentry_sdk

sentry_sdk.init(
    dsn="https://07d03d9b11da33e3faf853e57566613c@o4509357555515392.ingest.de.sentry.io/4509357791838288",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)
