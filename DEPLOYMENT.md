# Deployment op Vercel

Repository: https://github.com/robbeckers/airtechnology

1. Importeer deze repository als nieuw project in Vercel.
2. Gebruik productiebranch `main`, Root Directory `./` en Framework Preset `Other`.
3. `vercel.json` stelt Build Command `npm run build` en Output Directory `dist` in.
4. Voeg de onderstaande omgevingsvariabelen toe voor het contactformulier.
5. Deploy en controleer de homepage, een productpagina en het contactformulier.

## Contactformulier

`api/contact.py` gebruikt de bestaande validatie en SMTP-verzending uit
`src/contact_delivery.py`. De site en het endpoint draaien op hetzelfde domein.
Er zijn geen extra Python- of Node-packages nodig.

Verplicht voor verzending:

- `AIRTECHNIC_SMTP_HOST`
- `AIRTECHNIC_SMTP_USERNAME`
- `AIRTECHNIC_SMTP_PASSWORD`

Optioneel:

- `AIRTECHNIC_SMTP_FROM`: geautoriseerde afzender; standaard de gebruikersnaam.
- `AIRTECHNIC_SMTP_SECURITY`: `smtps` (standaard) of `starttls`.
- `AIRTECHNIC_SMTP_PORT`: standaard `465` voor SMTPS, `587` voor STARTTLS.

Vul de waarden uitsluitend in Vercel Environment Variables in en deploy daarna
opnieuw. Zonder deze instellingen geeft het formulier een foutmelding en geen
onterechte verzendbevestiging. Controleer na configuratie een herkenbaar testbericht
in `info@airtechnicsolutions.com`.

De bestaande limiet geldt per functie-instantie. Stel voor een gedeelde limiet
een Vercel Firewall-regel voor `POST /api/contact` in.

## Wijzigingen publiceren

Pas de bronbestanden aan en genereer de pagina's lokaal met:

```powershell
python src/build.py
npm run build
```

Commit de bronbestanden én gegenereerde HTML en push naar `main`.
Na het koppelen van Vercel worden nieuwe commits automatisch gedeployd.
De Vercel-build kopieert de ingecheckte HTML en websitebestanden naar `dist/`;
Python-bronnen, documentatie en reviewbestanden worden niet statisch gepubliceerd.
`dist/`, `.vercel/`, Python-cache en lokale geheimen blijven buiten Git.

De bestaande `.html`-adressen blijven behouden. Conceptpagina's uit de lokale
website blijven eveneens beschikbaar. Dit is een voorbereiding voor deployment;
de Vercel-projectkoppeling en mailboxcontrole worden bij de daadwerkelijke
deployment uitgevoerd.
