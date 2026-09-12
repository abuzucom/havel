CREATE TABLE profiles (
    id           uuid PRIMARY KEY,
    email        text NOT NULL,
    date_of_birth date,
    mothers_maiden_name text,
    home_address text,
    referral_source text
);
