create or replace function slugen(input text)
returns text as $$
  -- Remove accents and other diacritic/non-ascii characters
  with "unaccented" as (
    select unaccent(input) as value
  ),
  -- Lowercase the string
  "lowercase" as (
    select lower(value) as value
    from "unaccented"
  ),
  -- Replace everything that is not a letter or digit by hyphens
  "hyphenated" as (
    select regexp_replace(value, '[^a-z0-9]', '-', 'g') as value
    from "lowercase"
  ),
  -- Trim leading, trailing, and consecutive hyphens
  "trimmed" as (
    select trim(both '-' from regexp_replace(value, '-+', '-', 'g')) as value
    from "hyphenated"
  )
  select coalesce(value, '') from "trimmed";
$$ language sql immutable;
