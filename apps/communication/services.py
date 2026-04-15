import requests
import hashlib
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def _hash_email(email: str) -> str:
    return hashlib.md5(email.lower().strip().encode()).hexdigest()


def subscribe_to_mailchimp(email: str, whatsapp: str = None) -> dict:
    api_key = settings.MAILCHIMP_API_KEY
    list_id = settings.MAILCHIMP_LIST_ID
    server = settings.MAILCHIMP_SERVER_PREFIX

    url = (
        f"https://{server}.api.mailchimp.com/3.0"
        f"/lists/{list_id}/members/{_hash_email(email)}"
    )
    payload = {
        "email_address": email,
        "status_if_new": "subscribed",
        "status": "subscribed",
        "merge_fields": {}
    }
    if whatsapp:
        payload["merge_fields"]["WHATSAPP"] = whatsapp

    try:
        response = requests.put(
            url, json=payload,
            auth=("anystring", api_key),
            timeout=10
        )
        if response.status_code in [200, 201]:
            logger.info(f"[Mailchimp] ✅ Abonné : {email}")
            return {"success": True}
        else:
            error = response.json().get("detail", "Erreur inconnue")
            logger.error(f"[Mailchimp] ❌ {response.status_code} : {error}")
            return {"success": False, "error": error}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Timeout Mailchimp"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Connexion impossible"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_and_send_campaign(
    subject: str,
    html_content: str,
    preview_text: str = "",
    test_email: str = None
) -> dict:

    api_key = settings.MAILCHIMP_API_KEY
    list_id = settings.MAILCHIMP_LIST_ID
    server = settings.MAILCHIMP_SERVER_PREFIX
    reply_to = getattr(settings, "MAILCHIMP_REPLY_TO", "contact@ndiarama.com")

    base_url = f"https://{server}.api.mailchimp.com/3.0"
    auth = ("anystring", api_key)

    # ── ÉTAPE 1 : Créer la campagne ──────────────────────────────
    campaign_res = requests.post(
        f"{base_url}/campaigns",
        json={
            "type": "regular",
            "recipients": {"list_id": list_id},
            "settings": {
                "subject_line": subject,
                "preview_text": preview_text,
                "from_name": "NDIARAMA",
                "reply_to": reply_to,
            },
        },
        auth=auth,
        timeout=15,
    )

    if campaign_res.status_code != 200:
        error = campaign_res.json()
        logger.error(f"[Mailchimp] ❌ Création : {error}")
        return {
            "success": False,
            "step": "creation",
            "error": error.get("detail", str(error))
        }

    campaign_id = campaign_res.json()["id"]
    logger.info(f"[Mailchimp] ✅ Campagne créée : {campaign_id}")

    # ── ÉTAPE 2 : Ajouter le contenu ─────────────────────────────
    content_res = requests.put(
        f"{base_url}/campaigns/{campaign_id}/content",
        json={"html": _build_html_email(html_content)},
        auth=auth,
        timeout=15,
    )

    if content_res.status_code != 200:
        error = content_res.json()
        logger.error(f"[Mailchimp] ❌ Contenu : {error}")
        return {
            "success": False,
            "step": "content",
            "error": error.get("detail", str(error))
        }

    logger.info(f"[Mailchimp] ✅ Contenu ajouté")

    # ── MODE TEST ─────────────────────────────────────────────────
    if test_email:
        test_res = requests.post(
            f"{base_url}/campaigns/{campaign_id}/actions/test",
            json={
                "test_emails": [test_email],
                "send_type": "html"
            },
            auth=auth,
            timeout=15,
        )
        if test_res.status_code == 204:
            logger.info(f"[Mailchimp] ✅ Test envoyé à {test_email}")
            return {
                "success": True,
                "mode": "test",
                "campaign_id": campaign_id,
                "message": f"Email de test envoyé à {test_email}"
            }
        else:
            error = test_res.json()
            return {
                "success": False,
                "step": "test_send",
                "error": error.get("detail", str(error))
            }

    # ── ENVOI RÉEL ────────────────────────────────────────────────
    send_res = requests.post(
        f"{base_url}/campaigns/{campaign_id}/actions/send",
        auth=auth,
        timeout=15,
    )

    if send_res.status_code == 204:
        logger.info(f"[Mailchimp] ✅ Campagne envoyée : {campaign_id}")
        return {
            "success": True,
            "mode": "send",
            "campaign_id": campaign_id,
            "message": "Campagne envoyee a tous les abonnes."
        }
    else:
        error = send_res.json()
        logger.error(f"[Mailchimp] ❌ Envoi : {error}")
        return {
            "success": False,
            "step": "send",
            "error": error.get("detail", str(error))
        }


def _build_html_email(content: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>Newsletter NDIARAMA</title>
</head>
<body style="margin:0;padding:0;background:#f8f4ef;font-family:Georgia,serif;">
  <table width="100%" cellpadding="0" cellspacing="0"
         style="background:#f8f4ef;padding:40px 20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0"
               style="background:#ffffff;border-radius:16px;overflow:hidden;
                      box-shadow:0 4px 24px rgba(120,78,52,0.10);">
          <!-- HEADER -->
          <tr>
            <td style="background:#c69470;padding:28px 40px;text-align:center;">
              <p style="margin:0;font-size:11px;letter-spacing:0.25em;
                         color:rgba(255,255,255,0.8);text-transform:uppercase;">
                Studio Media et Consulting
              </p>
              <h1 style="margin:8px 0 0;font-size:26px;font-weight:600;color:#ffffff;">
                NDIARAMA
              </h1>
            </td>
          </tr>
          <!-- CONTENU -->
          <tr>
            <td style="padding:40px;color:#444444;font-size:15px;line-height:1.8;">
              {content}
            </td>
          </tr>
          <!-- FOOTER -->
          <tr>
            <td style="background:#2b211d;padding:24px 40px;text-align:center;">
              <p style="margin:0 0 8px;font-size:11px;color:rgba(255,255,255,0.5);
                         text-transform:uppercase;letter-spacing:0.15em;">
                NDIARAMA Media et Consulting — Bamako, Mali
              </p>
              <p style="margin:0;font-size:11px;color:rgba(255,255,255,0.4);">
                *|UNSUB|* &middot; *|UPDATE_PROFILE|*
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""