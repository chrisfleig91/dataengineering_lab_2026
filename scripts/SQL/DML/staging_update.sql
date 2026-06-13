UPDATE public.kunde AS k
SET k.name = ks.name,
  k.email = ks.email,
  k.registrierungsdatum = ks.registrierungsdatum,
  k.kunden_status = ks.kunden_status,
  k.neukunde = ks.neukunde
FROM staging.kunde_staging ks
WHERE k.kunden_id = ks.kunden_id
  AND (
    k.name != ks.name
    OR k.email != ks.email
    OR k.registrierungsdatum != ks.registrierungsdatum
    OR k.kunden_status != ks.kunden_status
    OR k.neukunde != ks.neukunde
  )