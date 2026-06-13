insert into public.bestellung 
select bs.bestell_id, bs.kundenadress_id, bs.bestelldatum from staging.bestellung_staging bs; 

insert into public.bestellposition (bestell_id, produkt, preis) 
select bps.bestell_id, bps.produkt, bps.preis from staging.bestellpositionen_staging bps;