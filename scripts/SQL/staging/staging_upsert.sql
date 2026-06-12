INSERT INTO public.kunde (kunden_id, name, email, registrierungsdatum, kunden_status, neukunde)
SELECT ks.kunden_id, ks.name, ks.email, ks.registrierungsdatum, ks.kunden_status, ks.neukunde
FROM staging.kunde_staging ks
ON CONFLICT (kunden_id) 
DO UPDATE SET 
    name = EXCLUDED.name,
    email = EXCLUDED.email,
    registrierungsdatum = EXCLUDED.registrierungsdatum,
    kunden_status = EXCLUDED.kunden_status,
    neukunde = EXCLUDED.neukunde;