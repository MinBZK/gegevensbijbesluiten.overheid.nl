-- This script is used to set the koepel column in the gg table to true or false based on the following conditions:
UPDATE gg
SET koepel = true
WHERE gg_cd in (
    SELECT DISTINCT ggs.gg_cd_sup
    FROM evtp_version ev
    JOIN evtp_gst eg ON ev.evtp_cd = eg.evtp_cd
    JOIN gst_gg gg ON gg.gst_cd = eg.gst_cd
    JOIN gg_struct ggs ON ggs.gg_cd_sub = gg.gg_cd
    WHERE ev.id_publicatiestatus IN (2, 3)
);

UPDATE gg
SET koepel = false
WHERE gg_cd not in (
    SELECT DISTINCT ggs.gg_cd_sup
    FROM evtp_version ev
    JOIN evtp_gst eg ON ev.evtp_cd = eg.evtp_cd
    JOIN gst_gg gg ON gg.gst_cd = eg.gst_cd
    JOIN gg_struct ggs ON ggs.gg_cd_sub = gg.gg_cd
    WHERE ev.id_publicatiestatus IN (2, 3)
);

-- This script is used to set the omschrijving_uitgebreid column in the gg table to the correct values based on the gg_cd column:
UPDATE gg
SET omschrijving_uitgebreid = 
    CASE 
        WHEN omschrijving = 'Vervoersgegevens' THEN 'Alle verzekeringsgegevens met betrekking tot de Wet langdurige zorg (Wlz) en andere verzekeringen die gericht zijn op bijvoorbeeld zorg en wonen.'
        WHEN omschrijving = 'Persoonsgegevens' THEN 'Alle gegevens over beroep en functie, inclusief BIG- en AGB-geregistreerde zorgverleners.'
        WHEN omschrijving = 'Werk en Inkomensgegevens' THEN 'Alle adres- en gebouwgegevens. Van adres, type woning tot woonoppervlakte.'
        WHEN omschrijving = 'Inkomens- en vermogensgegevens' THEN 'Een signalering als bijstand en WW samenlopen of andere meldingen worden hier getoond.'
        WHEN omschrijving = 'Belastinggegevens' THEN 'Van soort rechtsbijstand tot een check op andere woon- of verblijfadressen dan bij UWV bekend zijn. Zaakgegevens bestaan uit informatie en documenten die betrekking hebben op een specifieke zaak of kwestie.'
        WHEN omschrijving = 'Kadastrale gegevens' THEN 'Van type onderneming tot factuuradres. Hier vindt u al uw bedrijfsgegevens.'
        WHEN omschrijving = 'Adres- en gebouwgegevens' THEN 'Van aangifte inkomstenbelasting tot aanvragen voorlopige aanslagen. Alle gegevens over belastingen vindt u hier.'
        WHEN omschrijving = 'Milieugegevens' THEN 'Alle gegevens over uw opleidingen en cursussen. Van diploma tot studieschuld.'
        WHEN omschrijving = 'Justitiële gegevens' THEN 'Van schulden, alimentatieregelingen tot recht op kinderbijslag. Hier vindt u al uw financiële gegevens.'
        WHEN omschrijving = 'Zorggegevens' THEN 'Alle gegevens over huur van een woning of andere objecten.'
        WHEN omschrijving = 'WOZ-gegevens' THEN 'Van een verkeersovertreding tot een strafblad. Justitiële gegevens hebben betrekking op strafrechtelijke zaken en veroordelingen.'
        WHEN omschrijving = '(Voor)opleidingsgegevens' THEN 'Informatie over eigendom, grootte en grenzen van grondpercelen.'
        WHEN omschrijving = '(Bron)documentgegevens' THEN 'Van water- en energieverbruik tot diverse soorten afval. Hier vindt u gegevens over verschillende milieuzaken.'
        WHEN omschrijving = 'Signaleringen' THEN 'Gegevens over de betalingsregeling voor zorgtoeslag.'
        WHEN omschrijving = 'Verzekeringsgegevens' THEN 'Van verblijfsdocument tot vreemdelingennummer. Hier vindt u gegevens voor vluchtelingen, statushouders en migranten.'
        WHEN omschrijving = 'Financiële- en verzekeringsgegevens' THEN 'Gegevens over strafbaar gedrag en opsporingsonderzoek.'
        WHEN omschrijving = 'Politiegegevens' THEN 'Al uw persoonlijke gegevens, zoals naam, adres en geboortedatum, maar ook vingerafdrukken en burgerservicenummer.'
        ELSE omschrijving_uitgebreid
    END;

-- Insert the omschrijving column in the oe_com_type table and link to the evtp table
INSERT INTO "public"."oe_com_type" ("omschrijving") VALUES ('Per mail en download in MijnOverheid.');
INSERT INTO "public"."oe_com_type" ("omschrijving") VALUES ('Via de post of e-mail');
INSERT INTO "public"."oe_com_type" ("omschrijving") VALUES ('Via de DigiD app');
INSERT INTO "public"."oe_com_type" ("omschrijving") VALUES ('VIa e-mail of via het online portaal');

INSERT INTO "public"."evtp_oe_com_type" ("evtp_cd", "oe_com_type_cd") VALUES ('2','1');
INSERT INTO "public"."evtp_oe_com_type" ("evtp_cd", "oe_com_type_cd") VALUES ('2','2');
INSERT INTO "public"."evtp_oe_com_type" ("evtp_cd", "oe_com_type_cd", "link") VALUES ('2','3','https://test.nl');
INSERT INTO "public"."evtp_oe_com_type" ("evtp_cd", "link", "oe_com_type_cd") VALUES ('1','https://test.again.nl','2');
INSERT INTO "public"."evtp_oe_com_type" ("evtp_cd", "oe_com_type_cd") VALUES ('1','3');

INSERT INTO "public"."bestand_acc" ("volg_nr", "omschrijving", "bestand_verwijzing", "ts_create", "user_nm") VALUES ('1','','','2024-05-13 09:06:04.084212','');
INSERT INTO "public"."evtp_acc" ("evtp_cd", "oe_cd", "ts_acc", "notitie", "volg_nr", "bestand_acc_cd") VALUES ('8','5','2024-05-13 09:06:04.097208','Goedgekeurd door gemeente afdeling burgerzaken','1','1');
INSERT INTO "public"."bestand_acc" ("volg_nr", "omschrijving", "bestand_verwijzing", "ts_create", "user_nm") VALUES ('2','','','2024-05-13 09:06:04.084212','');
INSERT INTO "public"."evtp_acc" ("evtp_cd", "oe_cd", "ts_acc", "notitie", "volg_nr", "bestand_acc_cd") VALUES ('9','4','2024-05-13 09:06:04.097208','Goedgekeurd door RDW','1','1');

-- Inserting extra rge into existing gst
INSERT INTO "public"."gst_rge" ("gst_cd", "rge_cd", "sort_key") VALUES ('36','3','2');
INSERT INTO "public"."gst_rge" ("gst_cd", "rge_cd", "sort_key") VALUES ('4','4', '1');
INSERT INTO "public"."gst_rge" ("gst_cd", "rge_cd", "sort_key") VALUES ('33','4', '1');

-- Inserting sort_key specific for evtp based on gg-koepel
INSERT INTO "public"."gg_evtp_sort" ("gg_cd", "evtp_cd", "sort_key") VALUES ('86','2','1');
INSERT INTO "public"."gg_evtp_sort" ("gg_cd", "evtp_cd", "sort_key") VALUES ('7','2','100');
