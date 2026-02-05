import jinja2
from ..core.database import get_database
from bson import ObjectId
from datetime import datetime

class CampaignManager:
    @staticmethod
    def render_template(template_str: str, context: dict):
        template = jinja2.Template(template_str)
        return template.render(context)

    @staticmethod
    async def create_campaign(user_id: str, name: str, template: str, contacts: list):
        db = get_database()
        campaign = {
            "user_id": user_id,
            "name": name,
            "template": template,
            "total_contacts": len(contacts),
            "sent_count": 0,
            "failed_count": 0,
            "status": "pending",
            "created_at": datetime.utcnow()
        }
        result = await db.campaigns.insert_one(campaign)
        campaign_id = str(result.inserted_id)
        
        # Prepare message queue
        messages = []
        for contact in contacts:
            rendered_msg = CampaignManager.render_template(template, contact)
            messages.append({
                "campaign_id": campaign_id,
                "user_id": user_id,
                "phone": contact.get("phone"),
                "content": rendered_msg,
                "status": "queued",
                "created_at": datetime.utcnow()
            })
        
        if messages:
            await db.messages.insert_many(messages)
        
        return campaign_id
