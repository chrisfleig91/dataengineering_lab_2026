INSERT INTO kunde (
    SELECT ks.kunden_id, ks.name, ks.email, ks.registrierungsdatum, ks.kunden_status, ks.neukunde
    FROM staging.kunde_staging ks
      LEFT JOIN public.kunde k ON k.kunden_id = ks.kunden_id
    WHERE k.kunden_id IS NULL
  );