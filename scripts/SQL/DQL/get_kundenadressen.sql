SELECT k.kunden_id,
  name,
  a.plz,
  a.stadt,
  a.strasse,
  a.hausnummer,
  a.adress_id
FROM public.kunde k
  INNER JOIN public.kundenadresse ka ON ka.kunden_id = k.kunden_id
  INNER JOIN public.adresse a ON a.adress_id = ka.adress_id;