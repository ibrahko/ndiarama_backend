# communication/services.py

import requests
import hashlib
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def _hash_email(email: str) -> str:
    """
    Mailchimp identifie chaque contact par le MD5 de son email en minuscule.
    Obligatoire pour l'endpoint PUT /members/{subscriber_hash}
    """
    return hashlib.md5(email.lower().strip().encode()).hexdigest()


def subscribe_to_mailchimp(email: str, whatsapp: str = None) -> dict:
    """
    Ajoute ou met à jour un contact dans Mailchimp.
    
    On utilise PUT au lieu de POST pour deux raisons :
    - PUT = upsert (crée si inexistant, met à jour si existant)
    - POST échoue si l'email existe déjà → erreur 400
    """
    api_key = settings.MAILCHIMP_API_KEY
    list_id = settings.MAILCHIMP_LIST_ID
    server = settings.MAILCHIMP_SERVER_PREFIX  # ex: "us21"

    # URL de l'endpoint Mailchimp
    url = (
        f"https://{server}.api.mailchimp.com/3.0"
        f"/lists/{list_id}/members/{_hash_email(email)}"
    )

    # Payload envoyé à Mailchimp
    payload = {
        "email_address": email,
        "status_if_new": "subscribed",   # statut si nouveau contact
        "status": "subscribed",           # statut si contact existant
        "merge_fields": {}
    }

    # Ajouter WhatsApp si fourni
    # ⚠️ "WHATSAPP" doit correspondre au nom du champ custom dans Mailchimp
    if whatsapp:
        payload["merge_fields"]["WHATSAPP"] = whatsapp

    try:
        response = requests.put(
            url,
            json=payload,
            auth=("anystring", api_key),  # user peut être n'importe quoi
            timeout=10
        )

        response_data = response.json()

        # Succès : 200 (mis à jour) ou 201 (créé)
        if response.status_code in [200, 201]:
            logger.info(f"[Mailchimp] ✅ Abonné ajouté : {email}")
            return {
                "success": True,
                "mailchimp_id": response_data.get("id"),
                "status": response_data.get("status")
            }
        else:
            # Erreur côté Mailchimp (ex: email invalide, clé incorrecte)
            error_detail = response_data.get("detail", "Erreur inconnue")
            logger.error(f"[Mailchimp] ❌ Erreur {response.status_code} : {error_detail}")
            return {
                "success": False,
                "error": error_detail,
                "status_code": response.status_code
            }

    except requests.exceptions.Timeout:
        logger.error("[Mailchimp] ❌ Timeout — Mailchimp ne répond pas")
        return {"success": False, "error": "Timeout Mailchimp"}

    except requests.exceptions.ConnectionError:
        logger.error("[Mailchimp] ❌ Connexion impossible")
        return {"success": False, "error": "Connexion impossible"}

    except Exception as e:
        logger.error(f"[Mailchimp] ❌ Erreur inattendue : {str(e)}")
        return {"success": False, "error": str(e)}



def create_and_send_campaign(subject: str, html_content: str, preview_text: str = "") -> dict:
    """
    Crée une campagne Mailchimp et l'envoie immédiatement à toute la liste.
    À appeler depuis l'admin Django ou une vue protégée.
    """
    api_key = settings.MAILCHIMP_API_KEY
    list_id = settings.MAILCHIMP_LIST_ID
    server = settings.MAILCHIMP_SERVER_PREFIX

    base_url = f"https://{server}.api.mailchimp.com/3.0"
    auth = ("anystring", api_key)

    # ── ÉTAPE 1 : Créer la campagne ──────────────────────
    campaign_res = requests.post(
        f"{base_url}/campaigns",
        json={
            "type": "regular",
            "recipients": {"list_id": list_id},
            "settings": {
                "subject_line": subject,
                "preview_text": preview_text,
                "from_name": "NDIARAMA",
                "reply_to": settings.MAILCHIMP_REPLY_TO,  # ton email
            },
        },
        auth=auth,
        timeout=10,
    )

    if campaign_res.status_code != 200:
        logger.error(f"[Mailchimp] ❌ Création campagne échouée : {campaign_res.json()}")
        return {"success": False, "error": campaign_res.json()}

    campaign_id = campaign_res.json()["id"]
    logger.info(f"[Mailchimp] ✅ Campagne créée : {campaign_id}")

    # ── ÉTAPE 2 : Ajouter le contenu HTML ────────────────
    content_res = requests.put(
        f"{base_url}/campaigns/{campaign_id}/content",
        json={"html": html_content},
        auth=auth,
        timeout=10,
    )

    if content_res.status_code != 200:
        logger.error(f"[Mailchimp] ❌ Contenu échoué : {content_res.json()}")
        return {"success": False, "error": content_res.json()}

    logger.info(f"[Mailchimp] ✅ Contenu ajouté à {campaign_id}")

    # ── ÉTAPE 3 : Envoyer la campagne ────────────────────
    send_res = requests.post(
        f"{base_url}/campaigns/{campaign_id}/actions/send",
        auth=auth,
        timeout=10,
    )

    # 204 = succès sans contenu (normal pour Mailchimp)
    if send_res.status_code == 204:
        logger.info(f"[Mailchimp] ✅ Campagne envoyée : {campaign_id}")
        return {"success": True, "campaign_id": campaign_id}
    else:
        logger.error(f"[Mailchimp] ❌ Envoi échoué : {send_res.json()}")
        return {"success": False, "error": send_res.json()}