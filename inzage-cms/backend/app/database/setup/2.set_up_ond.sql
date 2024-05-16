-- add subjects in ond table
INSERT INTO "public"."ond" ("titel", "omschrijving", "sort_key", "user_nm") 
VALUES ('Belastingen', 'Bij dit onderwerp vindt u besluiten die gaan over belastingzaken. Bijvoorbeeld inkomstenbelasting, waterschapsheffingen en gemeentelijke heffingen.', '1', 'ICTU');
INSERT INTO "public"."ond" ("titel", "omschrijving", "sort_key", "user_nm") 
VALUES ('Familie', 'Bij dit onderwerp vindt u besluiten die gaan over familie en burgerlijke stand. Bijvoorbeeld huwelijk, ouderlijk gezag en pleegvergoeding.', '2', 'ICTU');
INSERT INTO "public"."ond" ("titel", "omschrijving", "sort_key", "user_nm") 
VALUES ('Gezondheid', 'Bij dit onderwerp vindt u besluiten die gaan over gezondheid en zorg. Bijvoorbeeld hulpverlening, WMO en Wlz en zorgverzekering.', '3', 'ICTU');
INSERT INTO "public"."ond" ("titel", "omschrijving", "sort_key", "user_nm") 
VALUES ('Identiteit', 'Bij dit onderwerp vindt u besluiten die gaan over persoonsregistratie. Bijvoorbeeld DigiD, naamswijziging en paspoorten.', '4', 'ICTU');
INSERT INTO "public"."ond" ("titel", "omschrijving", "sort_key", "user_nm") 
VALUES ('Inkomen', 'Bij dit onderwerp vindt u besluiten die gaan over uw inkomen. Bijvoorbeeld pensioenen, toeslagen en uitkeringen.', '5', 'ICTU');
INSERT INTO "public"."ond" ("titel", "omschrijving", "sort_key", "user_nm") 
VALUES ('Onderwijs', 'Bij dit onderwerp vindt u besluiten die gaan over onderwijs en inburgering. Bijvoorbeeld diploma’s, examens en studiefinanciering.', '6', 'ICTU');
INSERT INTO "public"."ond" ("titel", "omschrijving", "sort_key", "user_nm") 
VALUES ('Recht', 'Bij dit onderwerp vindt u besluiten die gaan over juridische zaken en burgerschap. Bijvoorbeeld rechtsbijstand, de stempas en meldingen van discriminatie.', '7', 'ICTU');
INSERT INTO "public"."ond" ("titel", "omschrijving", "sort_key", "user_nm") 
VALUES ('Schulden', 'Bij dit onderwerp vindt u besluiten die gaan over schulden. Bijvoorbeeld schuldhulpverlening, kwijtschelding en sanering.', '8', 'ICTU');
INSERT INTO "public"."ond" ("titel", "omschrijving", "sort_key", "user_nm") 
VALUES ('Vervoer', 'Bij dit onderwerp vindt u besluiten die gaan over mobiliteit en transport. Bijvoorbeeld een rijbewijs, verkeersboetes en voertuigregistraties.', '9', 'ICTU');
INSERT INTO "public"."ond" ("titel", "omschrijving", "sort_key", "user_nm") 
VALUES ('Werk', 'Bij dit onderwerp vindt u besluiten die gaan over werk en arbeid. Bijvoorbeeld contracten, ontwikkelsubsidies en Verklaring Omtrent het Gedrag (VOG).', '10', 'ICTU');
INSERT INTO "public"."ond" ("titel", "omschrijving", "sort_key", "user_nm") 
VALUES ('Wonen', 'Bij dit onderwerp vindt u besluiten die gaan over wonen en uw leefomgeving. Bijvoorbeeld bouwvergunningen, huursubsidie en WOZ-waarde.', '11', 'ICTU');

-- add links between subjects and event types
INSERT INTO "public"."evtp_ond" ("ond_cd", "evtp_cd", "user_nm") VALUES ('1','1','ICTU');
INSERT INTO "public"."evtp_ond" ("ond_cd", "evtp_cd", "user_nm") VALUES ('1','2','ICTU');
INSERT INTO "public"."evtp_ond" ("ond_cd", "evtp_cd", "user_nm") VALUES ('2','2','ICTU');
INSERT INTO "public"."evtp_ond" ("ond_cd", "evtp_cd", "user_nm") VALUES ('2','3','ICTU');
INSERT INTO "public"."evtp_ond" ("ond_cd", "evtp_cd", "user_nm") VALUES ('3','1','ICTU');
INSERT INTO "public"."evtp_ond" ("ond_cd", "evtp_cd", "user_nm") VALUES ('3','5','ICTU');
INSERT INTO "public"."evtp_ond" ("ond_cd", "evtp_cd", "user_nm") VALUES ('4','6','ICTU');
INSERT INTO "public"."evtp_ond" ("ond_cd", "evtp_cd", "user_nm") VALUES ('5','7','ICTU');
INSERT INTO "public"."evtp_ond" ("ond_cd", "evtp_cd", "user_nm") VALUES ('6','8','ICTU');
INSERT INTO "public"."evtp_ond" ("ond_cd", "evtp_cd", "user_nm") VALUES ('7','10','ICTU');
INSERT INTO "public"."evtp_ond" ("ond_cd", "evtp_cd", "user_nm") VALUES ('8','10','ICTU');
INSERT INTO "public"."evtp_ond" ("ond_cd", "evtp_cd", "user_nm") VALUES ('9','4','ICTU');
INSERT INTO "public"."evtp_ond" ("ond_cd", "evtp_cd", "user_nm") VALUES ('10','4','ICTU');
INSERT INTO "public"."evtp_ond" ("ond_cd", "evtp_cd", "user_nm") VALUES ('10','9','ICTU');