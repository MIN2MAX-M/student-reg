-- Enable case-insensitive text for email uniqueness
CREATE EXTENSION IF NOT EXISTS citext;

CREATE TABLE IF NOT EXISTS students (
  id BIGSERIAL PRIMARY KEY,

  first_name VARCHAR(80)  NOT NULL,
  last_name  VARCHAR(80)  NOT NULL,

  -- Case-insensitive uniqueness (EMMY@x == emmy@x)
  email CITEXT NOT NULL UNIQUE,

  phone   VARCHAR(32),
  age     INTEGER CHECK (age IS NULL OR (age >= 0 AND age <= 150)),
  address VARCHAR(255),

  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Helpful for alphabetical directory views
CREATE INDEX IF NOT EXISTS ix_students_name ON students (last_name, first_name);

-- Optional: fast lookups by email (UNIQUE already creates an index implicitly)
-- CREATE INDEX IF NOT EXISTS ix_students_email ON students (email);
