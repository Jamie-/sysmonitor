-- Proposed database schema used for reference during implementation.

CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    reset_password INTEGER,  -- Force password reset on next login
    date_added TEXT,
    security_token TEXT,  -- Reset password token
    token_expiry TEXT  -- Reset password token expiry
);

CREATE TABLE IF NOT EXISTS services(
    slug TEXT PRIMARY KEY,
    address TEXT NOT NULL,
    test_type TEXT NOT NULL,  -- e.g. ping test, get URL, connect to socket, etc
    test_data TEXT,  -- Data to send to target, dependant on test type, or number of pings, etc
    expected_status TEXT,  -- Expected status for test that support it
    expected_response TEXT,  -- Expected response
    repeat_interval INTEGER,  -- Time in seconds between checking target
    cooloff_interval INTEGER,  -- Time in seconds to wait before retry if failed (up to max_tries)
    max_tries INTEGER,  -- Number of times to try again before declaring resource dead/down
    group TEXT references groups(slug),
    call_webhook TEXT,  -- When to call webhook, e.g. always/on failure/on success
    webhook TEXT REFERENCES webhooks(slug),  -- If has webhook trigger,
    date_added TEXT,
    added_by TEXT REFERENCES users(username)
);

CREATE TABLE IF NOT EXISTS groups(
    slug TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    icon TEXT,
    color TEXT,
    date_added TEXT,
    added_by TEXT REFERENCES users(username),
    date_modified TEXT,
    modified_by TEXT REFERENCES users(username)
);

CREATE TABLE IF NOT EXISTS results(
    resource_slug TEXT REFERENCES services(slug),
    timestamp TEXT NOT NULL,
    result TEXT NOT NULL,
    duration INTEGER,  -- Time in seconds to perform test/check
    attempts INTEGER,  -- Number of repeat attempts before response/give up
    PRIMARY KEY (resource_slug, timestamp)
);

CREATE TABLE IF NOT EXISTS webhooks(
    slug TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    verify INT,  -- (boolean) Whether or not to verify the call is encrypted
    date_added TEXT NOT NULL,
    added_by TEXT REFERENCES users(username)
);

CREATE TABLE IF NOT EXISTS webhook_history(
    webhook_slug TEXT REFERENCES webhooks(slug),
    timestamp TEXT NOT NULL,
    request TEXT,  -- HTTP request sent
    response_code INTEGER,  -- Response code returned
    response TEXT,  -- HTTP response received
    PRIMARY KEY (webhook_slug, timestamp)
);

CREATE TABLE IF NOT EXISTS api_tokens(
    token TEXT PRIMARY KEY,
    username TEXT REFERENCES users(username),
    date_added TEXT,  -- Date token added
    last_used TEXT,  -- Date token last used
    revoked INTEGER
);

CREATE TABLE IF NOT EXISTS settings(
    key TEXT PRIMARY KEY,
    value TEXT,
    last_modified TEXT,  -- Datetime setting last modified
    modified_by TEXT REFERENCES users(username)
);
